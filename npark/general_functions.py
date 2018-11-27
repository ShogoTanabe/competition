import pandas as pd
import numpy as np


def read_tsv(file_path, _encoding="utf-8"):
  df = pd.read_csv(file_path, index_col=0, sep="\t", encoding=_encoding)
  print(df.shape)
  return df

