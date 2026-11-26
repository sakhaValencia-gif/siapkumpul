"""Contoh polymorphism: semua Pemeriksaan dipanggil dengan periksa(paket) yang sama."""
from models import PaketTugas, CekDiagram, CekArsipZip, CekStrukturProyek

paket = PaketTugas()
for p in (CekDiagram(), CekArsipZip(), CekStrukturProyek()):
    print(type(p).__name__, "->", p.periksa(paket))
