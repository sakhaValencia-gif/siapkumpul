import zipfile


class ZipTidakValid(Exception):
    pass


def daftar_isi_zip(path):
    """Kembalikan daftar nama berkas di dalam ZIP; ZipTidakValid bila gagal."""
    if not path:
        raise ZipTidakValid("tidak ada path")
    try:
        with zipfile.ZipFile(path) as z:
            if z.testzip() is not None:
                raise ZipTidakValid("isi ZIP rusak")
            return z.namelist()
    except (zipfile.BadZipFile, OSError) as e:
        raise ZipTidakValid(str(e))
