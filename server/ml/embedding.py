import numpy as np
import cache
from scipy.spatial import distance

class EmbeddingModel:

  def __init__(self, filename, skip_head=True, dist_type='euclidean',
      cache_capacity=10000):
    self.vocabulary = []
    self.dictionary = {}
    self.embeddings = None
    header_read = False
    self.dist_type = dist_type

    with open(filename, 'r') as filehandler:
      numbers = []
      for line in filehandler:
        if skip_head and not header_read:
          header_read = True
          pass
        else:
          split = line.split(' ')
          self.dictionary[split[0]] = len(self.vocabulary)
          self.vocabulary.append(split[0])
          numbers.append([float(x) for x in split[2:]]) #split[1:]

    self.embeddings = np.array(numbers, dtype=np.float32)
    self._cache = cache.LRUCache(cache_capacity)

  def has_word(self, word):
    return word in self.dictionary

  def find_word(self, word):
    if word in self.dictionary:
      return self.dictionary[word]
    else:
      return None

  def get_embedding_for_a_word(self, word):
    return self.get_embedding_for_words([word])

  def get_word(self, index):
    if index < len(self.vocabulary):
      return self.vocabulary[index]
    else:
      return None

  def get_embedding_for_words(self, words):
    indicies = [self.dictionary[word] for word in words if word in self.dictionary]
    if len(indicies) > 0:
      embedding = np.mean(self.embeddings[indicies, :], axis=0)
    else:
      embedding = np.zeros(self.embeddings.shape[1],)
    return embedding

  def compute_all_distances_from_a_word(self, word):
    cache_value = self._cache[word]
    if word in self._cache:
      print 'cache hit:', word
      return self._cache[word]
    print 'cache miss:', word
    embedding = self.get_embedding_for_a_word(word)
    embedding = embedding.reshape(1, self.embeddings.shape[1])
    dists = distance.cdist(embedding, self.embeddings, self.dist_type)[0,:]
    self._cache[word] = dists
    return dists

  def recommend_words_by_avg_dist(self, words, how_many=100):
    embeddings = []
    for word in words:
      # this might be faster because we cache each word's distances
      embeddings.append(self.compute_all_distances_from_a_word(word))

    # average distances
    avg_dists = np.mean(np.array(embeddings), axis=0)

    sort_indices = avg_dists.argsort()
    return [self.vocabulary[index] for index in sort_indices[:how_many]]

  def getAutoComplete(self, word):
    return [{'text':x} for x in self.vocabulary if not isinstance(x, float) and x.startswith(word)]
