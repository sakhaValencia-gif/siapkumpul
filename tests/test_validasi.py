import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest, tempfile, zipfile

from utils.validasi import valid_lokasi_folder


class TestValidasi(unittest.TestCase):
    def test_folder_ada(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(valid_lokasi_folder(d))

    def test_folder_tidak_ada(self):
        self.assertFalse(valid_lokasi_folder("/tidak/ada"))
        self.assertFalse(valid_lokasi_folder(""))


if __name__ == "__main__":
    unittest.main()
