## Word2vec for Phrases

In general, word2vec does not take care of Phrases within a dataset. Therefore, an effort is required to make n-gram dataset before using word2vec for an application that requires to detect phrases.

gensim_bigram.py is for converting any dataset containing sentence data into meaningful bigrams. Similarly, gensim_trigram.py is for extracting meaningful trigrams from the data that came out of gemsim_bigram.py.

Each of these python files (gensim_bigram, gensim_trigram, gensim_4gram) has training of word2vec on the processed n-gram data.

For our purpose we used word2vec training after 4-gram processing at the end of gensim_4gram.py file.
