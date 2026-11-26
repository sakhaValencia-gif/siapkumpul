LOLOS = "LOLOS"
PERBAIKI = "PERBAIKI"


class HasilCek:
    def __init__(self, status, pesan):
        self.status = status
        self.pesan = pesan

    @property
    def lolos(self):
        return self.status == LOLOS

    def __str__(self):
        return f"[{self.status}] {self.pesan}"
