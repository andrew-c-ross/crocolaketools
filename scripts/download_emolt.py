#!/usr/bin/env python3

#
#
## @author
#
# @date

import argparse
from datetime import datetime

from crocolaketools.config import config_paths as cfgp
from crocolaketools.downloader.downloaderEMOLT import DownloaderEMOLT


def download_eMOLT(
    config: dict = None,
    overwrite: bool = False,
) -> None:
    """Download eMOLT file using DownloaderEMOLT.

    Parameters
    ----------
    config    : configuration dict passed to DownloaderEMOLT.
                Must contain at least 'db' and 'db_type'.
                Defaults to {'db': 'eMOLT', 'db_type': 'PHY'}.
    overwrite : re-download even if file already exists.
    """
    downloader = DownloaderEMOLT(
        config=config,
        overwrite=overwrite,
    )
    downloader.eMOLT_download()


#------------------------------------------------------------------------------#
def main():
    parser = argparse.ArgumentParser(
        description="Download eMOLT parquet files from ERDDAP."
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="Re-download even if file already exists on disk",
    )
    parser.add_argument(
        "--config",
        action="store_true",
        default=False,
        help="Use datasets.yaml defaults for input_path instead of CLI arguments",
    )


    cfgp.add_config_dir_argument(parser)
    args = parser.parse_args()

    cfgp.apply_config_dir_argument(args)

    # when --config is passed, let DownloaderEMOLT read input_path from
    # datasets.yaml; otherwise use the default {'db': 'eMOLT', 'db_type': 'PHY'}
    config = None if args.config else {'db': 'eMOLT', 'db_type': 'PHY'}

    download_eMOLT(
        config=config,
        overwrite=args.overwrite,
    )

##########################################################################

if __name__ == "__main__":
    print(datetime.now())
    print()
    main()
    print("download_emolt.py executed successfully")
    print()
    print(datetime.now())
    print(" ")
