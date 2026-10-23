#!/usr/bin/env python3

## @file
#
#
## @author
## @date

##########################################################################
import argparse
from warnings import simplefilter
from datetime import datetime

import pandas as pd
# ignore pandas "educational" performance warnings
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
from dask.distributed import Client
from crocolaketools.config import config_paths as cfgp
from crocolaketools.converter.converterEMOLT import ConverterEMOLT

import functools
print = functools.partial(print, flush=True)
##########################################################################

def eMOLT2parquet(eMOLT_path=None, outdir_pqt=None, fname_pq=None, use_config_file=None):

    client = Client(**cfgp.get_config_cluster_db_dict("EMOLT"))

    if not use_config_file:
        print("Using user-defined configuration")
        config = {
            'db': 'eMOLT',
            'db_type': 'PHY',
            'input_path': eMOLT_path,
            'outdir_pq': outdir_pqt,
            'outdir_schema': './schemas/eMOLT/',
            'fname_pq': fname_pq,
            'add_derived_vars': False,
            'overwrite': False,
        }
        ConverterPHY = ConverterEMOLT(config)

    else: # reads from file
        print("Using configuration from datasets.yaml")
        ConverterPHY = ConverterEMOLT()
    print("Converting PHY files to parquet...")
    ConverterPHY.convert()
    print("PHY files converted to parquet.")
    del ConverterPHY
    print("done.")

    client.shutdown()

    return

##########################################################################
def main():
    parser = argparse.ArgumentParser(description='Script to convert eMOLT database to parquet')
    parser.add_argument('-i', help="Path to eMOLT data", required=False)
    parser.add_argument('-o', help="Destination path for parquet format database", required=False)
    parser.add_argument("-f", help="Basename for output files", required=False, default="demo_eMOLT.parquet")
    parser.add_argument('--config', action='store_true', help="Use config files instead of parsing arguments", required=False, default=None)


    cfgp.add_config_dir_argument(parser)
    args = parser.parse_args()

    cfgp.apply_config_dir_argument(args)

    eMOLT2parquet(args.i, args.o, args.f, args.config)

##########################################################################
if __name__ == "__main__":
    print(datetime.now())
    print()
    main()
    print("eMOLT2parquet.py executed successfully")
    print()
    print(datetime.now())
    print(" ")