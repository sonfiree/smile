from pathlib import Path

from smile.data.prepare.contrib.celeb_a_download import download_file_from_google_drive
from smile.data.prepare.contrib.celeb_a_download import unzip


_CELEB_A_HQ_DELTA_FILES = [
    ("deltas00000.zip", "0B4qLcYyJmiz0TXdaTExNcW03ejA"),
    ("deltas01000.zip", "0B4qLcYyJmiz0TjAwOTRBVmRKRzQ"),
    ("deltas02000.zip", "0B4qLcYyJmiz0TjNRV2dUamd0bEU"),
    ("deltas03000.zip", "0B4qLcYyJmiz0TjRWUXVvM3hZZE0"),
    ("deltas04000.zip", "0B4qLcYyJmiz0TjRxVkZ1NGxHTXc"),
    ("deltas05000.zip", "0B4qLcYyJmiz0TjRzeWlhLVJIYk0"),
    ("deltas06000.zip", "0B4qLcYyJmiz0TjVkYkF4dTJRNUk"),
    ("deltas07000.zip", "0B4qLcYyJmiz0TjdaV2ZsQU94MnM"),
    ("deltas08000.zip", "0B4qLcYyJmiz0Tksyd21vRmVqamc"),
    ("deltas09000.zip", "0B4qLcYyJmiz0Tl9wNEU2WWRqcE0"),
    ("deltas10000.zip", "0B4qLcYyJmiz0TlBCNFU3QkctNkk"),
    ("deltas11000.zip", "0B4qLcYyJmiz0TlNyLUtOTzk3QjQ"),
    ("deltas12000.zip", "0B4qLcYyJmiz0Tlhvdl9zYlV4UUE"),
    ("deltas13000.zip", "0B4qLcYyJmiz0TlpJU1pleF9zbnM"),
    ("deltas14000.zip", "0B4qLcYyJmiz0Tm5MSUp3ZTZ0aTg"),
    ("deltas15000.zip", "0B4qLcYyJmiz0TmRZTmZyenViSjg"),
    ("deltas16000.zip", "0B4qLcYyJmiz0TmVkVGJmWEtVbFk"),
    ("deltas17000.zip", "0B4qLcYyJmiz0TmZqZXN3UWFkUm8"),
    ("deltas18000.zip", "0B4qLcYyJmiz0TmhIUGlVeE5pWjg"),
    ("deltas19000.zip", "0B4qLcYyJmiz0TnBtdW83OXRfdG8"),
    ("deltas20000.zip", "0B4qLcYyJmiz0TnJQSS1vZS1JYUE"),
    ("deltas21000.zip", "0B4qLcYyJmiz0TzBBNE8xbFhaSlU"),
    ("deltas22000.zip", "0B4qLcYyJmiz0TzZySG9IWlZaeGc"),
    ("deltas23000.zip", "0B4qLcYyJmiz0U05ZNG14X3ZjYW8"),
    ("deltas24000.zip", "0B4qLcYyJmiz0U0YwQmluMmJuX2M"),
    ("deltas25000.zip", "0B4qLcYyJmiz0U0lYX1J1Tk5vMjQ"),
    ("deltas26000.zip", "0B4qLcYyJmiz0U0tBanQ4cHNBUWc"),
    ("deltas27000.zip", "0B4qLcYyJmiz0U1BRYl9tSWFWVGM"),
    ("deltas28000.zip", "0B4qLcYyJmiz0U1BhWlFGRXc1aHc"),
    ("deltas29000.zip", "0B4qLcYyJmiz0U1pnMEI4WXN1S3M"),
    ("image_list.txt", "0B4qLcYyJmiz0U25vdEVIU3NvNFk")
]


def download_celeb_a_hq_delta_files(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    for fname, id in _CELEB_A_HQ_DELTA_FILES:
        fpath = str(output_dir / fname)
        download_file_from_google_drive(id, fpath)
        unzip(fpath)
