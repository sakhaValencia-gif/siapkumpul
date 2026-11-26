from abc import ABC, abstractmethod


class Pemeriksaan(ABC):
    """Kelas abstrak: tiap pemeriksaan wajib mengimplementasikan periksa()."""

    @abstractmethod
    def periksa(self, paket):
        """Kembalikan HasilCek untuk paket tugas."""
