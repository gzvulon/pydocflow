import numpy as np
import pandas as pd
import pyarrow as pa


def main():
    df = pd.DataFrame(
        {
            'one': [-1, np.nan, 2.5],
            'two': ['foo', 'bar', 'baz'],
            'three': [True, False, True]
        },
        index=list('abc'))
    table = pa.Table.from_pandas(df)
    print(table)


def entrypoint():
    import fire
    fire.Fire(main)


if __name__ == "__main__":
    entrypoint()
