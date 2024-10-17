import unittest
import detect_text_in_image_tesseract
import re


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        detect_text_in_image_tesseract.initialize(param={})

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    def test_sample_image_from_disk_hindi(self):
        image_path = "sample_data/hindi-text-2.png"
        image_text = detect_text_in_image_tesseract.run(image_path)
        expected_text = "( मेरे पीछे कौन आ रहा है)"
        self.assertEqual(image_text.strip(), expected_text.strip())

    def test_sample_image_from_disk_tamil(self):
        image_path = "sample_data/tamil-text.png"
        image_text = detect_text_in_image_tesseract.run(image_path)
        cleaned_image_text = re.sub(r'[\u200c\u200b]', '', image_text) # remove zero width space and zero width non-joiner \u200c and \u200b
        expected_text = "காதல் மற்றும் போர்"
        self.assertEqual(cleaned_image_text.strip(), expected_text.strip())

    def test_sample_image_from_disk_telugu(self):
        image_path = "sample_data/telugu-text.png"
        image_text = detect_text_in_image_tesseract.run(image_path)
        expected_text = "నేను భూమిని ప్రేమిస్తున్నాను"
        self.assertEqual(image_text.strip(), expected_text.strip())


# if __name__ == "__main__":
#     unittest.main()
