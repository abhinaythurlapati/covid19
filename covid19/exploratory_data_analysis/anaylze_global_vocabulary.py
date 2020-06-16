from covid19 import results_data_path
import pandas as pd
from os import path

global_vocab_df = pd.read_csv(path.join(results_data_path, 'global_vocabulary.csv'), index_col=[0])
global_vocab_df['vocab'].str.sort_values

print(global_vocab_df)