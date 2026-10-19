"""Serialize report commits from independent workers sharing this checkout."""
from contextlib import contextmanager
import fcntl


@contextmanager
def publication_lock(root):
    directory = root / "experiments"
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "report_publication.lock").open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield
