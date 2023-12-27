import unittest
import detect_text_in_image_tesseract

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        detect_text_in_image_tesseract.initialize(param={})
    
    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    def test_sample_image_from_disk(self):
        image_path = "sample_data/text.png"
        image_text = detect_text_in_image_tesseract.run(image_path)
        expected_text = "It was the best of\ntimes, it was the worst\nof times, it was the age\nof wisdom, it was the\nage of foolishness..."
        self.assertEqual(image_text.strip(), expected_text.strip())

# if __name__ == "__main__":
#     unittest.main()