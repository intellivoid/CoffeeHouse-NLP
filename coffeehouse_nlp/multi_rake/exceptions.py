import sys


class UnsupportedLanguage(Exception):
    """Unsupported Language exception class."""

    def __init__(self, error, language_code):
        self.error = error
        self.language_code = language_code

    def __unicode__(self):
        return "{0}, detected language: {1}".format(self.error, self.language_code)

    if sys.version_info > (3, 0):
        def __str__(self):
            return self.__unicode__()

    else:
        def __str__(self):
            return self.__unicode__().encode('utf8')


class InvalidInput(Exception):
    """Unsupported Language exception class."""

    def __init__(self, error):
        self.error = error

    def __unicode__(self):
        return self.error

    if sys.version_info > (3, 0):
        def __str__(self):
            return self.__unicode__()

    else:
        def __str__(self):
            return self.__unicode__().encode('utf8')


class LanguagePredictionFailure(Exception):
    """Language Prediction Failure class."""

    def __init__(self, error):
        self.error = error

    def __unicode__(self):
        return self.error

    if sys.version_info > (3, 0):
        def __str__(self):
            return self.__unicode__()

    else:
        def __str__(self):
            return self.__unicode__().encode('utf8')
