import unittest

# from unittest.mock import patch
import detect_objects


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        detect_objects.initialize(param={})

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    def test_sample_image_from_disk(self):
        detected_classes = []
        image_path = "sample_data/people.jpg"
        _, detected_classes = detect_objects.run(image_path)
        expected_classes = ["person", "person", "person", "person"]
        for expected_class in expected_classes:
            self.assertIn(expected_class, detected_classes)


# if __name__ == "__main__":
#     unittest.main()
