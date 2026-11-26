import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest, tempfile, zipfile

from models import PaketTugas, CekDiagram, CekArsipZip, CekStrukturProyek


def buat_zip(folder, isi):
    p = os.path.join(folder, "proyek.zip")
    with zipfile.ZipFile(p, "w") as z:
        for n in isi:
            z.writestr(n, "x")
    return p


class TestPemeriksaan(unittest.TestCase):
    def test_diagram_hilang(self):
        self.assertFalse(CekDiagram().periksa(PaketTugas()).lolos)

    def test_zip_rusak(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "proyek.zip")
            open(p, "w").write("bukan zip")
            self.assertFalse(CekArsipZip().periksa(PaketTugas(None, p)).lolos)

    def test_struktur_kurang(self):
        with tempfile.TemporaryDirectory() as d:
            z = buat_zip(d, ["README.md"])
            h = CekStrukturProyek().periksa(PaketTugas(None, z))
            self.assertIn("main.py, models/, services/", h.pesan)

    def test_struktur_lengkap_dengan_folder_induk(self):
        with tempfile.TemporaryDirectory() as d:
            z = buat_zip(d, ["app/main.py", "app/models/a.py", "app/services/b.py"])
            self.assertTrue(CekStrukturProyek().periksa(PaketTugas(None, z)).lolos)


if __name__ == "__main__":
    unittest.main()
