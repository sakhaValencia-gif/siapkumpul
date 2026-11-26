from models import (CekDiagram, CekArsipZip, CekStrukturProyek, LaporanPemeriksaan)


class PengecekService:
    def __init__(self, daftar_pemeriksaan=None):
        self.daftar = daftar_pemeriksaan or [CekDiagram(), CekArsipZip(), CekStrukturProyek()]

    def jalankan(self, paket):
        laporan = LaporanPemeriksaan()
        for pemeriksaan in self.daftar:
            laporan.tambah(pemeriksaan.periksa(paket))  # polymorphism
        return laporan
