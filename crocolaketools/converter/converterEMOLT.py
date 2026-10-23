import dask.dataframe as dd
import pandas as pd
from gsw import p_from_z
from .converter import Converter

class ConverterEMOLT(Converter):

    def __init__(self, config=None):
        Converter.__init__(self, config or {'db': 'eMOLT', 'db_type': 'PHY'})
        # derived variables (SA, CT, sigma1) need PSAL, which eMOLT lacks
        if self.add_derived_vars:
            raise ValueError("eMOLT has no salinity: set add_derived_vars to False.")

    def read_to_ddf(self, flist=None, lock=None):
        df = pd.concat(pd.read_parquet(self.input_path / f) for f in flist)
        # temporary
        df = df.loc[df.depth >= 0, :]
        df['PRES'] = p_from_z(-df['depth'], df['latitude']).astype('float32')
        df['PLATFORM_NUMBER'] = 0
        df['CYCLE_NUMBER'] = 0
        df = self.standardize_data(df)
        df = self.add_qc_flags(df, ['TEMP', 'PRES'], 1)
        return dd.from_pandas(df, npartitions=4)