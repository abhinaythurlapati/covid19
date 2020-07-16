from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.util import ngrams
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, SnowballStemmer
import re


class DataPreProcessing:
    stopwords = set(stopwords.words('english'))
    snowball_stemmer = SnowballStemmer('english')
    porter_stemmer = PorterStemmer()

    def __init__(self, data, columns):
        """
        returns a data frame object
        """
        if not isinstance(data, list):
            raise TypeError('kw_arg "data" is not of type list')

        if not isinstance(columns, list):
            raise TypeError('kw_arg "columns" is not of type list')

        # return pd.DataFrame(data=data, columns=self.columns)
        pass

    @staticmethod
    def word_tokenizer(document, to_lower=True):
        if to_lower not in [True, False]:
            raise ValueError('kw_arg:"to_lower" has to be one of "True", "False"')
        if isinstance(document, str):
            return word_tokenize(text=document)
        if isinstance(document, list):
            word_tokenized = list()
            for doc in document:
                tokenized = word_tokenize(text=doc)
                if to_lower:
                    tokenized = [word.lower() for word in tokenized]
                word_tokenized.extend(tokenized)

            return word_tokenized

    @staticmethod
    def sentence_tokenizer(document):
        if isinstance(document, str):
            return sent_tokenize(document)
        if isinstance(document, list):
            doc_tokenized = list()
            for section in document:
                tokenized = sent_tokenize(text=section)
                doc_tokenized.extend(tokenized)

            return doc_tokenized

    @staticmethod
    def word_counts(document, remove_special_chars= False, remove_stop_words= False, remove_hyperlinks=False,
                    remove_numbers=False, remove_chars_by_length=False, remove_char_length=2):
        """
        returns a dict having keys as words and values as word_counts
        :param remove_hyperlinks:
        :param remove_stop_words:
        :param remove_special_chars:
        :param document:
        :return:
        """
        word_count_dict = dict()
        if isinstance(document, str) or isinstance(document, list):
            sentences = DataPreProcessing.sentence_tokenizer(document=document)
            words = DataPreProcessing.word_tokenizer(document=sentences)

            if remove_hyperlinks:
                words = DataPreProcessing.remove_hyperlinks(words=words)

            if remove_special_chars:
                words = DataPreProcessing.remove_special_chars(words=words)

            if remove_stop_words:
                words = DataPreProcessing.remove_stop_words(words=words)

            if remove_numbers:
                words = DataPreProcessing.remove_numbers(words=words)

            if remove_chars_by_length:
                words = DataPreProcessing.remove_by_length(words=words, length=remove_char_length)

            for word in words:
                if word not in word_count_dict:
                    word_count_dict[word] = 1
                else:
                    word_count_dict[word] += 1

        return word_count_dict

    @staticmethod
    def unique_words(document):
        if isinstance(document, str) or isinstance(document, list):
            sentences = DataPreProcessing.sentence_tokenizer(document=document)
            words = DataPreProcessing.word_tokenizer(document=sentences)
            return list(set(words))

    @staticmethod
    def generate_ngrams(document, grams=2):
        if isinstance(document, str) or isinstance(document, list):
            sentences = DataPreProcessing.sentence_tokenizer(document=document)
            words = DataPreProcessing.word_tokenizer(document=sentences)
            return list(ngrams(words, grams))

    @staticmethod
    def get_stopwords():
        """
        :returns a set of stopwords as defined by nltk corups
        """
        return DataPreProcessing.stopwords

    @staticmethod
    def extend_stopwords(stop_words):
        """
        extends the existing stop words and returns the newly formed extended list of stop words
        :param stop_words:
        :return:
        """
        if isinstance(stop_words, str):
            DataPreProcessing.stopwords.add(stop_words)
        if isinstance(stop_words, list):
            kw_arg_stop_words = set(stop_words)
            DataPreProcessing.stopwords.union(kw_arg_stop_words)
        return list(DataPreProcessing.stopwords)

    @staticmethod
    def remove_stop_words(words=None, sentences=None):
        """
        removes the stop words defined in the vocabulary.
        either words or sentences should have values but not both
        :param words: list of words
        :param sentences: list of sentences or single sentence
        :return:
        """
        if words is not None and sentences is not None:
            raise AssertionError("Only one of kw_args: words or sentences should be present; but not both")

        if words is None and sentences is None:
            raise TypeError('parameters for kw_arg: "words" or "sentences" is not supplied')

        if words and not isinstance(words, list):
            raise ValueError("kw_arg: words accepts only list type")

        if sentences and not (isinstance(sentences, str) or isinstance(sentences, list)):
            raise ValueError("{kw_arg: 'sentences' should be one of 'str' or 'list'}")

        stop_words = DataPreProcessing.stopwords
        if words:
            words_set = set(words)
            return list(words_set.difference(stop_words))

        if sentences and isinstance(sentences, str):
            tokenized_words = sentences.split()
            return ' '.join([word for word in tokenized_words if word not in stop_words])

        if isinstance(sentences, list):
            filtered_sentences = list()
            for sentence in sentences:
                tokenized_words = sentence.split(' ')
                updated_sentence = ' '.join([word for word in tokenized_words if word not in stop_words])
                filtered_sentences.append(updated_sentence)
            return filtered_sentences

    @staticmethod
    def remove_numbers(words):
        """
        Accepts a list of words and removes the numbers i.e 1, 2 , 300 etc from it
        :param words:
        :return: list of removed numbers
        """

        if words is None:
            return list()

        if not isinstance(words, list):
            raise TypeError('kw_arg "words" should be of type list')

        return [word for word in words if not word.isdigit()]

    @staticmethod
    def remove_by_length(words, length=2):
        """
        returns the words that have the length greater than 'length' argument
        :return:
        """
        if not isinstance(words, list):
            raise TypeError('kw_arg "words" should be of type list')

        if length < 0:
            raise ValueError('kw_arg: "length" should be non negative')
        return [word for word in words if len(word) > length]

    @staticmethod
    def remove_special_chars(words):
        """
        :param words: list of words/ word string
        :param remove_numbers: boolean value indicating
        :returns: the list of words after removing special chars
        """
        match = re.compile(r"(?![-'])[a-zA-Z0-9-']+(?<!['-])")
        filtered_words = list()
        for word in words:
            match_obj = match.search(word)
            if match_obj is not None:
                truncated_word = match_obj.group()
                filtered_words.append(truncated_word)
        return filtered_words

    @staticmethod
    def remove_hyperlinks(words):
        """
        takes list of words or word as the input
        :param words: list or string
        :return: removes the hyperlink and replace it with ''
        """
        filtered_words = list()
        for word in words:
            filtered_word = re.sub(r'https?://.*[\r\n\s$]*', '', word)
            if filtered_word is not None and filtered_word != '':
                filtered_words.append(filtered_word)
        return filtered_words

    @staticmethod
    def get_synonyms(word):
        """
        returns the list of synonyms of a word as per wordnet corpus
        :param word: valid english word
        :return: list of synonyms
        """
        if not isinstance(word, str):
            raise ValueError('kw_arg: word should be of "str" type')

        synonyms = [synonym.name() for syn in wordnet.synsets(word) for synonym in syn.lemmas()]
        return list(set(synonyms))

    @staticmethod
    def stemmer(words):
        """
        returns the root of the word used to index or stem
        :param words:
        :return:
        """
        if words is None:
            return []

        if len(words) == 0:
            return []

        if not isinstance(words, list):
            raise TypeError("kw_arg: 'words' should be of type 'list' ")

        return [DataPreProcessing.snowball_stemmer.stem(word) for word in words]

    @staticmethod
    def clean_text(text='', remove_char_length=2):
        if not isinstance(text, str):
            raise TypeError('kw_arg: "text" is not of type "str"')

        tokens = DataPreProcessing.word_tokenizer(document=text, to_lower=True)
        filtered_words = DataPreProcessing.remove_hyperlinks(tokens)
        processed_words = DataPreProcessing.remove_special_chars(filtered_words)
        filtered_words = DataPreProcessing.remove_numbers(processed_words)
        filtered_words = DataPreProcessing.remove_by_length(filtered_words, length=remove_char_length)
        filtered_words = DataPreProcessing.remove_stop_words(words=filtered_words)
        stemmed_words = DataPreProcessing.stemmer(filtered_words)
        return stemmed_words


class VocabularyBuilder(DataPreProcessing):
    corpus_vocabulary = set()

    @staticmethod
    def add_to_vocab(words: object):
        if isinstance(words, str):
            words_set = set(list(words))

        if isinstance(words, list):
            words_set = set(words)

        VocabularyBuilder.corpus_vocabulary = VocabularyBuilder.corpus_vocabulary.union(words_set)

    @staticmethod
    def remove_from_vocab(words):
        if not isinstance(words, list):
            raise ValueError('kw_arg "words" is not of type "list"')

        words_set = set(words)
        VocabularyBuilder.corpus_vocabulary = VocabularyBuilder.corpus_vocabulary.difference(words_set)

    @staticmethod
    def get_vocab():
        return list(VocabularyBuilder.corpus_vocabulary)

