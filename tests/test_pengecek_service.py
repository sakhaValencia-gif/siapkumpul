import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest, tempfile, zipfile

from models import PaketTugas
from services import PengecekService


class TestPengecekService(unittest.TestCase):
    def test_semua_lolos(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "diagram.png"), "w").write("x")
            with zipfile.ZipFile(os.path.join(d, "p.zip"), "w") as z:
                for n in ("main.py", "models/a.py", "services/b.py"):
                    z.writestr(n, "x")
            lap = PengecekService().jalankan(PaketTugas.dari_folder(d))
            self.assertTrue(lap.semua_lolos())

    def test_folder_kosong(self):
        with tempfile.TemporaryDirectory() as d:
            lap = PengecekService().jalankan(PaketTugas.dari_folder(d))
            self.assertFalse(lap.semua_lolos())
            self.assertIn("Masih ada", lap.teks())


if __name__ == "__main__":
    unittest.main()
