import os


def valid_lokasi_folder(lokasi):
    return bool(lokasi) and os.path.isdir(lokasi)
