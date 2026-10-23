#!/usr/bin/env python3

#
#
## @author
#
## @date

import time

import requests
from crocolaketools.downloader.downloader import Downloader


EMOLT_URL = 'https://comet.nefsc.noaa.gov/erddap/tabledap/eMOLT_historic_non-realtime_bottom_temperatures.parquet?time%2Clatitude%2Clongitude%2Cdepth%2Csea_water_temperature'


class DownloaderEMOLT(Downloader):
    """class DownloaderEMOLT: methods to download eMOLT
    """

    def __init__(
        self,
        config: dict = None,
        overwrite: bool = False,
    ):
        """Initialize the eMOLT downloader.

        Arguments:
        config    -- configuration dictionary (must contain 'db' and 'db_type').
        overwrite -- if True, re-download files that already exist.
        """
        if config is None:
            config = {
                'db': 'eMOLT',
                'db_type': 'PHY',
            }

        super().__init__(config)
        self.overwrite = overwrite

    def eMOLT_download(self) -> None:
        """Download, skipping files already on disk"""
        start_time = time.time()
        print("Downloading eMOLT...")

        url = self.get_url()
        local_pq_path = self.input_path / 'eMOLT.parquet'


        if self._is_already_downloaded(local_pq_path):
            print(
                f"File already present at {local_pq_path}. "
                "Use overwrite=True or use '--overwrite' flag to force re-download."
            )
        else:
            print(f"Downloading from {url} ...")

            try:
                self._download_file(url, local_pq_path)
                print(f"Saved archive to {local_pq_path}")
            except requests.exceptions.HTTPError as e:
                print(f"Error downloading {local_pq_path}: {e}")

        elapsed_time = time.time() - start_time
        print("done.")
        print("Time to download eMOLT database: " + str(elapsed_time))

    def get_url(self) -> str:
        return EMOLT_URL


if __name__ == "__main__":
    DownloaderEMOLT().eMOLT_download()
