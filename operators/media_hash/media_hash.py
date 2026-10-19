import gc
import hashlib
import os

from feluda import Operator


class MediaHash(Operator):
    def __init__(self) -> None:
        self.hash = None

    def run(self, feluda_media: dict, remove_after_processing: bool = False) -> str:
        if not isinstance(feluda_media, dict) or "path" not in feluda_media:
            raise ValueError("Expected a dict with a 'path' key.")

        file_path = feluda_media["path"]

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, "rb") as f:
                file_hash = hashlib.blake2b()
                while chunk := f.read(4092):
                    file_hash.update(chunk)
            self.hash = file_hash.hexdigest()
            return self.hash
        finally:
            if remove_after_processing and os.path.exists(file_path):
                os.remove(file_path)

    def cleanup(self) -> None:
        self.hash = None
        gc.collect()

    def state(self) -> dict:
        return {"hash": self.hash}
