import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from corpus_progress_publish import publish_reports


class ProgressPublicationTests(unittest.TestCase):
    def test_publishes_only_reports_and_preserves_unrelated_staged_edits(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            remote, root = base / "remote.git", base / "repo"
            subprocess.run(["git", "init", "--bare", "--initial-branch=main", str(remote)],
                           check=True, capture_output=True)
            root.mkdir()

            def git(*args):
                return subprocess.run(["git", *args], cwd=root, check=True,
                                      capture_output=True, text=True).stdout.strip()

            git("init", "--initial-branch=main")
            git("config", "user.name", "Test")
            git("config", "user.email", "test@example.invalid")
            report = root / "reports" / "test"
            report.mkdir(parents=True)
            (report / "summary.json").write_text(json.dumps({"run_id": "test", "status": "running"}))
            (root / "other.txt").write_text("original\n")
            git("add", ".")
            git("commit", "-m", "Initial")
            git("remote", "add", "origin", str(remote))
            git("push", "-u", "origin", "main")
            (root / "other.txt").write_text("staged change\n")
            git("add", "other.txt")
            (root / "other.txt").write_text("unstaged change\n")
            (report / "progress.md").write_text("Latest progress\n")
            (report / "summary.json").write_text(json.dumps({"run_id": "test", "status": "stopped"}))
            result = publish_reports(root, base / "run", report)
            self.assertEqual(result["status"], "published", result)
            self.assertEqual(git("show", "HEAD:other.txt"), "original")
            self.assertEqual(git("show", ":other.txt"), "staged change")
            self.assertEqual((root / "other.txt").read_text(), "unstaged change\n")
            self.assertEqual(git("rev-parse", "HEAD"), git("rev-parse", "origin/main"))
            self.assertEqual(set(git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").splitlines()),
                             {"reports/test/summary.json", "reports/test/progress.md"})
            # Reporting may never publish unrelated source commits automatically.
            git("commit", "-m", "Unrelated work")
            (report / "progress.md").write_text("New progress\n")
            blocked = publish_reports(root, base / "run", report)
            self.assertEqual(blocked["status"], "failed")
            self.assertIn("Unpublished unrelated commits", blocked["error"])
            self.assertNotEqual(git("rev-parse", "HEAD"), git("rev-parse", "origin/main"))


if __name__ == "__main__":
    unittest.main()
