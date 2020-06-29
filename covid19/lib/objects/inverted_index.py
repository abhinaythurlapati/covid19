from collections import defaultdict
from covid19.definitions.json_keys import RPVocab
import pickle
from covid19 import inverted_index_dir, total_files
from os import path
from math import log10

num_docs = total_files


class InvertedIndex:
    """
    inverted index data structure supporting research paper full search
    sample inverted index
    {
      'word_1': {
        'title': {uid_1: word_count_1, uid_2: word_count_2, ...   },
        'abstract': {uid_1: word_count_1, uid_2: word_count_2, ...   },
        'headers': {uid_1: word_count_1, uid_2: word_count_2, ..... },
        'body_text': {uid_1: word_count_1, uid_2: word_count_2, ..... },
        'full_text': {uid_1: word_count_1, uid_2: word_count_2, ..... },
      },
      'word_2': {
        'title': {uid_1: word_count_1, uid_2: word_count_2, ...   },
        'abstract': {uid_1: word_count_1, uid_2: word_count_2, ...   },
        'headers': {uid_1: word_count_1, uid_2: word_count_2, ..... },
        'body_text': {uid_1: word_count_1, uid_2: word_count_2, ..... },
        'full_text': {uid_1: word_count_1, uid_2: word_count_2, ..... },
      }
    }
    """

    inverted_index = defaultdict(dict)
    allowed_field_values = [RPVocab.title, RPVocab.abstract,RPVocab.headers, RPVocab.body_text, RPVocab.full_text]
    inverted_index_file_path = path.join(inverted_index_dir, 'inverted_index.pickle')

    @staticmethod
    def get_length():
        return len(InvertedIndex.inverted_index)

    @staticmethod
    def reset_inverted_index():
        InvertedIndex.inverted_index = defaultdict(dict)

    @staticmethod
    def get_data_structure():
            return {
                RPVocab.title: defaultdict(),
                RPVocab.abstract: defaultdict(),
                RPVocab.headers: defaultdict(),
                RPVocab.body_text: defaultdict(),
                RPVocab.full_text: defaultdict()
            }

    @staticmethod
    def get_result_dict(search_term, search_results):
        return {
            "search_term": search_term,
            "search_results": search_results
        }

    @staticmethod
    def update_inverted_index(items, field):
        """
        items Data structure:
        {
            'unique_id_1' : {'word_1':  'word_count_1', 'word_2':  'word_count_2', 'word_3':  'word_count_3'   },
            'unique_id_2' : {'word_1':  'word_count_1', 'word_2':  'word_count_2', 'word_3':  'word_count_3'   },
            .
            .
        }

        items is a dictionary have unique_id has its key and a list having tuples(word, word_count as its items)
        :param items: data to add, presents like above data structure
        :param field: field in which items should be added to
        :return: updates the class variable inverted index with the items
        """

        if not isinstance(items, dict):
            raise TypeError('kw_arg "items" is not of type dict')

        if not isinstance(field, str):
            raise TypeError('kw_arg "field" is not of type str')

        if field not in InvertedIndex.allowed_field_values:
            raise ValueError('kw_arg field should be one of {}'.format(' '.join(InvertedIndex.allowed_field_values)))

        for uid, data_dict in items.items():
            for word, word_count in data_dict.items():
                if word in InvertedIndex.inverted_index:
                    InvertedIndex.inverted_index[word][field][uid] = word_count
                else:
                    InvertedIndex.inverted_index[word] = InvertedIndex.get_data_structure()
                    InvertedIndex.inverted_index[word][field][uid] = word_count
        return InvertedIndex.inverted_index

    @staticmethod
    def write_to_file(filename=inverted_index_file_path):
        with open(filename, 'wb') as fp:
            pickle.dump(InvertedIndex.inverted_index, fp, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def read_from_file(filename=inverted_index_file_path, update_inverted_index=False):
        with open(filename, 'rb') as fp:
            inverted_index = pickle.load(filename)
            if update_inverted_index:
                InvertedIndex.inverted_index = inverted_index

            return inverted_index

    @staticmethod
    def delete_words(words):
        if not isinstance(words, list):
            raise TypeError('kw_arg "words" is not of type "list"')

        for word in words:
            try:
                del InvertedIndex.inverted_index[word]
            except KeyError:
                print("Key {} not found in Inverted Index".format(word))

    @staticmethod
    def convert_dict_to_tuple(dictionary):
        if not isinstance(dictionary, dict):
            raise TypeError('kw_arg "words" is not of type "dict"')
        return list(dict(dictionary.items()))

    @staticmethod
    def get_matching_documents_ids(search_terms, field=RPVocab.full_text):
        """
        returns a list of dicts  having the below format
        [
        {
            "search_term": "word1",
            "search_results": [(doc_id1, count), (doc_id2, count2) ]
        },
        {
            "search_term2": "word2",
            "search_results": [(doc_id, count), (doc_id2, count2) ]
        }
        ]

        :param search_terms:
        :param field:
        :return:
        """
        if not isinstance(search_terms, list):
            raise TypeError('kw_arg "search_terms" is not of type "list"')

        if not isinstance(field, str):
            raise TypeError('kw_arg "field" is not of type "str"')

        search_results = list()

        for search_term in search_terms:
            term_results = InvertedIndex.convert_dict_to_tuple(InvertedIndex.inverted_index[search_term][field])
            result_dict = InvertedIndex.get_result_dict(search_term=search_term, search_results=term_results)
            search_results.append(result_dict)

        return search_results

    @staticmethod
    def merge_with_other(inverted_index2, fields='all'):
        '''
        This function has bugs
        :param inverted_index2:
        :param fields:
        :return:
        '''
        inverted_index1 = InvertedIndex.inverted_index
        update_dict = {
            RPVocab.title: False,
            RPVocab.abstract: False,
            RPVocab.headers: False,
            RPVocab.body_text: False,
            RPVocab.full_text: False
        }

        if isinstance(fields, str):
            if fields == 'all':
                for key, value in update_dict.items():
                    update_dict[key] = True
            else:
                if fields not in any(update_dict.keys()):
                    raise ValueError('kw_arg "fields" takes one of {} if type is "str"'.format(','.join(update_dict.keys())))

        if isinstance(fields, list):
            for field in fields:
                if field in update_dict.keys():
                    update_dict[field] = True
                else:
                    raise ValueError('kw_arg "fields" takes these values  {} if type is "list"'.format(','.join(update_dict.keys())))

        if InvertedIndex.get_length() == 0:
            InvertedIndex.inverted_index = inverted_index2
            return

        if update_dict[RPVocab.title]:
            for word, word_dict in inverted_index2.items():
                if word in inverted_index1:
                    inverted_index1[word][RPVocab.title].update(inverted_index2[word][RPVocab.title])
                else:
                    InvertedIndex.inverted_index[word] = InvertedIndex.get_data_structure()
                    inverted_index1[word][RPVocab.title].update(inverted_index2[word][RPVocab.title])

        if update_dict[RPVocab.abstract]:
            for word, word_dict in inverted_index2.items():
                if word in inverted_index1:
                    inverted_index1[word][RPVocab.abstract].update(inverted_index2[word][RPVocab.abstract])
                else:
                    InvertedIndex.inverted_index[word] = InvertedIndex.get_data_structure()
                    inverted_index1[word][RPVocab.abstract].update(inverted_index2[word][RPVocab.abstract])

        if update_dict[RPVocab.headers]:
            for word, word_dict in inverted_index2.items():
                if word in inverted_index1:
                    inverted_index1[word][RPVocab.headers].update(inverted_index2[word][RPVocab.headers])
                else:
                    InvertedIndex.inverted_index[word] = InvertedIndex.get_data_structure()
                    inverted_index1[word][RPVocab.headers].update(inverted_index2[word][RPVocab.headers])

        if update_dict[RPVocab.body_text]:
            for word, word_dict in inverted_index2.items():
                if word in inverted_index1:
                    inverted_index1[word][RPVocab.body_text].update(inverted_index2[word][RPVocab.body_text])
                else:
                    InvertedIndex.inverted_index[word] = InvertedIndex.get_data_structure()
                    inverted_index1[word][RPVocab.body_text].update(inverted_index2[word][RPVocab.body_text])

        if update_dict[RPVocab.full_text]:
            for word, word_dict in inverted_index2.items():
                if word in inverted_index1:
                    inverted_index1[word][RPVocab.full_text].update(inverted_index2[word][RPVocab.full_text])
                else:
                    InvertedIndex.inverted_index[word] = InvertedIndex.get_data_structure()
                    inverted_index1[word][RPVocab.full_text].update(inverted_index2[word][RPVocab.full_text])

        InvertedIndex.inverted_index = inverted_index1


    @staticmethod
    def get_topN_matching_docs(search_results, top_N=5):
        """
        {
          "doc_id1": score
          "doc_id2":

        }
        :param search_results:
        :return:
        """
        scores_dict = dict()

        for word_doc in search_results:
            word_search_results = word_doc['search_results']
            for word_search_result in word_search_results:
                doc_id, term_frequency = 1 + log10(word_search_result[0]), word_search_result[1]
                inverse_document_frequency = log10(num_docs/len(word_search_results))
                tf_idf_score = round(term_frequency*inverse_document_frequency, 3)
                if doc_id in scores_dict:
                    scores_dict[doc_id] += tf_idf_score
                else:
                    scores_dict[doc_id] = tf_idf_score

        sorted_doc_ids = sorted(scores_dict.items(), key=lambda kv: kv[1], reverse=True)
        # returns sorted scores in desc order
        # [('doc_id, score'),('doc_id1, score1'),('doc_id2, score2')]
        return sorted_doc_ids[:top_N] if top_N > len(sorted_doc_ids) else sorted_doc_ids
