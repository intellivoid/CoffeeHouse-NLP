import cld2
import regex

LETTERS_RE = regex.compile(r'\p{L}+')

SENTENCE_DELIMITERS_RE = regex.compile(
    r'[\.,;:¡!¿\?…⋯‹›«»\\"“”\[\]\(\)⟨⟩}{&]'  # any punctuation sign or &
    r'|\s[-–~]+\s',  # or '-' between spaces
    regex.VERBOSE,
)


def detect_language(text, proba_threshold):
    """
    Detects the language from a text

    :param text:
    :param proba_threshold:
    :return:
    """
    _, _, details = cld2.detect(text)

    language_code = details[0].language_code
    probability = details[0].percent

    if language_code != 'un' and probability > proba_threshold:
        return {
            "language_name": details[0].language_name,
            "language_code": details[0].language_code,
            "confidence": details[0].percent,
            "score": details[0].score
        }


def keep_only_letters(string):
    """ Returns the string with only letters """
    return ' '.join(token.group() for token in LETTERS_RE.finditer(string))


def separate_words(text):
    """ Separates the words into a list (Tokenize) """
    words = []

    for word in text.split():
        if not word.isnumeric():
            words.append(word)

    return words


def split_sentences(text):
    """ Splits sentences into a list """
    sentences = SENTENCE_DELIMITERS_RE.split(text)
    return sentences
