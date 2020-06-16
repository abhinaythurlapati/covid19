import yaml
from os import path, mkdir
import logging
import multiprocessing_logging
import pandas as pd

# get the current directory where this __init__.py resides
cur_dir = path.dirname(path.realpath(__file__))
config_file_path = path.join(cur_dir, "config\\config.yml")

if not path.isfile(config_file_path):
    raise FileNotFoundError("{}".format(config_file_path))

with open(config_file_path) as f:
    config = yaml.load(f, Loader=yaml.Loader)

data_dir_paths = [path.join(config['data_dir'], data_sub_dir) for data_sub_dir in config['data_sub_dirs']]

metadata_path = path.join(config['data_dir'], config['metadata'])
cord_19_embeddings_path = path.join(config['data_dir'], config['covid_word_embeddings'])
results_data_path = path.join(config['results_data'], '')
target_tables_unsorted_dir_path = path.join(config['target_tables_unsorted_data_dir'], '')
target_tables_dir_path = path.join(config['target_tables_data_dir'], '')
key_scientific_questions_dir_path = path.join(config['target_tables_unsorted_data_dir'],
                                              config['target_tables_unsorted_data_sub_dir'][0])
risk_factors_dir_path = path.join(config['target_tables_unsorted_data_dir'],
                                  config['target_tables_unsorted_data_sub_dir'][1])


inverted_index_dir = path.join(results_data_path, 'inverted_indexes')
if not path.isdir(inverted_index_dir):
    try:
        mkdir(inverted_index_dir)
    except OSError:
        print("Creation of the directory {} failed".format(inverted_index_dir))

vocabulary_dir = path.join(results_data_path, 'vocabulary')
if not path.isdir(vocabulary_dir):
    try:
        mkdir(vocabulary_dir)
    except OSError:
        print("Creation of the directory {} failed".format(vocabulary_dir))


# logging definintions
logging.basicConfig(
    filename= path.join(config['logs_dir','pytonic.log']),
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(process)s %(module)s %(funcName)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p"
)
multiprocessing_logging.install_mp_handler()
logger = logging.getLogger('dev')

total_files = 65000
