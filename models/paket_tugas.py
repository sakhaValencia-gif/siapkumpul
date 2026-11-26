import os

EKSTENSI_DIAGRAM = (".png", ".jpg", ".jpeg", ".pdf", ".svg", ".drawio")


class PaketTugas:
    """Menyimpan lokasi berkas diagram dan ZIP proyek (None bila tidak ada)."""

    def __init__(self, lokasi_diagram=None, lokasi_zip=None):
        self.lokasi_diagram = lokasi_diagram
        self.lokasi_zip = lokasi_zip

    @classmethod
    def dari_folder(cls, folder):
        diagram = zip_ = None
        if os.path.isdir(folder):
            for nama in sorted(os.listdir(folder)):
                path = os.path.join(folder, nama)
                low = nama.lower()
                if zip_ is None and low.endswith(".zip"):
                    zip_ = path
                elif diagram is None and low.endswith(EKSTENSI_DIAGRAM):
                    diagram = path
        return cls(diagram, zip_)
