import tkinter as tk

from ui import AplikasiSiapKumpul
from ui.app import LATAR


def main():
    jendela = tk.Tk()
    jendela.title("SiapKumpul")
    jendela.geometry("620x480")
    jendela.minsize(480, 460)
    jendela.configure(background=LATAR)
    AplikasiSiapKumpul(jendela).pack(fill="both", expand=True)
    jendela.mainloop()


if __name__ == "__main__":
    main()
