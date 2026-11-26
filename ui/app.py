import os
import queue
import threading
import tkinter as tk
from tkinter import filedialog, ttk

from models import PaketTugas
from services import PengecekService
from utils.validasi import valid_lokasi_folder

LATAR = "#ffffff"
TEKS = "#1f2328"
AKSEN = "#1f5fa8"
AKSEN_GELAP = "#184a83"
HIJAU = "#1a6b2f"
MERAH = "#a1260d"
NONAKTIF = "#d6d9de"


def ringkas(nama, batas=48):
    """Potong bagian tengah nama berkas panjang agar ekstensinya tetap terlihat."""
    if len(nama) <= batas:
        return nama
    return nama[:batas - 15] + "..." + nama[-12:]


class AplikasiSiapKumpul(ttk.Frame):
    def __init__(self, induk, service=None):
        super().__init__(induk, padding=16)
        self.service = service or PengecekService()
        self.folder = tk.StringVar()
        self._antrean = queue.Queue()
        self._sedang_periksa = False

        self._atur_gaya()
        self._buat_widget()
        self.folder.trace_add("write", lambda *_: self._tampilkan_kosong())
        self._tampilkan_kosong()

    def _atur_gaya(self):
        gaya = ttk.Style(self)
        # Tema "clam" dipakai karena tema bawaan Windows mengabaikan warna latar tombol.
        gaya.theme_use("clam")
        gaya.configure(".", background=LATAR, foreground=TEKS)
        gaya.configure("Judul.TLabel", font=("TkDefaultFont", 16, "bold"))
        gaya.configure("Ringkasan.TLabel", font=("TkDefaultFont", 11, "bold"))
        gaya.configure("Lolos.Ringkasan.TLabel", foreground=HIJAU)
        gaya.configure("Perbaiki.Ringkasan.TLabel", foreground=MERAH)
        gaya.configure("Utama.TButton", background=AKSEN, foreground=LATAR,
                       focuscolor=LATAR, padding=(16, 6))
        gaya.map("Utama.TButton",
                 background=[("disabled", NONAKTIF), ("active", AKSEN_GELAP)],
                 foreground=[("disabled", TEKS)])
        gaya.configure("TButton", focuscolor=TEKS, padding=(12, 6))

    def _buat_widget(self):
        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="SiapKumpul", style="Judul.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(self, text="Cek berkas tugas OOP sebelum dikumpulkan di Sindig.").grid(
            row=1, column=0, sticky="w", pady=(0, 16))

        ttk.Label(self, text="Folder pengumpulan", underline=0).grid(row=2, column=0, sticky="w")
        baris = ttk.Frame(self)
        baris.grid(row=3, column=0, sticky="ew", pady=(4, 8))
        baris.columnconfigure(0, weight=1)
        self.isian = ttk.Entry(baris, textvariable=self.folder)
        self.isian.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.tombol_pilih = ttk.Button(baris, text="Pilih folder...", command=self.pilih_folder)
        self.tombol_pilih.grid(row=0, column=1)

        self.tombol_periksa = ttk.Button(self, text="Periksa berkas", style="Utama.TButton",
                                         command=self.periksa)
        self.tombol_periksa.grid(row=4, column=0, sticky="w")

        ttk.Separator(self).grid(row=5, column=0, sticky="ew", pady=16)

        self.area_hasil = ttk.Frame(self)
        self.area_hasil.grid(row=6, column=0, sticky="nsew")
        self.area_hasil.columnconfigure(1, weight=1)
        self.area_hasil.bind("<Configure>", lambda _: self._atur_lebar_teks())
        self.rowconfigure(6, weight=1)

        self.isian.bind("<Return>", lambda _: self.periksa())
        for tombol in (self.tombol_pilih, self.tombol_periksa):
            tombol.bind("<Return>", lambda e: e.widget.invoke())
        self.winfo_toplevel().bind("<Alt-f>", lambda _: self.isian.focus_set())
        self.isian.focus_set()

    def pilih_folder(self):
        pilihan = filedialog.askdirectory(parent=self, title="Pilih folder pengumpulan",
                                          mustexist=True)
        # Dialog yang dibatalkan mengembalikan nilai kosong.
        if pilihan:
            self.folder.set(pilihan)
            self.tombol_periksa.focus_set()

    def periksa(self):
        if self._sedang_periksa:
            return
        # Path hasil "Copy as path" di Windows diapit tanda kutip.
        folder = self.folder.get().strip().strip('"')
        if not folder:
            self._tampilkan_pesan("Isi lokasi folder dulu, atau klik \"Pilih folder...\".", True)
            return
        if not valid_lokasi_folder(folder):
            self._tampilkan_pesan("[PERBAIKI] Folder tidak ditemukan.", True)
            return
        self._atur_sibuk(True)
        self._tampilkan_pesan("Memeriksa berkas...")
        # ZIP besar bisa lama diuji, jadi pemeriksaan dijalankan di luar thread GUI.
        threading.Thread(target=self._kerjakan, args=(folder,), daemon=True).start()
        self.after(50, self._tunggu_hasil)

    def _kerjakan(self, folder):
        try:
            paket = PaketTugas.dari_folder(folder)
            self._antrean.put((paket, self.service.jalankan(paket), None))
        except Exception as galat:
            self._antrean.put((None, None, galat))

    def _tunggu_hasil(self):
        try:
            paket, laporan, galat = self._antrean.get_nowait()
        except queue.Empty:
            self.after(50, self._tunggu_hasil)
            return
        self._atur_sibuk(False)
        if galat:
            self._tampilkan_pesan(f"Pemeriksaan gagal: {galat}", True)
        else:
            self._tampilkan_laporan(paket, laporan)

    def _atur_sibuk(self, sibuk):
        self._sedang_periksa = sibuk
        status = ["disabled"] if sibuk else ["!disabled"]
        for widget in (self.isian, self.tombol_pilih, self.tombol_periksa):
            widget.state(status)
        self.winfo_toplevel().configure(cursor="watch" if sibuk else "")

    def _bersihkan_hasil(self):
        for widget in self.area_hasil.winfo_children():
            widget.destroy()

    def _tampilkan_kosong(self):
        self._tampilkan_pesan("Belum ada hasil. Pilih folder yang berisi diagram dan ZIP proyek.")

    def _tampilkan_pesan(self, pesan, galat=False):
        self._bersihkan_hasil()
        gaya = "Perbaiki.Ringkasan.TLabel" if galat else "TLabel"
        ttk.Label(self.area_hasil, text=pesan, style=gaya).grid(
            row=0, column=0, columnspan=2, sticky="w")
        self._atur_lebar_teks()

    def _tampilkan_laporan(self, paket, laporan):
        self._bersihkan_hasil()
        berkas = (("Diagram", paket.lokasi_diagram), ("ZIP", paket.lokasi_zip))
        for nomor, (jenis, lokasi) in enumerate(berkas):
            nama = ringkas(os.path.basename(lokasi)) if lokasi else "tidak ada"
            ttk.Label(self.area_hasil, text=f"{jenis}: {nama}").grid(
                row=nomor, column=0, columnspan=2, sticky="w")

        awal = len(berkas)
        for nomor, hasil in enumerate(laporan.hasil, start=awal):
            warna = "Lolos" if hasil.lolos else "Perbaiki"
            jarak = (12 if nomor == awal else 4, 0)
            ttk.Label(self.area_hasil, text=hasil.status,
                      style=f"{warna}.Ringkasan.TLabel").grid(
                row=nomor, column=0, sticky="nw", padx=(0, 12), pady=jarak)
            ttk.Label(self.area_hasil, text=hasil.pesan).grid(
                row=nomor, column=1, sticky="nw", pady=jarak)

        warna = "Lolos" if laporan.semua_lolos() else "Perbaiki"
        ttk.Label(self.area_hasil, text=laporan.kesimpulan(),
                  style=f"{warna}.Ringkasan.TLabel").grid(
            row=awal + len(laporan.hasil), column=0, columnspan=2, sticky="w", pady=(16, 0))
        self._atur_lebar_teks()

    def _atur_lebar_teks(self):
        self.area_hasil.update_idletasks()
        lebar = self.area_hasil.winfo_width()
        if lebar <= 1:
            return
        for label in self.area_hasil.winfo_children():
            info = label.grid_info()
            sisa = lebar - label.winfo_x() if int(info["column"]) else lebar
            label.configure(wraplength=max(sisa - 8, 100))
