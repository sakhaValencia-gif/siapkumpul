class LaporanPemeriksaan:
    def __init__(self):
        self._hasil = []

    def tambah(self, hasil):
        self._hasil.append(hasil)

    @property
    def hasil(self):
        return tuple(self._hasil)

    def semua_lolos(self):
        return bool(self._hasil) and all(h.lolos for h in self._hasil)

    def kesimpulan(self):
        return "Siap dikumpulkan!" if self.semua_lolos() else "Masih ada yang perlu diperbaiki."

    def teks(self):
        baris = [str(h) for h in self._hasil]
        baris.append(self.kesimpulan())
        return "\n".join(baris)
