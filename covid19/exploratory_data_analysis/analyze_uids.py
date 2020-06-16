from covid19 import metadata_path, cord_19_embeddings_path, results_data_path
import pandas as pd
from os import path

print(metadata_path)
print(cord_19_embeddings_path)

metadata_df = pd.read_csv(metadata_path, low_memory=False, usecols=[0])

# readonly the uid column as the file size is huge
cord_19_embeddings_df = pd.read_csv(cord_19_embeddings_path, usecols=[0], header=None, names=['hash'])

print(metadata_df.shape)
print(cord_19_embeddings_df.shape)

print(metadata_df.head())
print(cord_19_embeddings_df.head())

metadata_uid_set = set(metadata_df['cord_uid'])
cord_19_embeddings_set = set(cord_19_embeddings_df['hash'])

common_uid = metadata_uid_set.intersection(cord_19_embeddings_set)
metadata_only_uid = metadata_uid_set.difference(cord_19_embeddings_set)
cord_19_embeddings_only_uid = cord_19_embeddings_set.difference(metadata_uid_set)

"""
common_uid_df = pd.DataFrame({'uid': list(common_uid)})
metadata_only_uid_df = pd.DataFrame({'uid': list(metadata_only_uid)})
cord_19_embeddings_only_uid_df = pd.DataFrame({'uid': list(cord_19_embeddings_only_uid)})

common_uid_df.to_csv(path.join(results_data_path, 'common_uids.csv'))
metadata_only_uid_df.to_csv((path.join(results_data_path, 'metadata_only_uids.csv')))
cord_19_embeddings_only_uid_df.to_csv(path.join(results_data_path, 'cord_19_embeddings_only.csv'))
"""

# add new 'label'  based on uids
# c - common uids
# m - metadata data only


metadata_df = pd.read_csv(metadata_path, low_memory=False, index_col=[0])

common_metadata_df = metadata_df.loc[list(common_uid)]
common_metadata_df.to_csv(path.join(results_data_path, 'common_metadata.csv'))

metadata_only_df = metadata_df.loc[list(metadata_only_uid)]
metadata_only_df.to_csv(path.join(results_data_path, 'metadata_only.csv'))
