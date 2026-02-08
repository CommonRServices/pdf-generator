import os
import pathlib
import tempfile


class TempDirStorage:
    def __init__(self) -> None:
        self._td = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self._td.name)

    def cleanup(self):
        self._td.cleanup()

    def save_bytes(self, filename: str, content: bytes) -> str:
        abs_path = os.path.join(self.root, filename)
        with open(abs_path, "wb") as f:
            f.write(content)
        return abs_path
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
