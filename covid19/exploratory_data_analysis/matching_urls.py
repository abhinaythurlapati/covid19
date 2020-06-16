"""
The aim of this program is to look for matching documents based on urls to understand the source of data in the target tables
"""

from covid19 import metadata_path, target_tables_unsorted_dir_path
from os import path, walk, listdir
import pandas as pd
from covid19.definitions.columns import Columns
import inspect, re

def varname(p):
  for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
    m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
    if m:
      return m.group(1)


def compare_sets(set1_name, set1, set2_name, set2):
    print('Length of {} is {}'.format(set1_name, len(set1)))
    print('Length of {} is {}'.format(set2_name, len(set2)))
    common_values = set1.intersection(set2)
    print('{} common values found in {} and {}'.format(len(common_values), set1_name, set2_name))

    set1_only = set1.difference(set2)
    print('{} values in present in {} but not in {}'.format(len(set1_only), set1_name, set2_name))

    set2_only = set2.difference(set1)
    print('{} values in present in {} but not in {}'.format(len(set2_only), set2_name, set1_name))


#  load the title and url columns from the metadata.csv
metadata_df = pd.read_csv(metadata_path, usecols=[3, 17])
metadata_columns = metadata_df.columns
n_rows_metadata = metadata_df.shape[0]
print("number of rows in metadata: {}".format(n_rows_metadata))

# lists to store the urls in all the files in the unsorted data directory
risk_factors_urls = list()
risk_factors_title = list()
qa_study_link = list()
qa_studies = list()

for root_dir, dirs, files in walk(target_tables_unsorted_dir_path):

    for f_name in files:
        file_path = path.join(root_dir, f_name)
        df = pd.read_csv(file_path)
        df_columns = df.columns

        if Columns.study_link in df_columns:
            qa_study_link.extend(df[Columns.study_link].values.tolist())

        if Columns.url in df_columns:
            risk_factors_urls.extend(df[Columns.url].values.tolist())

        if Columns.title in df_columns:
            risk_factors_title.extend(df[Columns.title].values.tolist())

        if Columns.study in df_columns:
            qa_studies.extend(df[Columns.study].values.tolist())


# convert metadata title and url columns to set
metadata_urls_set = set(metadata_df['url'].values.tolist())
metadata_title_set = set(metadata_df['title'].values.tolist())


compare_sets(set1_name=varname(qa_studies), set1=set(qa_studies),
             set2_name=varname(metadata_title_set), set2=metadata_title_set)


print('comparing urls')
compare_sets(set1_name=varname(qa_study_link), set1=set(qa_study_link),
             set2_name=varname(metadata_urls_set), set2=metadata_urls_set)



print('comparing titles')
compare_sets(set1_name=varname(risk_factors_title), set1=set(risk_factors_title),
             set2_name=varname(metadata_title_set), set2=metadata_title_set)


print('comparing urls')
compare_sets(set1_name=varname(risk_factors_urls), set1=set(risk_factors_urls),
             set2_name=varname(metadata_urls_set), set2=metadata_urls_set)

