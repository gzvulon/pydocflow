import numpy as np
import pandas as pd
import pyarrow as pa

if __name__ == "__main__":
    df = pd.DataFrame({'one': [-1, np.nan, 2.5],

                    'two': ['foo', 'bar', 'baz'],

                    'three': [True, False, True]},

                    index=list('abc'))
    table = pa.Table.from_pandas(df)