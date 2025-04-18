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


def run(image_path):
    try:
        with Image.open(image_path) as load_image:
            data = pytesseract.image_to_string(
                load_image, lang="eng+hin+tam+tel", config=f"--psm {config_psm} --oem {config_oem}"
            )
        return data
    except Exception as e:
        raise RuntimeError(f"Text detection failed: {e}")

def cleanup(param):
    pass


def state():
    pass


# image_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png"
# response = requests.get(image_url)
# response.raise_for_status()
# text_data = run(BytesIO(response.content))
# print(text_data)
