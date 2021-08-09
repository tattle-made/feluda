import unittest
from image import detect_text, get_vector


class TestImageOperator(unittest.TestCase):
    def test_detect_text(self):
        pass
        file = open("./test_data/image-with-text.jpg", "rb")
        content = file.read()
        text_in_image = detect_text(content)
        self.assertEqual(text_in_image["text"], "GRAZY\n")
        file.close()

    def test_get_vector(self):
        pass

    def test_get_vector_from_file(self):
        """
        This requires mocking wertrezeug.FileStorage and might be
        counter productive.
        """
        pass

    def test_get_vector_from_url(self):
        file_url = ""
        image_vec = get_vector(file_url, "url")
        self.assertEqual(image_vec.length, 516)

    def test_get_doc(self):
        pass


if __name__ == "__main__":
    unittest.main()
