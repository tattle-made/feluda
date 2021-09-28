import unittest


class TestES(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # ping es server to see if its working
        print("setting up")

    @classmethod
    def tearDownClass(cls) -> None:
        # delete any artefacts created during tests
        print("tearing down")

    def test_create_indices(self):
        pass

    def test_store_vectors(self):
        pass

    def test_store_text(self):
        pass

    def test_search_vectors(self):
        pass

    def test_search_text(self):
        pass

    def test_store_metadata(self):
        pass

    def test_find_by_metadata_field(self):
        pass
