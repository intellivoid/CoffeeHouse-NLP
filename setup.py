import os
from setuptools import setup, find_packages

# Find all the stopwords data files
stopwords_file_path = os.path.join('coffeehouse_nlp', 'multi_rake', 'stopwords')

stopwords_files_fetch = os.listdir(os.path.join(os.getcwd(), stopwords_file_path))
stopwords_files = []
for file in stopwords_files_fetch:
    file_path = os.path.join(os.getcwd(), stopwords_file_path, file)
    if not os.path.isdir(file_path):
        stopwords_files.append(file_path)

setup(
    name='coffeehouse_nlp',
    version='1.0.0',
    description='CoffeeHouse Natural Language Processing engine',
    url='https://github.com/Intellivoid/CoffeeHouse-NLP',
    author='Zi Xing Narrakas',
    author_email='netkas@intellivoid.net',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Text Processing',
        'Programming Language :: Python :: 3',
    ],
    keywords='nlp natural language processing',
    data_files=[
        (os.path.join('coffeehouse_nlp', 'multi_rake', 'stopwords'), stopwords_files)
    ],
    install_requires=[
        'nltk',
        'numpy',
        'pyrsistent',
        'cld2-cffi',
        'wikipedia',
        'requests',
        'bs4'
    ],
    packages=find_packages()
)
