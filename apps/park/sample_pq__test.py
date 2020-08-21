import sample_pq


def test_me():
    df = sample_pq.create_sample_dataframe()
    import pyarrow
    print(type(df))
    assert type(df) == pyarrow.lib.Table

