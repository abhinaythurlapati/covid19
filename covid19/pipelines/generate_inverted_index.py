import pandas as pd
from covid19.lib.objects.researchpaper import ResearchPaper
from covid19.lib.objects.buffer import Buffer
from covid19.lib.objects.inverted_index import InvertedIndex
from covid19.DataManagement.loaddata import LoadData
from covid19.DataManagement.datapreprocessing import DataPreProcessing

from multiprocessing import current_process, Queue, Process
from queue import Empty
from time import time
from covid19 import logger, inverted_index_dir
from os import path


def sentences_producer(queue, data):
    """
    puts the list of sentences or a single sentence in the queue generated by the research paper
    :param queue: queue object
    :param data: data generator object
    :return:
    """
    count = 0
    start_time = time()
    p = current_process()
    logger.info('Running process: {} with pid: {}'.format(p.name, p.pid))
    for datum in data.get_datum():
        count += 1
        if count % 1000 == 0:
            logger.info('Approx: {} files have been processed so far'.format(count))
        rp = ResearchPaper(r_paper=datum)
        sentences = rp.get_r_paper_title()
        uid = rp.get_r_paper_id()
        if sentences is not None and len(sentences) > 0:
            # tuple with first term as uid and second term as sentences
            queue.put((uid, sentences))
    end_time = time()
    logger.info('Exiting process {} with pid: {}'.format(p.name, p.pid))
    logger.info('Process: {} with pid: {} ran for {} seconds'.format(p.name, p.pid, end_time - start_time))


def corpus_to_words_producer(corp_queue, word_queue):
    in_queue = corp_queue
    out_queue = word_queue
    p = current_process()
    start_time = time()
    logger.info('Running process: {} with pid: {}'.format(p.name, p.pid))
    try:
        while True:
            item = in_queue.get(timeout=60)
            uid, corpus = item[0], item[1]
            words_count_dict = DataPreProcessing.word_counts(document=corpus, remove_hyperlinks=True,
                                                             remove_special_chars=True, remove_numbers=True,
                                                             remove_chars_by_length=True, remove_char_length=2,
                                                             remove_stop_words=True)
            out_queue.put((uid, words_count_dict))
            # logger.info('Placed words of size: {} in words queue'.format(len(words)))
    except Empty:
        logger.info('For Process: {} with pid: {} No data found in the corpus queue for the last 60 seconds, '
                    'preparing to terminate'.format(p.name, p.pid))
    end_time = time()
    logger.info('Process: {} with pid: {} ran for {} seconds'.format(p.name, p.pid, end_time - start_time))


def generate_interim_inverted_index(word_queue, result_queue):
    in_queue = word_queue
    buffer = Buffer(max_size=100)
    p = current_process()
    start_time = time()
    logger.info('Running process: {} with pid: {}'.format(p.name, p.pid))
    # store the uid as key and words count as values

    try:
        while True:
            item = in_queue.get(timeout=100)
            try:
                if len(item) != 0:
                    buffer.add(item)
            except OverflowError:
                items_dict = dict()
                for item in buffer.buffer_data:
                    uid = item[0]
                    words_count = item[1]
                    items_dict[uid] = words_count

                InvertedIndex.update_inverted_index(items=items_dict, field='title')
                buffer.clear()
                logger.info('Created inverted_index of size {} in the Process: {} with pid: {}'.format(
                    len(items_dict), p.name, p.pid))
                logger.info('Current size of Intermediate Inverted index is {} in Process {} with pid:{}'.format(
                    InvertedIndex.get_length(), p.name, p.pid))
                logger.info('Placing the inverted index of size {} to results queue'.format(InvertedIndex.get_length()))
                result_queue.put(InvertedIndex.inverted_index)
                InvertedIndex.reset_inverted_index()

    # this block of code is executed if in_queue is empty for 10 seconds
    except Empty:
        items_dict = dict()
        if buffer.size() > 0:
            for item in buffer.buffer_data:
                uid = item[0]
                words_count = item[1]
                items_dict[uid] = words_count

            InvertedIndex.update_inverted_index(items=items_dict, field='title')
            buffer.clear()
            logger.info("No data found in the words_queue for last 100 seconds")
            logger.info("Emptying left over results in the buffer of size {} in Process with pid: {}".format(
                len(items_dict), p.name, p.pid))
            logger.info('Inverted Index is updated with the left over items in the buffer')
            logger.info('Inverted Index of size {} is placed in results queue'.format(InvertedIndex.get_length()))
            result_queue.put(InvertedIndex.inverted_index)
    end_time = time()
    logger.info('Process: {} with pid: {} ran for {} seconds'.format(p.name, p.pid, end_time - start_time))


if __name__ == "__main__":

    corpus_queue = Queue(maxsize=100)
    words_queue = Queue()
    results_queue = Queue(maxsize=10)
    global_inverted_index = InvertedIndex()

    data_gen_process = Process(target=sentences_producer, args=(corpus_queue, LoadData(),), name='sentence producer')

    corpus_to_words_process = [Process(target=corpus_to_words_producer, args=(corpus_queue, words_queue,),
                                       name='corpus to word process') for i in range(5)]
    generate_interim_index_process = [Process(target=generate_interim_inverted_index, args=(words_queue, results_queue,),
                                           name='generate_interim_vocabulary process') for i in range(5)]

    # Starting all Process
    # starting data generation process
    logger.info('Starting {} process having pid {}'.format(data_gen_process.name, data_gen_process.pid))
    data_gen_process.start()
    # starting corpus to word process
    for process in corpus_to_words_process:
        process.daemon = True
        logger.info('Starting {} process having pid {}'.format(process.name, process.pid))
        process.start()

    # starting generate vocabulary process
    for process in generate_interim_index_process:
        process.daemon = True
        logger.info('Starting {} process having pid {}'.format(process.name, process.pid))
        process.start()

    import json

    while any([process.is_alive() for process in corpus_to_words_process]) or results_queue.empty() is False:
        try:
            i_index = results_queue.get(timeout=300)
            logger.info('id of i_index: {}'.format(id(i_index)))
            logger.info('Length of inverted index: {}'. format(global_inverted_index.get_length()))
            logger.info('Length of inverted index about to be merged: {}'.format(len(i_index)))
            global_inverted_index.merge_with_other(i_index, fields='all')
            logger.info('Global Inverted index updated to size: {} after Merging'.format(global_inverted_index.get_length()))

            # update the data frame with the results generated and write to file

        except Empty:
            logger.info("No results found in the  result_queue for the past 300 seconds")
            logger.info('Here is the status of the corpus to words process')
            for process in corpus_to_words_process:
                logger.info("p_id: {}, pid: {}, is_alive:{}".format(process.name, process.pid, process.is_alive()))

    # wait till child process complete
    data_gen_process.join()
    for process in corpus_to_words_process:
        process.join()

    for process in generate_interim_index_process:
        process.join()

    logger.info('Generating inverted indexed pickle file')
    file_path = path.join(inverted_index_dir, 'Inverted_Index_title.pickle')
    InvertedIndex.write_to_file(filename=file_path)
    logger.info('Written inverted index to "{}"'.format(file_path))
