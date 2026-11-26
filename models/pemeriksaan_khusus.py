import os

from utils.zip_reader import daftar_isi_zip, ZipTidakValid
from .hasil_cek import HasilCek, LOLOS, PERBAIKI
from .pemeriksaan import Pemeriksaan


class CekDiagram(Pemeriksaan):
    def periksa(self, paket):
        if paket.lokasi_diagram and os.path.isfile(paket.lokasi_diagram):
            return HasilCek(LOLOS, "Diagram ditemukan.")
        return HasilCek(PERBAIKI, "Berkas diagram belum ditemukan.")


class CekArsipZip(Pemeriksaan):
    def periksa(self, paket):
        if not paket.lokasi_zip or not os.path.isfile(paket.lokasi_zip):
            return HasilCek(PERBAIKI, "ZIP proyek belum ditemukan.")
        try:
            daftar_isi_zip(paket.lokasi_zip)
        except ZipTidakValid:
            return HasilCek(PERBAIKI, "ZIP proyek rusak atau tidak bisa dibuka.")
        return HasilCek(LOLOS, "ZIP proyek bisa dibuka.")


class CekStrukturProyek(Pemeriksaan):
    WAJIB_BERKAS = ("main.py",)
    WAJIB_FOLDER = ("models", "services")

    def periksa(self, paket):
        try:
            isi = daftar_isi_zip(paket.lokasi_zip)
        except ZipTidakValid:
            return HasilCek(PERBAIKI, "Struktur belum bisa dicek karena ZIP belum bisa dibuka.")
        kurang = []
        for b in self.WAJIB_BERKAS:
            if not any(p == b or (p.endswith("/" + b) and p.count("/") <= 1) for p in isi):
                kurang.append(b)
        for f in self.WAJIB_FOLDER:
            if not any(p.startswith(f + "/") or ("/" + f + "/") in p for p in isi):
                kurang.append(f + "/")
        if kurang:
            return HasilCek(PERBAIKI, "ZIP belum berisi " + ", ".join(kurang) + ".")
        return HasilCek(LOLOS, "Struktur proyek lengkap (main.py, models/, services/).")
