import os


def initialize(param):
    global config_psm
    global config_oem
    config_psm = param.get("psm", 6)
    config_oem = param.get("oem", 1)

    try:
        global Image
        global pytesseract
        global requests
        global BytesIO

        from io import BytesIO

        import pytesseract
        import requests
        from PIL import Image

        try:
            pytesseract.get_tesseract_version()
        except pytesseract.TesseractNotFoundError:
            raise RuntimeError(
                "Tesseract OCR is not installed or not in PATH. "
            )

        required_langs = ["eng", "hin", "tam", "tel"]
        try:
            installed_langs = pytesseract.get_languages()
            missing_langs = [lang for lang in required_langs if lang not in installed_langs]
            if missing_langs:
                print(f"Warning: Some required language packs are not installed: {', '.join(missing_langs)}")
                print("OCR may not work correctly for these languages.")
        except Exception as e:
            print(f"Warning: Could not verify language pack installation: {e}")

    except ImportError as e:
        raise ImportError(
            f"Failed to import required packages: {e}. "
            "Please ensure pytesseract and Pillow are installed."
        )


def run(image_path, delete_after=False):


    try:
        with Image.open(image_path) as load_image:
            data = pytesseract.image_to_string(
                load_image, lang="eng+hin+tam+tel", config=f"--psm {config_psm} --oem {config_oem}"
            )

        if delete_after and os.path.exists(image_path):
            try:
                os.remove(image_path)
                print(f"Successfully deleted temporary file: {image_path}")
            except OSError as e:
                print(f"Warning: Could not delete file {image_path}: {e}")

        return data

    except Exception as e:
        if delete_after and os.path.exists(image_path):
            try:
                os.remove(image_path)
                print(f"Deleted temporary file after error: {image_path}")
            except OSError as e:
                print(f"Warning: Could not delete file {image_path} after error: {e}")
        raise RuntimeError(f"Text detection failed: {e}")
