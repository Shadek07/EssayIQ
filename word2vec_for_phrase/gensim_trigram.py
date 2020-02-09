
import re
from spacy.lang.en.stop_words import STOP_WORDS
from gensim.models.phrases import Phrases, Phraser
from gensim.models import Word2Vec
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

wiki_file_name = "wiki_bigram.txt"
def get_sentences(input_file_pointer):
    while True:
        line = input_file_pointer.readline()
        if not line:
            break
        yield line


def clean_sentence(sentence):
    sentence = sentence.lower().strip()
    sentence = re.sub(r'[^a-z0-9_\s]', '', sentence) #keep character '_' as it is part of phrase
    return re.sub(r'\s{2,}', ' ', sentence)


def tokenize(sentence): #tokenization + lemmatization + removing all words containing only digits
    return [lemmatizer.lemmatize(token) for token in sentence.split() if ((token not in STOP_WORDS)
                                                                          and (not token.isdigit()))]

def build_phrases(sentences):
    phrases = Phrases(sentences,
                      min_count=8, threshold=0.2, max_vocab_size=800000, delimiter=b'_', scoring='npmi',
                      progress_per=1000)
    return Phraser(phrases)

def sentence_to_bi_grams(phrases_model, sentence):
    return ' '.join(phrases_model[sentence])

class MyCorpus(object):
    """An interator that yields sentences (lists of str)."""
    def __iter__(self):
        input_file_pointer = open(wiki_file_name, 'r') #bigram file
        while True:
            line = input_file_pointer.readline()
            if not line:
                break
            cleaned_sentence = clean_sentence(line)
            tokenized_sentence = tokenize(cleaned_sentence)
            yield tokenized_sentence

sentences = MyCorpus()
phrases_model = build_phrases(sentences)
phrases_model.save('tri_phrases_model.txt')

#phrases_model = Phraser.load('phrases_model.txt')
print('phrase model done')

def sentences_to_bi_grams(phrases_model, input_file_name, output_file_name):
    with open(input_file_name, 'r') as input_file_pointer:
        with open(output_file_name, 'w+') as out_file:
            for sentence in get_sentences(input_file_pointer):
                #cleaned_sentence = clean_sentence(sentence)
                tokenized_sentence = tokenize(sentence)
                parsed_sentence = sentence_to_bi_grams(phrases_model, tokenized_sentence)
                out_file.write(parsed_sentence + '\n')

sentences_to_bi_grams(phrases_model, wiki_file_name, "wiki_trigram.txt")
print('wiki_trigram done')
class MyTrigramCorpus(object):
    """An interator that yields sentences (lists of str)."""
    def __iter__(self):
        input_file_pointer = open("wiki_trigram.txt", 'r')
        while True:
            line = input_file_pointer.readline()
            if not line:
                break
            #cleaned_sentence = clean_sentence(line)
            tokenized_sentence = tokenize(line)
            yield tokenized_sentence
#use processed bigram to train word2Vec

'''trigram_sentences = MyTrigramCorpus()
model = Word2Vec(trigram_sentences, size=50, window=10, min_count=8, workers=20, iter=10)

words = list(model.wv.vocab)
print(len(words))
with open("wiki_trigram_50d.txt", "w") as out_file:
  for word in words:
    out_file.write(word)
    a = model[word]
    for value in a:
      out_file.write(" " + "%.4f"% value)
    out_file.write('\n')
model.save("wiki_trigram_w2v.model")
print('wordvec model done')'''

'''print(model.similar_by_word('drama_film', 5))
model = Word2Vec.load("wiki_trigram_w2v.model")
words = list(model.wv.vocab)
print(len(words))
#print(model.similar_by_word('drama_film', 5))'''