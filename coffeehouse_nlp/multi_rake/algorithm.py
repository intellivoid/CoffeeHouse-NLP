import operator
import numpy as np

from collections import Counter, defaultdict

from coffeehouse_nlp.multi_rake.exceptions import UnsupportedLanguage, InvalidInput, LanguagePredictionFailure
from coffeehouse_nlp.multi_rake.stopwords import STOPWORDS
from coffeehouse_nlp.multi_rake.utils import (
    detect_language, keep_only_letters, separate_words, split_sentences,
)


class Rake:
    """Multi-Rake Method"""
    def __init__(self, min_chars=3, max_words=3, min_freq=1,
                 language_code=None, stopwords=None, lang_detect_threshold=50,
                 max_words_unknown_lang=2, generated_stopwords_percentile=80,
                 generated_stopwords_max_len=3, generated_stopwords_min_freq=2):
        """
        Public Constructor

        :param min_chars:
        :param max_words:
        :param min_freq:
        :param language_code:
        :param stopwords:
        :param lang_detect_threshold:
        :param max_words_unknown_lang:
        :param generated_stopwords_percentile:
        :param generated_stopwords_max_len:
        :param generated_stopwords_min_freq:
        """
        self.min_chars = min_chars
        self.max_words = max_words
        self.min_freq = min_freq
        self.lang_detect_threshold = lang_detect_threshold
        self.max_words_unknown_lang = max_words_unknown_lang
        self.generated_stopwords_percentile = generated_stopwords_percentile
        self.generated_stopwords_max_len = generated_stopwords_max_len
        self.generated_stopwords_min_freq = generated_stopwords_min_freq

        if language_code is not None and language_code not in STOPWORDS:
            raise UnsupportedLanguage(
                "There are no built-in stopwords for {0}.".format(language_code), language_code)

        if stopwords is not None:
            self.stopwords = stopwords
        else:
            self.stopwords = STOPWORDS.get(language_code, set())

    def extract_keywords(self, text_input, language_code=None):
        """
        Extracts keywords from a text, if the language_code is
        set to None, it will attempt to predict the language

        :param language_code:
        :param text_input:
        :return:
        """
        text_input = text_input.lower()
        max_words = self.max_words

        if language_code is None:
            language_code = detect_language(text_input, self.lang_detect_threshold)

        if self.stopwords:
            stop_words = self.stopwords

        else:
            if language_code is None:
                raise LanguagePredictionFailure("The given text input cannot be processed")
            else:
                if language_code["language_code"] in STOPWORDS:
                    stop_words = STOPWORDS[language_code["language_code"]]
                else:
                    raise UnsupportedLanguage(
                        "There are no built-in stopwords for {0}.".format(language_code), language_code)
                    # noinspection PyUnreachableCode
                    """if text_for_stopwords:
                        text_for_stopwords = text_for_stopwords.lower()
                        text_for_stopwords = ' '.join([text, text_for_stopwords])
                    else:
                        text_for_stopwords = text
    
                    stop_words = self._generate_stop_words(text_for_stopwords)
    
                    if self.max_words_unknown_lang is not None:
                        max_words = self.max_words_unknown_lang"""

        if language_code is None:
            raise InvalidInput("The given text input cannot be processed")

        phrase_list = self._generate_candidate_keywords(
            split_sentences(text_input),
            stop_words,
            max_words,
        )

        keywords = self._generate_candidate_keyword_scores(
            phrase_list,
            Rake._calculate_word_scores(phrase_list),
        )

        keywords = sorted(
            keywords.items(),
            key=operator.itemgetter(1),
            reverse=True,
        )

        dict_keywords = []

        for item in keywords:
            item = list(item)
            dict_keywords.append({
                "keyword": item[0],
                "scores": item[1]
            })

        return {
            "language_detection": language_code,
            "keywords": dict_keywords
        }

    def _generate_stop_words(self, text):
        """
        Generates stop words from text
        :param text:
        :return:
        """
        stop_words = set()

        text = keep_only_letters(text)

        if not text:
            return stop_words

        text = text.split()

        word_counts = Counter(text).most_common()
        counts_sample = [word_count[1] for word_count in word_counts]

        upper_bound = np.percentile(
            counts_sample,
            self.generated_stopwords_percentile,
        )

        upper_bound = max(upper_bound, self.generated_stopwords_min_freq)

        for word, count in word_counts:  # pragma: no branch
            if count >= upper_bound:
                if len(word) <= self.generated_stopwords_max_len:
                    stop_words.add(word)
            else:
                break

        return stop_words

    def _generate_candidate_keywords(self, sentence_list, stop_words, max_words):
        """
        Predicts the potential candidates of keywords

        :param sentence_list:
        :param stop_words:
        :param max_words:
        :return:
        """
        result = []
        phrases = []

        for sentence in sentence_list:
            tmp = []

            for word in sentence.split():
                if word in stop_words:
                    if tmp:
                        phrases.append(' '.join(tmp))
                        tmp = []

                else:
                    tmp.append(word)

            if tmp:
                phrases.append(' '.join(tmp))

        for phrase in phrases:
            if (
                    phrase
                    and len(phrase) >= self.min_chars
                    and len(phrase.split()) <= max_words
            ):
                result.append(phrase)

        return result

    def _generate_candidate_keyword_scores(self, phrase_list, word_score):
        """
        Generates the scores for the candidates

        :param phrase_list:
        :param word_score:
        :return:
        """
        keyword_candidates = {}

        for phrase in phrase_list:
            if phrase_list.count(phrase) >= self.min_freq:
                word_list = separate_words(phrase)
                candidate_score = 0

                for word in word_list:
                    candidate_score += word_score[word]

                keyword_candidates[phrase] = candidate_score

        return keyword_candidates

    @staticmethod
    def _calculate_word_scores(phrase_list):
        """
        Calculates the word scores

        :param phrase_list:
        :return:
        """
        word_frequency = defaultdict(int)
        word_degree = defaultdict(int)

        for phrase in phrase_list:
            word_list = separate_words(phrase)
            word_list_length = len(word_list)
            word_list_degree = word_list_length - 1

            for word in word_list:
                word_frequency[word] += 1
                word_degree[word] += word_list_degree

        for item in word_frequency:
            word_degree[item] = word_degree[item] + word_frequency[item]

        word_score = defaultdict(int)

        for item in word_frequency:
            # noinspection PyTypeChecker
            word_score[item] = (word_degree[item] / word_frequency[item])

        return word_score
