import os
import json

from pyrsistent import freeze


def load_stopwords():
    """
    Loads the stopwords from stopwords.json

    :return:
    """
    data_path = os.path.join(os.path.dirname(__file__), 'stopwords')
    stopwords = {}
    with open(os.path.join(data_path, "stopwords.json"), encoding="utf-8") as json_file:
        data = json.load(json_file)
        for language, file_name in data.items():
            with open(os.path.join(data_path, file_name), encoding="utf-8") as file:
                stopwords[language] = json.load(file)
    return stopwords


_STOPWORDS = load_stopwords()
STOPWORDS = freeze(_STOPWORDS)
