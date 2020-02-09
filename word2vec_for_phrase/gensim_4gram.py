
import re
from spacy.lang.en.stop_words import STOP_WORDS
from gensim.models.phrases import Phrases, Phraser
from gensim.models import Word2Vec
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def get_sentences(input_file_pointer):
    while True:
        line = input_file_pointer.readline()
        if not line:
            break
        yield line


def clean_sentence(sentence):
    sentence = sentence.lower().strip()
    sentence = re.sub(r'[^a-z0-9_\s]', '', sentence)
    return re.sub(r'\s{2,}', ' ', sentence)


def tokenize(sentence):
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
        input_file_pointer = open("wiki_trigram.txt", 'r')
        while True:
            line = input_file_pointer.readline()
            if not line:
                break
            cleaned_sentence = clean_sentence(line)
            tokenized_sentence = tokenize(cleaned_sentence)
            yield tokenized_sentence


sentences = MyCorpus()
phrases_model = build_phrases(sentences)
phrases_model.save('4_phrases_model.txt')

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

sentences_to_bi_grams(phrases_model, "wiki_trigram.txt", "wiki_4gram.txt")
print('wiki_4gram done')
class My4gramCorpus(object):
    """An interator that yields sentences (lists of str)."""
    def __iter__(self):
        input_file_pointer = open("wiki_4gram.txt", 'r')
        while True:
            line = input_file_pointer.readline()
            if not line:
                break
            #cleaned_sentence = clean_sentence(line)
            tokenized_sentence = tokenize(line)
            yield tokenized_sentence
#use processed bigram to train word2Vec
four_gram_sentences = My4gramCorpus()
model = Word2Vec(four_gram_sentences, size=50, window=10, min_count=8, workers=20, iter=10)

words = list(model.wv.vocab)
print(len(words))
model.save("wiki_4gram_w2v.model")
print('wordvec model done')


model = Word2Vec.load("wiki_4gram_w2v.model")
words = list(model.wv.vocab)
words.sort()
with open("wiki_4gram_50d.txt", "w") as out_file:
  for word in words:
    out_file.write(word)
    a = model[word]
    for value in a:
      out_file.write(" " + "%.4f"% value)
    out_file.write('\n')
print(len(words))

'''with open('wiki_3m.50d.txt', 'w') as out_file:
    for word in words:
        vec = model[word]
        out_file.write(word)
        for number in vec:
            out_file.write(' ' + str(round(number, 4)))
        out_file.write('\n')'''
'''for w in words[0:1000]:
    print(w)'''

'''print('curiosity', model.similar_by_word('curiosity', 10))
print('learningproblems', model.similar_by_word('learningproblems', 10))
print('causeproblem', model.similar_by_word('causeproblem', 10))
print('causeproblems', model.similar_by_word('causeproblems', 10))
print('causes_adverse',model.similar_by_word('causes_adverse', 10))
print('causesmental',model.similar_by_word('causesmental', 10))
print('causesmental_disorders',model.similar_by_word('causesmental_disorders', 10))
print('causesmental_illness',model.similar_by_word('causesmental_illness', 10))
print('causesroot',model.similar_by_word('causesroot', 10))
print('asksquestion',model.similar_by_word('asksquestion', 10))
print('dailyconversation',model.similar_by_word('dailyconversation', 10))
print('communicationgap',model.similar_by_word('communicationgap', 8))
print('encouragepeople', model.similar_by_word('encouragepeople', 8))
print('engageconversation', model.similar_by_word('engageconversation', 8))
print('invitedspeak', model.similar_by_word('invitedspeak', 8))
print('courageleadership', model.similar_by_word('courageleadership', 8))
print('provides_comfortable', model.similar_by_word('provides_comfortable', 8))
print(model.similar_by_word('curiosity', 8))
print(model.similar_by_word('curiosity', 8))
print(model.similar_by_word('curiosity', 8))
print(model.similar_by_word('curiosity', 8))'''
