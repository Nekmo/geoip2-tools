import os.path
import time
from pathlib import Path


DEFAULT_GENERIC_TIMEOUT = 60 * 15
DEFAULT_SLEEP = .1


class GenericLockFile:
    def __init__(self, lock_file: str, timeout: int = DEFAULT_GENERIC_TIMEOUT,
                 sleep: float = DEFAULT_SLEEP):
        self.lock_file = Path(lock_file)
        self.timeout = timeout
        self.sleep = sleep
        directory = self.lock_file.parent
        os.makedirs(directory, exist_ok=True)

    def __enter__(self):
        i = 0
        max_retries = self.timeout / self.sleep
        while self.lock_file.exists():
            time.sleep(self.sleep)
            if max_retries and i >= max_retries:
                break
            i += 1
        self.lock_file.touch()

    def __exit__(self, *args):
        self.lock_file.unlink(missing_ok=True)


class PosixLockFile(GenericLockFile):
    def __enter__(self):
        import fcntl
        self.lock_file.touch()
        with open(str(self.lock_file), 'w') as f:
            fcntl.flock(f, fcntl.LOCK_EX)

    def __exit__(self, *args):
        import fcntl
        with open(str(self.lock_file), 'w') as f:
            fcntl.flock(f, fcntl.LOCK_UN)


def lock_file(lock_file: str):
    if os.name == 'posix':
        return PosixLockFile(lock_file)
    else:
        return GenericLockFile(lock_file)
