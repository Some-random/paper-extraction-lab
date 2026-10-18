import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("benchmark_admission", SCRIPTS / "admit_training_benchmarks.py")
admission = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(admission)

NODE = ("NodeName=blackwell1 State=MIXED+PLANNED Partitions=il,il-data CPUEfctv=288 CPUAlloc=248 "
        "RealMemory=3090000 AllocMem=2611200 CfgTRES=cpu=288,mem=3090000M,gres/gpu=8,gres/gpu:b200=8 "
        "AllocTRES=cpu=248,mem=2550G,gres/gpu=6,gres/gpu:b200=6")
LAUNCH = {"job_id": "123", "admission_required": True, "target_gpu": "B200", "requested_gpus": 2,
          "cpus_per_task": 24, "memory_mib": 192 * 1024}


def job(**changes):
    value = dict(JobId="123", UserId=f"owner({os.getuid()})", JobName="bio4b-match", QOS="il-lo",
                 Account="infolab", Partition="il", Nice="10000", Requeue="0",
                 NumNodes="1", NumTasks="1", NumCPUs="24",
                 TimeLimit="00:20:00", ReqTRES="cpu=24,mem=192G,node=1,gres/gpu=2,gres/gpu:b200=2",
                 JobState="PENDING", Reason="JobHeldUser", Priority="0", ReqNodeList="(null)")
    value.update(changes)
    return " ".join(f"{key}={value}" for key, value in value.items())


class Scheduler:
    def __init__(self, *, preview="safe", initial=None, second_node=None):
        self.calls, self.bound = [], False
        self.preview, self.initial, self.second_node = preview, initial, second_node

    def __call__(self, args):
        self.calls.append(args)
        if args[:3] == ["scontrol", "show", "job"]:
            return self.initial or job(ReqNodeList="blackwell1" if self.bound else "(null)")
        if args[:3] == ["scontrol", "show", "nodes"]:
            return NODE
        if args[:3] == ["scontrol", "show", "node"]:
            return self.second_node or NODE
        if args[0] == "sbatch":
            return "Job 0 to start at 2026-10-18T20:00:00 using 24 processors on nodes blackwell1" + (
                " Preempts: 999" if self.preview == "preempt" else "")
        if args[:2] == ["scontrol", "update"]:
            self.bound = True
        return ""


class AdmissionTests(unittest.TestCase):
    def test_typed_spare_resources_and_reject_bad_states(self):
        node = admission.fields(NODE)
        self.assertTrue(admission.spare(node, "b200", 2, 24, 192 * 1024))
        self.assertFalse(admission.spare(node, "b200", 3, 24, 192 * 1024))
        self.assertFalse(admission.spare(node, "b200", 2, 48, 192 * 1024))
        self.assertFalse(admission.spare(node, "b200", 2, 24, 512 * 1024))
        for state in ("MIXED+DRAIN", "DOWN", "MIXED+MAINT", "MIXED+NOT_RESPONDING"):
            self.assertFalse(admission.spare({**node, "State": state}, "b200", 2, 24, 192 * 1024))
        self.assertFalse(admission.spare({**node, "AllocTRES": "gres/gpu=6"}, "b200", 2, 24, 192 * 1024))

    def test_preemption_or_missing_success_preview_never_releases(self):
        scheduler = Scheduler(preview="preempt")
        self.assertEqual(admission.attempt("123", LAUNCH, scheduler)["status"], "waiting_spare_capacity")
        self.assertFalse(any(args[:2] == ["scontrol", "release"] for args in scheduler.calls))
        self.assertFalse(admission.preview_safe("not scheduled on nodes blackwell1", "blackwell1"))
        self.assertFalse(admission.preview_safe("Job 0 to start at now on nodes ampere1", "blackwell1"))

    def test_binds_reqnodelist_rechecks_then_releases_only_allowlisted_id(self):
        scheduler = Scheduler()
        result = admission.attempt("123", LAUNCH, scheduler)
        self.assertEqual(result, {"status": "released", "node": "blackwell1"})
        self.assertIn(["scontrol", "update", "JobId=123", "ReqNodeList=blackwell1"], scheduler.calls)
        self.assertEqual(scheduler.calls[-1], ["scontrol", "release", "123"])
        self.assertEqual(sum(args[0] == "sbatch" for args in scheduler.calls), 2)
        self.assertTrue(all("--test-only" in args for args in scheduler.calls if args[0] == "sbatch"))

    def test_owner_shape_and_name_mismatches_never_mutate(self):
        for changes in ({"UserId": "other(99999)"}, {"JobName": "evaluation"}, {"NumCPUs": "48"},
                        {"TimeLimit": "1-00:00:00"}, {"QOS": "il"}, {"JobId": "999"},
                        {"Nice": "0"}, {"Requeue": "1"}):
            scheduler = Scheduler(initial=job(**changes))
            self.assertEqual(admission.attempt("123", LAUNCH, scheduler)["status"], "invalid_request")
            self.assertEqual(len(scheduler.calls), 1)

    def test_capacity_taken_between_checks_keeps_held(self):
        scheduler = Scheduler(second_node=NODE.replace("gres/gpu:b200=6", "gres/gpu:b200=8"))
        self.assertEqual(admission.attempt("123", LAUNCH, scheduler)["status"], "waiting_spare_capacity")
        self.assertFalse(any(args[:2] == ["scontrol", "release"] for args in scheduler.calls))

    def test_persisted_deadline_stops_without_scheduler_actions_or_budget_reset(self):
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            (run / "admission_state.json").write_text(json.dumps({
                "job_ids": ["123"], "started_epoch": 0, "deadline_epoch": 100, "jobs": {}}))
            calls = []
            state = admission.supervise(run, ["123"], command=lambda args: calls.append(args), clock=lambda: 101)
            self.assertEqual(state["stop_reason"], "admission_runtime_limit")
            self.assertEqual(state["deadline_epoch"], 100)
            self.assertEqual(calls, [])
            with self.assertRaises(ValueError):
                admission.supervise(run, ["999"], once=True, clock=lambda: 101)

    def test_running_job_is_never_released_or_modified(self):
        scheduler = Scheduler(initial=job(JobState="RUNNING", Reason="None", Priority="100"))
        self.assertEqual(admission.attempt("123", LAUNCH, scheduler)["status"], "already_started")
        self.assertEqual(len(scheduler.calls), 1)

    def test_single_node_range_form_is_valid_and_larger_ranges_rejected(self):
        shape = admission.request_shape(LAUNCH)
        self.assertTrue(admission.valid_job(admission.fields(job(NumNodes="1-1")), "123", shape, os.getuid()))
        for nodes in ("1-2", "2", "2-2"):
            self.assertFalse(admission.valid_job(admission.fields(job(NumNodes=nodes)), "123", shape, os.getuid()))

    def test_only_explicit_terminal_scheduler_states_unblock_second_request(self):
        for state in ("CONFIGURING", "SUSPENDED", "RESIZING", "SIGNALING", "UNKNOWN"):
            scheduler = Scheduler(initial=job(JobState=state))
            result = admission.attempt("123", LAUNCH, scheduler)
            self.assertEqual(result["status"], "already_started")
            self.assertEqual(len(scheduler.calls), 1)
        for state in admission.TERMINAL_SLURM:
            self.assertEqual(admission.attempt("123", LAUNCH, Scheduler(initial=job(JobState=state)))["status"], "terminal")

    def test_released_pending_or_running_job_blocks_second_until_terminal(self):
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            for job_id in ("123", "124"):
                (run / f"launch_{job_id}.json").write_text(json.dumps({**LAUNCH, "job_id": job_id}))
            with mock.patch.object(admission, "attempt", return_value={"status": "released"}) as attempt:
                state = admission.supervise(run, ["123", "124"], once=True, clock=lambda: 100)
                self.assertEqual([call.args[0] for call in attempt.call_args_list], ["123"])
                self.assertEqual(state["jobs"]["124"]["status"], "waiting_spare_capacity")
            for slurm in ("PENDING", "RUNNING"):
                with mock.patch.object(admission, "attempt") as attempt:
                    state = admission.supervise(run, ["123", "124"], once=True, clock=lambda: 110,
                                                command=lambda args: job(JobState=slurm))
                    attempt.assert_not_called()
                    self.assertEqual(state["jobs"]["123"]["scheduler_state"], slurm)
            with mock.patch.object(admission, "attempt", return_value={"status": "released"}) as attempt:
                state = admission.supervise(run, ["123", "124"], once=True, clock=lambda: 120,
                                            command=lambda args: job(JobState="COMPLETED"))
                self.assertEqual([call.args[0] for call in attempt.call_args_list], ["124"])
                self.assertEqual(state["jobs"]["123"]["status"], "terminal")

    def test_accounting_only_unblocks_on_authoritative_terminal_record(self):
        def missing_job(args):
            if args[0] == "scontrol":
                raise RuntimeError("Forgotten allocation")
            self.assertIn("123", args)
            return "123.batch|COMPLETED\n123|COMPLETED\n999|RUNNING\n"
        self.assertEqual(admission.refresh_active("123", {"status": "released"}, missing_job)["status"], "terminal")
        with self.assertRaises(ValueError):
            admission.refresh_active("123", {"status": "released"}, lambda args: "")

    def test_four_and_eight_b200_shapes_require_exact_resources(self):
        for count, cpus, gib in ((4, 32, 256), (8, 48, 384)):
            launch = {**LAUNCH, "requested_gpus": count, "cpus_per_task": cpus, "memory_mib": gib * 1024}
            shape = admission.request_shape(launch)
            self.assertEqual(shape, ("b200", count, cpus, gib * 1024))
            request = admission.fields(job(NumCPUs=str(cpus),
                ReqTRES=f"cpu={cpus},mem={gib}G,node=1,gres/gpu={count},gres/gpu:b200={count}"))
            self.assertTrue(admission.valid_job(request, "123", shape, os.getuid()))
            with self.assertRaises(ValueError):
                admission.request_shape({**launch, "cpus_per_task": cpus - 1})
            with self.assertRaises(ValueError):
                admission.request_shape({**launch, "memory_mib": (gib - 1) * 1024})

    def test_four_requests_preserve_budget_and_active_job_blocks_every_other_request(self):
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            ids = ["123", "124", "125", "126"]
            (run / "admission_state.json").write_text(json.dumps({
                "job_ids": ids, "started_epoch": 10, "deadline_epoch": 500,
                "jobs": {"123": {"status": "released"},
                         **{job_id: {"status": "waiting_spare_capacity"} for job_id in ids[1:]}}}))
            with mock.patch.object(admission, "attempt") as attempt:
                state = admission.supervise(run, ids, once=True, clock=lambda: 110,
                                            command=lambda args: job(JobState="RUNNING"))
                attempt.assert_not_called()
            self.assertEqual(state["started_epoch"], 10)
            self.assertEqual(state["deadline_epoch"], 500)
            self.assertEqual(set(state["jobs"]), set(ids))
            self.assertEqual(state["supervisor_status"], "watching")
            with self.assertRaises(ValueError):
                admission.supervise(run, [*ids, "127"], once=True, clock=lambda: 110)


if __name__ == "__main__":
    unittest.main()
