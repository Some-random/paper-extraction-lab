"""Publish only the census's generated reports, preserving other local edits."""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timedelta, timezone
try:
    from .report_publication_lock import publication_lock
except ImportError:  # Existing command-line runners import from ROOT/src.
    from report_publication_lock import publication_lock


def publish_reports(root, run_dir, report_dir):
    with publication_lock(root):
        return _publish_reports(root, run_dir, report_dir)


def _publish_reports(root, run_dir, report_dir):
    """Return delivery status; a delivery failure must never stop acquisition."""
    result = {"at_pst": datetime.now(timezone(timedelta(hours=-8))).isoformat()}

    def git(*args):
        command = subprocess.run(["git", *args], cwd=root, text=True,
                                 capture_output=True, timeout=45)
        if command.returncode:
            # Do not copy transport output or credential-bearing URLs to logs.
            raise RuntimeError(f"git {args[0]} exited {command.returncode}")
        return command.stdout.strip()

    try:
        relative = report_dir.resolve().relative_to(root.resolve())
        if not relative.parts or relative.parts[0] != "reports":
            raise ValueError("Publication is restricted to this repository's reports directory")
        paths = [str(relative / name) for name in
                 ("README.md", "source_coverage.md", "summary.json", "progress.md")
                 if (report_dir / name).exists()]
        if git("symbolic-ref", "--short", "HEAD") != "main":
            raise RuntimeError("Automatic report publication requires main")
        if git("rev-parse", "--abbrev-ref", "@{upstream}") != "origin/main":
            raise RuntimeError("Automatic report publication requires upstream origin/main")
        # A retry may include our earlier unpushed report commit. Do not publish
        # someone else's unrelated commits just because they are on this branch.
        ahead = git("rev-list", "origin/main..HEAD").splitlines()
        for commit in ahead:
            subject = git("show", "-s", "--format=%s", commit)
            changed = set(git("diff-tree", "--no-commit-id", "--name-only", "-r", commit).splitlines())
            if not subject.startswith("Report corpus progress:") or not changed.issubset(paths):
                raise RuntimeError("Unpublished unrelated commits need review before automatic publication")
        git("add", "--", *paths)
        changed = git("diff", "--name-only", "HEAD", "--", *paths)
        if changed:
            summary = json.loads((report_dir / "summary.json").read_text())
            message = f"Report corpus progress: {summary['run_id']} ({summary['status']})"
            # --only commits the named generated paths even when unrelated files
            # are already staged. Their staged and working copies stay intact.
            git("commit", "--only", "-m", message, "--", *paths)
        result["commit"] = git("rev-parse", "HEAD")
        git("push", "origin", "refs/heads/main:refs/heads/main")
        result["status"] = "published"
    except Exception as exc:
        result.update(status="failed", error=f"{type(exc).__name__}: {exc}")
    run_dir.mkdir(parents=True, exist_ok=True)
    temporary = run_dir / "progress_delivery.json.tmp"
    temporary.write_text(json.dumps(result, indent=2) + "\n")
    temporary.replace(run_dir / "progress_delivery.json")
    return result
