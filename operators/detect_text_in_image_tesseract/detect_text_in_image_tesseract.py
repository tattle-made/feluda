import gc
import os
import shutil
from typing import Any

import pytesseract
from PIL import Image

from feluda import Operator
from feluda.factory import ImageFactory


class ImageTextDetector(Operator):
    """Operator to detect text in images using Tesseract OCR."""

    def __init__(self, psm: int = 6, oem: int = 1, tesseract_cmd: str = None) -> None:
        """Initialize the `ImageTextDetector` class.

        Args:
            psm (int): Page segmentation mode for Tesseract (default: 6)
            oem (int): OCR Engine mode for Tesseract (default: 1)
        """
        self.psm = psm
        self.oem = oem
        self.tesseract_cmd = tesseract_cmd or shutil.which("tesseract")
        self.validate_system()
        self.validate_languages()

    def validate_system(self) -> None:
        """Validate that Tesseract OCR is installed and accessible.

        Raises:
            RuntimeError: If Tesseract is not installed or not in PATH.
        """
        if self.tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd
        try:
            pytesseract.get_tesseract_version()
        except pytesseract.TesseractNotFoundError:
            raise RuntimeError(
                "Tesseract OCR is not installed or not in PATH. "
                "Please install Tesseract to use this operator."
            )

    def validate_languages(self) -> None:
        """Validate that required language packs are installed.

        Checks for English, Hindi, Tamil, and Telugu language support.
        """
        required_langs = ["eng", "hin", "tam", "tel"]
        try:
            installed_langs = pytesseract.get_languages()
            missing_langs = [
                lang for lang in required_langs if lang not in installed_langs
            ]
            if missing_langs:
                print(
                    f"Warning: Some required language packs are not installed: {', '.join(missing_langs)}"
                )
                print("OCR may not work correctly for these languages.")
        except Exception as e:
            print(f"Warning: Could not verify language pack installation: {e}")

    def run(self, file: ImageFactory, remove_after_processing: bool = False) -> str:
        """Run the text detection operator.

        Args:
            file (ImageFactory): ImageFactory object
            remove_after_processing (bool): Whether to remove the file after processing

        Returns:
            str: Detected text from the image
        """
        if not isinstance(file, dict) or "path" not in file:
            raise ValueError(
                "Invalid file object. Expected ImageFactory object with 'path' key."
            )

        image_path = file["path"]

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        try:
            with Image.open(image_path) as load_image:
                text = pytesseract.image_to_string(
                    load_image,
                    lang="eng+hin+tam+tel",
                    config=f"--psm {self.psm} --oem {self.oem}",
                )
            return text

        except Exception as e:
            raise RuntimeError(f"Text detection failed: {e}") from e

        finally:
            if remove_after_processing:
                try:
                    if os.path.exists(image_path):
                        os.remove(image_path)
                except OSError as e:
                    print(f"Warning: Could not delete file {image_path}: {e}")

    def cleanup(self) -> None:
        """Cleans up resources used by the operator."""
        gc.collect()

    def state(self) -> dict[str, Any]:
        """Returns the current state of the operator.

        Returns:
            dict: State of the operator including PSM and OEM settings
        """
        return {
            "psm": self.psm,
            "oem": self.oem,
        }
