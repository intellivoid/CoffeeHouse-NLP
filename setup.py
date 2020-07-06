from setuptools import setup, find_packages

setup(
    name='coffeehouse_nlp',
    version='1.0.0',
    description='CoffeeHouse Natural Language Processing engine',
    url='https://github.com/Intellivoid/CoffeeHouse-NLP',
    author='Zi Xing Narrakas',
    author_email='netkas@intellivoid.info',
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Topic :: Text Processing',
        'Programming Language :: Python :: 3',
    ],
    keywords='nlp natural language processing',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'nltk',
        'wikipedia'
        'requests',
        'bs4'
        'coffeehousemod_tokenizer',
        'coffeehousemod_stopwords'
    ]
)
