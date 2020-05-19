from appModule import app, db, bcrypt,api, distance_threshold
from flask_restful import Resource, reqparse
from sklearn  import  cluster
from sklearn.preprocessing import normalize
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from models import User, Concepts, ConceptsSchema, Article, ArticleSchema, CommentSchema
from models import Annotation, AnnotationSchema
from models import Assignment, AssignmentSchema, Theme, ThemeSchema, ThemeAssignmentJoinSchema, SubmissionAssignmentJoinSchema, ThemeSentence, ThemeSentenceSchema, Submission, SubmissionSchema
#from ml import embedding
#from ml import kde
#from ml import kde_new
#from ml import matching
from flask import request, jsonify, session, Response
import ipdb
import re
import collections
import tensorflow_hub as hub
#import matplotlib.pyplot as plt
import numpy as np
import json
import ast
import os
import pandas as pd
import random
from nltk.stem import WordNetLemmatizer

from scipy.spatial import distance
#from spacy.lang.en.stop_words import STOP_WORDS
#from gensim.models.phrases import Phrases, Phraser
#from gensim.models import Word2Vec
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize


lemmatizer = WordNetLemmatizer()
STOP_WORDS = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                  "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
                  "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
                  "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
                  "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as",
                  "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through",
                  "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
                  "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how",
                  "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
                  "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should",
                  "now"]
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
#@param ["https://tfhub.dev/google/universal-sentence-encoder/4","https://tfhub.dev/google/universal-sentence-encoder-large/5"]
model = hub.load(module_url)
print ("module %s loaded" % module_url)


header_read = False

skip_head = True
# dist_type = 'cosine' #'euclidean'
vocabulary = []
dictionary = {}
embeddings = None
cache_capacity = 10000

with open('./PhraseModel/wiki_4gram_50d.txt', 'r') as filehandler:
  numbers = []
  cnt = 0
  for line in filehandler:
    if skip_head and not header_read:
      header_read = True
      pass
    else:
      split = line.split(' ')
      dictionary[split[0]] = len(vocabulary)
      vocabulary.append(True) #dummy value
      numbers.append([float(x) for x in split[1:]])  # split[1:]
    cnt += 1

embeddings = np.array(numbers, dtype=np.float32)
print 'embedding done'

def embed(input):
  return model(input)
def deleteUSE_model():
  global model
  del model

schema = ConceptsSchema()
assignment_schema = AssignmentSchema()
submission_schema = SubmissionSchema()
theme_schema = ThemeSchema()
themeAssignmentJoinSchema = ThemeAssignmentJoinSchema()
article_list_schema = ArticleSchema(only=('published_date','title','type','section','id'), many=True)
article_schema = ArticleSchema()
comment_schema = CommentSchema()


headerNames = ['word'] + range(300)
# wordsFileName = './data/glove.6B.300d.txt'
#wordsFileName = './data/glove.6B.50d.txt' # for testing
wordsFileName = './data/wiki_4gram_50d.txt'

# unified w2v queries with caching
'''w2v_model = embedding.EmbeddingModel(wordsFileName)
kde_model = kde.KdeModel(w2v_model)
kde_model = kde_new.KdeModel(w2v_model)'''
default_kde_h_sq = 2
# default_kde_h_sq = 1e-1

# previous_clustering_result = None

print 'I am ready......'
serverAnnotator = 7
white = ['http://localhost:5000', 'http://localhost:9000']
@app.after_request
def after_request(response):
  #print request.environ
  ''' response.headers.add('Access-Control-Allow-Credentials', "true")
  response.headers.add('Access-Control-Allow-Origin', 'http://0.0.0.0:9000')
  response.headers.add('Access-Control-Allow-Origin', 'http://0.0.0.0:5000')
  response.headers.add('Access-Control-Allow-Origin', 'http://www.hdilab-essayiq.xyz:5000')
  response.headers.add('Access-Control-Allow-Origin', 'http://hdilab-essayiq.xyz:5000')
  response.headers.add('Access-Control-Allow-Origin', 'http://www.hdilab-essayiq.xyz:9000')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Accept')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
  response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
  response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response
  print 'request header', request.headers['Origin']
  white_origin = ['http://0.0.0.0:9000', 'http://0.0.0.0:5000']'''
  server = True
  if server: #for server
    response.headers['Access-Control-Allow-Credentials'] = "true"
    response.headers['Access-Control-Allow-Origin'] =  'http://www.hdilab-essayiq.xyz:9000' #'http://127.0.0.1:9000'#
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE,OPTIONS,PATCH'
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Accept')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
    response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response
  else:
    white_origin = ['http://0.0.0.0:9000', 'http://0.0.0.0:5000']
    if request.headers['Origin'] in white_origin: #for local
      response.headers['Access-Control-Allow-Credentials'] = "true"
      response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
      response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE,OPTIONS,PATCH'
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Accept')
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
      response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
      response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
      response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response

class QueryAutoComplete(Resource):
  def get(self, word):
    wordUTF8 = word.encode('UTF-8')
    new_list = w2v_model.getAutoComplete(wordUTF8)
    return {'word': new_list}

class Register(Resource):
  def post(self):
    # Parse the arguments

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help="User name to be called")
    parser.add_argument('email', type=str, help='Email address to create user')
    parser.add_argument('password', type=str, help='Password to create user')

    args = parser.parse_args()

    _userName = args['name']
    _userEmail = args['email']
    _userPassword = args['password']

    user = User(name=_userName, email=_userEmail, password=_userPassword)
    try:
      db.session.add(user)
      db.session.commit()
      status = 'success'

    except Exception as e:
      status = 'This user is already registered'
      db.session.close()

    return {'result': status}

class Login(Resource):
  def post(self):
    print "abc"
    try:
      # Parse the arguments
      parser = reqparse.RequestParser()
      parser.add_argument('email', type=str, help='Email address for Authentification')
      parser.add_argument('password', type=str, help='Password for Authentication')
      args = parser.parse_args()

      _userEmail = args['email']
      _userPassword = args['password']

      user = User.query.filter_by(email=_userEmail).first()
      if user and bcrypt.check_password_hash(user.password, _userPassword):
        session['logged_in'] = True
        session['user'] = user.id
        session['userName'] = user.name
        status = True
      else:
        status = False
      return jsonify({'result':status, 'name': user.name})
    except Exception as e:
      print e
      return {'error':str(e)}

class Logout(Resource):
  def get(self):
    try:
      # Parse the arguments
      session.pop('logged_in', None)
      session.pop('user', None)
      session.pop('userName', None)
      # session.pop('previous_clustering_result',None)

      return {'result':'success'}
    except Exception as e:
      return {'error':str(e)}

class Status(Resource):
  def get(self):

    if session.get('logged_in'):
      if session['logged_in']:
        return {'status':True, 'user': session['user'], 'userName':session['userName']}
    else:
      return {'status' : False}

class AssignmentList(Resource):
  def get(self):
    assignment_query = Assignment.query.all()
    results = assignment_schema.dump(assignment_query, many=True).data
    print 'inside get method of Assignment list...'
    #print results
    return results
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help="Assignment name")
    parser.add_argument('title', type=str, help='Assignment title')
    parser.add_argument('description', type=str, help='Assignment description')
    #parser.add_argument('creator_id', type=int, help='Password to create user')

    args = parser.parse_args()
    assignment = Assignment(args['name'], args['title'], args['description'], session['user'], session['userName'])
    assignment.add(assignment)
    query = Assignment.query.get(assignment.id)
    results = schema.dump(query).data
    return results, 201


class AssignmentUpdate(Resource):
  def get(self, id):
    assignment_query = Assignment.query.get_or_404(id)
    result = assignment_schema.dump(assignment_query).data
    return result

  def patch(self, id):
    assignment = Assignment.query.get_or_404(id)
    raw_dict = request.get_json(force=True)
    try:
      if session.get('logged_in'):
        userID = session['user']
      schema.validate(raw_dict)
      assignment_dict = raw_dict

      if userID == assignment.creator_id:
        for key, value in assignment_dict.items():
          setattr(assignment, key, value)
        assignment.update()
        return self.get(id)
      else:
        resp = jsonify({"error":"You are not owner of this concept"})
        resp.status_code = 401
        return resp

    except ValidationError as err:
      resp = jsonify({"error":err.messages})
      resp.status_code = 401
      return resp

    except SQLAlchemyError as e:
      db.session.rollback()
      resp = jsonify({"error": str(e)})
      resp.status_code = 401
      return resp

class SubmissionList(Resource):
  def get(self):
    submission_query = Submission.query.join(Assignment, Assignment.id == Submission.assignmentID) \
      .add_columns(Submission.submissionID, Submission.assignmentID, Submission.submissionName,
                   Submission.submissionBody, Assignment.name, Assignment.title)
    results = SubmissionAssignmentJoinSchema().dump(submission_query, many=True).data

    #submission_query = Submission.query.all()
    #results = submission_schema.dump(submission_query, many=True).data
    print 'inside get method of Submission list...'
    #print results
    return results
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('submissionName', type=str, help="Submission name")
    parser.add_argument('submissionBody', type=unicode, help="Essay") #unicode for python2, str for python3
    parser.add_argument('assignmentID', type=int, help='assignment ID')
    #parser.add_argument('creator_id', type=int, help='Password to create user')

    args = parser.parse_args()
    submission = Submission(args['submissionName'], args['submissionBody'], args['assignmentID'], session['user'], session['userName'])
    submission.add(submission)
    query = Submission.query.get(submission.submissionID)
    results = submission_schema.dump(query).data
    return results, 201

class ThemeList(Resource):
  def get(self):
    theme_query = Theme.query.join(Assignment, Assignment.id==Theme.assignment_id)\
                  .add_columns(Theme.id, Theme.assignment_id, Theme.themeName, Theme.color, Theme.themeSentences, Assignment.name, Assignment.title).order_by(Theme.id)
    results = themeAssignmentJoinSchema.dump(theme_query, many=True).data #theme_schema.dump(theme_query, many=True).data
    print 'get method of theme'
    return results
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('themeName', type=str, help="Theme name")  # unicode for python2, str for python3
    parser.add_argument('themeSentences', type=unicode, help='theme sentences')
    parser.add_argument('assignment_id', type=int, help='assignment id')
    parser.add_argument('color', type=str, help='theme color')

    args = parser.parse_args()
    themeObject = Theme(args['themeName'], args['themeSentences'], args['assignment_id'], args['color'])
    themeObject.add(themeObject)
    query = Theme.query.get(themeObject.id)
    results = theme_schema.dump(query).data
    return results, 201

class ThemeData(Resource):
  def get(self, themeId):
    theme_query = Theme.query.filter_by(id=themeId).join(Assignment, Assignment.id == Theme.assignment_id) \
      .add_columns(Theme.id, Theme.assignment_id, Theme.themeName, Theme.color, Theme.themeSentences, Assignment.name,
                   Assignment.title)
    results = themeAssignmentJoinSchema.dump(theme_query,
                                             many=True).data  # theme_schema.dump(theme_query, many=True).data
    #print 'specific theme'
    #print results
    return results[0]
  def patch(self, themeId):
    theme = Theme.query.get_or_404(themeId)
    raw_dict = request.get_json(force=True)
    for key, value in raw_dict.items():
      setattr(theme, key, value)
    theme.update()
    return self.get(themeId)


class ThemeDelete(Resource):
  def get(self, themeId):
    theme = Theme.query.get_or_404(themeId)
    delete = theme.delete(theme)

class ThemeByAssignment(Resource):
  def get(self, assignment_id):
    themeQuery = Theme.query.filter_by(assignment_id=assignment_id)
    themes = ThemeSchema().dump(themeQuery, many=True).data
    print 'get with param'
    return themes

class ConceptList(Resource):
  def get(self):
    concepts_query = Concepts.query.all()
    print concepts_query
    results = schema.dump(concepts_query, many=True).data
    return results

  def post(self):
    raw_dict = request.get_json(force=True)
    try:
      schema.validate(raw_dict)
      concept_dict = raw_dict

      if session.get('logged_in'):
        userID = session['user']
        userName = session['userName']
      else:
        return {'status':"UnAuthorized Access for Post ConceptList"}

      concept = Concepts(concept_dict['name'], userID, concept_dict['concept_type'], concept_dict['input_terms'], userName)
      concept.add(concept)

      query = Concepts.query.get(concept.id)
      results = schema.dump(query).data

      return results, 201

    except ValidationError as err:
      resp = jsonify({"error":err.messages})
      resp.status_code = 403
      return resp

    except SQLAlchemyError as e:
      db.session.rollback()
      resp = jsonify({"error": str(e)})
      resp.status_code = 403
      return resp


class ConceptsUpdate(Resource):
  def get(self,id):
    concept_query = Concepts.query.get_or_404(id)
    result = schema.dump(concept_query).data
    return result

  def patch(self,id):
    concept = Concepts.query.get_or_404(id)
    raw_dict = request.get_json(force=True)

    try:
      if session.get('logged_in'):
        userID = session['user']
      schema.validate(raw_dict)
      concept_dict = raw_dict

      if userID == concept.creator_id:
        for key, value in concept_dict.items():
          setattr(concept, key, value)
        concept.update()
        return self.get(id)
      else:
        resp = jsonify({"error":"You are not owner of this concept"})
        resp.status_code = 401
        return resp

    except ValidationError as err:
      resp = jsonify({"error":err.messages})
      resp.status_code = 401
      return resp

    except SQLAlchemyError as e:
      db.session.rollback()
      resp = jsonify({"error": str(e)})
      resp.status_code = 401
      return resp

  def delete(self, id):
    concept = Concepts.query.get_or_404(id)
    try:
      delete = concept.delete(concept)
      concepts_query = Concepts.query.all()
      results =  schema.dump(concepts_query, many=True).data
      return results
    except SQLAlchemyError as e:
      db.session.rollback()
      resp = jsonify({"error": str(e)})
      resp.status_code = 401
      return resp

class ArticleList(Resource):
  def get(self):
    articles_query = Article.query.all()
    results = article_list_schema.dump(articles_query).data
    return results


class ArticleUpdate(Resource):
  def get(self,id):
    try:
      article_query = Article.query.get_or_404(id)
      article_result = article_schema.dump(article_query).data
      comments_result = comment_schema.dump(article_query.comments, many=True).data

    except Exception as e:
      print e
    return jsonify({'article':article_result, 'comments':comments_result})


class ConceptScore(Resource):
  def get(self):

    parser = reqparse.RequestParser()
    parser.add_argument('articleID', type=int, help="articleID")
    parser.add_argument('conceptID', type=int, help='conceptID')

    args = parser.parse_args()
    articleID = args['articleID']
    conceptID = args['conceptID']
    try:
      article_query = Article.query.get_or_404(articleID)
      comments = article_query.comments
      concept_query = Concepts.query.get_or_404(conceptID)
      concept_info = schema.dump(concept_query).data
      commentsScore, keywords = self.getScore(concept_query, comments)
      return jsonify({'scores':commentsScore, 'keywords': keywords, 'concept': concept_info})

    except Exception as e:
      print e

  def getScore(self, concept, comments):
    try:
      positive_terms_concept = concept.input_terms['positive']
      negative_terms_concept = concept.input_terms['negative']

      if 'irrelevant' in concept.input_terms:
        irrelevant_terms_concept = concept.input_terms['irrelevant']
      else:
        irrelevant_terms_concept = []

      if positive_terms_concept == None:
        positive_terms = []
      else:
        positive_terms = [w['text'] for w in positive_terms_concept]

      if negative_terms_concept == None:
        negative_terms = []
      else:
        negative_terms = [w['text'] for w in negative_terms_concept]

      if irrelevant_terms_concept == None:
        irrelevant_terms = []
      else:
        irrelevant_terms = [w['text'] for w in irrelevant_terms_concept]

      kde_model.learn(h_sq=default_kde_h_sq,
                      pos_words=positive_terms,
                      neg_words=negative_terms, irr_words=irrelevant_terms)
      scores = {}
      all_comment_words = []
      for comment in comments:
          scores[comment.commentID] = \
              kde_model.get_comment_score_from_text(comment.commentBody)
          words_in_a_comment = re.sub('[^a-z]+', ' ', comment.commentBody.lower()).split()
          all_comment_words +=  [w for w in words_in_a_comment if w not in all_comment_words]

      n_addl_keywords = 50
      # keywords = kde_model.getKeywordsScore(all_comment_words, concept.concept_type, len(all_comment_words)/20)
      keywords = kde_model.getKeywordsScore(all_comment_words, concept.concept_type)
      print keywords

    except Exception as e:
      print e

    return scores, keywords

class ConceptDownload(Resource):
  def get(self,id):
    concept_query = Concepts.query.get_or_404(id)
    result = schema.dump(concept_query).data

    return Response(result, mimetype="application/json", headers={'Content-Disposition':'attachment;filename=concept.json'})

class ConceptDelete(Resource):
  def get(self,id):
    concept = Concepts.query.get_or_404(id)
    try:
      if session.get('logged_in'):
        userID = session['user']

      if userID == concept.creator_id:
        delete = concept.delete(concept)
        concepts_query = Concepts.query.all()
        results =  schema.dump(concepts_query, many=True).data
        return results
      else:
        resp = jsonify({"error":"You are not owner of this concept"})
        resp.status_code = 401
        return resp

    except ValidationError as err:
      resp = jsonify({"error":err.messages})
      resp.status_code = 401
      return resp

    except SQLAlchemyError as e:
      db.session.rollback()
      resp = jsonify({"error": str(e)})
      resp.status_code = 401
      return resp

class AssignmentDelete(Resource):
  def get(self,id):
    assignment = Assignment.query.get_or_404(id)
    try:
      userID = None
      if session.get('logged_in'):
        userID = session['user']
      if (userID is not None) and (userID == assignment.creator_id):
        delete = assignment.delete(assignment)
        assignment_query = Assignment.query.all()
        results = schema.dump(assignment_query, many=True).data
        return results
      else:
        resp = jsonify({"error":"You are not owner of this assignment"})
        resp.status_code = 401
        return resp

    except ValidationError as err:
      resp = jsonify({"error":err.messages})
      resp.status_code = 401
      return resp

    except SQLAlchemyError as e:
      db.session.rollback()
      resp = jsonify({"error": str(e)})
      resp.status_code = 401
      return resp

class SubmissionHighlight(Resource):
  def get(self, submission_id, assignment_id):
    return WholeSubmissionHighlight().getData(submission_id, assignment_id)
  def get_sentence_array(self, essaystr):
    essaystr = essaystr.replace("\r", " ")
    essaystr = essaystr.replace("\n", " ")
    essaystr = ' '.join(essaystr.split())
    if essaystr.find('?') != -1:
      print 'essaystr', essaystr
    sentences = sent_tokenize(essaystr)
    ngrams = []
    for sentence in sentences:
        ngrams.append(sentence)
    return ngrams

class AnnotateWholeSubmissions(Resource):
  def get(self, assignment_id):
    submissionQuery = Submission.query.filter_by(assignmentID=assignment_id)
    submissions = SubmissionSchema().dump(submissionQuery, many=True).data
    results = []
    for submission in submissions:
      results.append(self.getData(submission['submissionID'], assignment_id))
    return results

  def getData(self, submission_id, assignment_id):
    themeQuery = Theme.query.filter_by(assignment_id=assignment_id)
    themes = ThemeSchema().dump(themeQuery, many=True).data
    submission = Submission.query.get_or_404(submission_id)
    essay = submission.submissionBody
    x = [(theme['themeName'], theme['themeSentences'], theme['color']) for theme in themes]
    submission_sentences = self.get_sentence_array(essay)
    #print 'submission name', submission.submissionName
    return {'sentences': submission_sentences, 'submissionid': submission_id, 'submissionname': submission.submissionName, 'themes': themes}

  def get_sentence_array(self, essaystr):
    essaystr = essaystr.replace("\r", " ")
    essaystr = essaystr.replace("\n", " ")
    essaystr = ' '.join(essaystr.split())
    sentences = sent_tokenize(essaystr)
    ngrams = []
    for sentence in sentences:
      ngrams.append(sentence)
    return ngrams

class SaveAnnotation(Resource):
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('assignment_id', type=int, help='Assignment id')
    parser.add_argument('submissionID', type=int, help='submission id')
    parser.add_argument('sentenceIndex', type=int, help='Sentence index')
    parser.add_argument('selectedTheme', type=int, help='Selected theme')
    parser.add_argument('annotatorID', type=int, help='user id')
    parser.add_argument('submissionName', type=str, help="submission name")
    parser.add_argument('sentence', type=unicode, help="sentence content")
    parser.add_argument('annotatorName', type=str, help='user name')
    # parser.add_argument('creator_id', type=int, help='Password to create user')
    args = parser.parse_args()
    #assignment_id, submissionID, sentenceIndex, selectedTheme, annotatorID, submissionName=None, annotatorName=None
    AnnotationObject = Annotation(args['assignment_id'], args['submissionID'], args['sentenceIndex'], args['selectedTheme'], args['annotatorID'], args['sentence'], args['submissionName'], args['annotatorName'])
    AnnotationObject.add(AnnotationObject)
    query = Annotation.query.get(AnnotationObject.id)
    results = AnnotationSchema().dump(query).data
    return results
    '''f = open("annotation.txt", "a+")
    f.write(str(args)+'\n')
    return 201'''

class GetAnnotation(Resource):
  def getthemesentence(self, themeid):
    annotationQuery = Annotation.query.filter_by(selectedTheme=themeid)
    annotations = AnnotationSchema().dump(annotationQuery, many=True).data
    random.shuffle(annotations) #randomize annotation data
    themesentences = ""
    numsentences =  int(len(annotations)*0.10) #take 10% of annotated theme sentences from all annotator
    if numsentences < 10:
      numsentences = min(10, len(annotations))
    print 'numsentences', numsentences
    for x in annotations[0:numsentences]:
      themesentences = themesentences + ' ' + x['sentence']
    return themesentences
  def getgoldstandard(self, submissionid, userid):
    annotationQuery = Annotation.query.filter_by(submissionID=submissionid, annotatorID=userid).order_by('sentenceIndex')
    annotations = AnnotationSchema().dump(annotationQuery, many=True).data
    return annotations
  def getthemesentencebyuser(self, themeid, userid):
    #print themeid, userid
    annotationQuery = Annotation.query.filter_by(selectedTheme=themeid, annotatorID=userid)
    annotations = AnnotationSchema().dump(annotationQuery, many=True).data
    print 'annotation size', len(annotations)
    random.shuffle(annotations)
    themesentences = ""
    numsentences = int(len(annotations) * 0.10)  # take 10% of annotated theme sentences from all annotator
    if numsentences < 10:
      numsentences = min(10, len(annotations))
    print themeid, numsentences
    for x in annotations[0:numsentences]:
      themesentences = themesentences + ' ' + x['sentence']
    return themesentences

  def get(self, annotatorID):
    annotationQuery = Annotation.query.filter_by(annotatorID=annotatorID)
    annotations = AnnotationSchema().dump(annotationQuery, many=True).data
    return annotations
  '''def get(self, assignment_id):
    annotation = {}
    annotation['sentence'] = []
    with open('annotation.txt') as fp:
      for line in fp:
        if len(line) < 10:
          continue
        print type(line)
        #data = json.loads(line)
        data = ast.literal_eval(line)
        if int(data['assignmentid']) == int(assignment_id):
          annotation['sentence'].append(data)
    return annotation['sentence']'''
class GetUserAnnotation(Resource):
  def get(self, userid, selectedtheme):
    '''parser = reqparse.RequestParser()
    parser.add_argument('userid', type=int, help="user id")
    parser.add_argument('selectedtheme', type=int, help='theme id')
    args = parser.parse_args()
    print args['userid']'''
    print selectedtheme, userid
    userid = int(userid)
    selectedtheme = int(selectedtheme)
    return GetAnnotation().getthemesentencebyuser(selectedtheme, userid) #args['selectedtheme'], args['userid']
    #return 201


class DeleteAnnotation(Resource):
  def get(self, id):
    annotation = Annotation.query.get_or_404(id)
    try:
      if session.get('logged_in'):
        userID = session['user']
      if userID == annotation.annotatorID:
        delete = annotation.delete(annotation)
        return {'annotation': GetAnnotation().get(annotation.annotatorID), 'id': id}
      else:
        resp = jsonify({"error": "You are not owner of this concept"})
        resp.status_code = 401
        return resp
    except Exception as e:
      print e
      return {'error':str(e)}

# simple Least Recently Used Cache
# inspired by https://www.kunxi.org/blog/2014/05/lru-cache-in-python/
class LRUCache:
  def __init__(self, capacity):
    self._cache = collections.OrderedDict()
    self._capacity = capacity

  def __setitem__(self, key, value):
    if key in self._cache:
      self._cache.pop(key)
    elif len(self._cache) >= self._capacity:
      self._cache.popitem(last=False)
    self._cache[key] = value

  def __getitem__(self, key):
    if key in self._cache:
      value = self._cache.pop(key)
      # put in the back
      self._cache[key] = value
      return value
    else:
      return None

  def __contains__(self, key):
    return key in self._cache

class WholeSubmissionHighlight(Resource):
  def get(self, assignment_id, userid):
    submissionQuery = Submission.query.filter_by(assignmentID=assignment_id)
    submissions = SubmissionSchema().dump(submissionQuery, many=True).data
    results = []
    if serverAnnotator != None:
      userid = serverAnnotator
    phrase2vecresult = []
    f2 = open('essayiqgold.txt', "w")
    sentence_cnt = [0]
    for submission in submissions:
      results.append(self.getData(submission['submissionID'], assignment_id, userid, sentence_cnt))
      phrase2vecresult.append(self.getDataPhrase2Vec(submission['submissionID'], assignment_id, userid))
      goldstandardannotations = GetAnnotation().getgoldstandard(submission['submissionID'], userid)
      for annotation in goldstandardannotations:
        dic = dict()
        dic['sentence'] = annotation['sentence']
        dic['themeid'] = annotation['selectedTheme']
        theme = Theme.query.get_or_404(annotation['selectedTheme'])
        dic['color'] = theme.color
        dic['sentenceindex'] = annotation['sentenceIndex']
        dic['submissionname'] = submission['submissionName']
        f2.write(json.dumps(dic)+'\n')
    f2.close()
    print 'sentence count', sentence_cnt[0]
    #deleteUSE_model()


    f = open("essayiq.txt", "w")
    for res in results:
      for i in range(len(res['sentences'])):
        dic = dict()
        dic['sentence'] = res['sentences'][i]
        dic['themeMarker'] = res['themeMarkers'][i]
        dic['color'] = res['colors'][i]
        dic['submissionname'] = res['submissionName']
        dic['themeid'] = res['themeids'][i]
        dic['sentenceindex'] = i
        f.write(json.dumps(dic)+'\n')

    # for submission in submissions:
    # phrase2vecresult.append(self.getDataPhrase2Vec(submission['submissionID'], assignment_id, userid))
    f3 = open('phrase2vec.txt', "w")
    for res in phrase2vecresult:
      for i in range(len(res['sentences'])):
        dic = dict()
        dic['sentence'] = res['sentences'][i]
        dic['themeMarker'] = res['themeMarkers'][i]
        dic['color'] = res['colors'][i]
        dic['submissionname'] = res['submissionName']
        dic['themeid'] = res['themeids'][i]
        dic['sentenceindex'] = i
        f3.write(json.dumps(dic)+'\n')

    return results

  def clean_sentence(self, sentence):
      sentence = sentence.lower().strip()
      sentence = re.sub(r'[^a-z0-9_\s]', '', sentence)
      return re.sub(r'\s{2,}', ' ', sentence)

  def tokenize(self,sentence):
    return [lemmatizer.lemmatize(token) for token in sentence.split() if ((token not in STOP_WORDS)
                                                                          and (not token.isdigit()))]
  # for each submission sentence, this function returns themeName or No theme
  def getData(self, submission_id, assignment_id, userid, sentence_cnt=None):
    themeQuery = Theme.query.filter_by(assignment_id=assignment_id)
    themes = ThemeSchema().dump(themeQuery, many=True).data
    submission = Submission.query.get_or_404(submission_id)
    essay = submission.submissionBody

    #x = [(theme['themeName'], theme['themeSentences'], theme['color'], theme['id']) for theme in themes]
    x = [(theme['themeName'], GetAnnotation().getthemesentencebyuser(theme['id'], userid), theme['color'], theme['id']) for theme in themes]
    submission_sentences = self.get_sentence_array(essay)
    if sentence_cnt is not None:
      sentence_cnt[0] += len(submission_sentences)
    theme_sentences_array = [self.get_sentence_array(item[1]) for item in x]
    num_themes = len(theme_sentences_array)
    theme_embedding = []
    for i in range(0, len(theme_sentences_array)):
      theme_embedding.append(embed(theme_sentences_array[i]))
    themeMarker = []
    themeColors = []
    selectedThemeSentences = []
    for sent in submission_sentences:
      candidate_embedding = embed([sent])
      most_similar_sentences = []
      for i in range(0, len(theme_embedding)):  # for each theme
        sent_embeddings = np.array(theme_embedding[i])
        dists = distance.cdist(candidate_embedding[:1], sent_embeddings, 'cosine')[0, :]
        tuples = [tup for tup in sorted(enumerate(dists), key=lambda x: x[1])]
        for j in range(0, len(tuples)):
          most_similar_sentences.append(
            (tuples[j][1], x[i][0], x[i][2], theme_sentences_array[i][tuples[j][0]], x[i][3]))  # x[i][0] is themeName
      most_similar_sentences = sorted(most_similar_sentences, key=lambda t: t[0])
      if most_similar_sentences[0][0] <= distance_threshold:
        themeMarker.append(most_similar_sentences[0][1])
        themeColors.append(most_similar_sentences[0][2])
        selectedThemeSentences.append((most_similar_sentences[0][3], most_similar_sentences[0][4]))
      else:
        themeMarker.append("No theme")
        themeColors.append("None")
        selectedThemeSentences.append(("No theme sentence", -1))
    return {'sentences': submission_sentences, 'themeMarkers': themeMarker, 'colors': themeColors, 'themes': themes,
            'submissionName': submission.submissionName, 'themeSentences': [t[0] for t in selectedThemeSentences], 'themeids': [t[1] for t in selectedThemeSentences]}

  # for each submission sentence, this function returns themeName or No theme
  def getDataPhrase2Vec(self, submission_id, assignment_id, userid):

    #_cache = LRUCache(cache_capacity)

    def get_embedding_for_words(words):
      indicies = [dictionary[word] for word in words if word in dictionary]
      if len(indicies) > 0:
        embedding = np.mean(embeddings[indicies, :], axis=0)
      else:
        embedding = np.zeros(embeddings.shape[1], )
      return embedding

    themeQuery = Theme.query.filter_by(assignment_id=assignment_id)
    themes = ThemeSchema().dump(themeQuery, many=True).data
    submission = Submission.query.get_or_404(submission_id)
    essay = submission.submissionBody

    # x = [(theme['themeName'], theme['themeSentences'], theme['color'], theme['id']) for theme in themes]
    x = [(theme['themeName'], GetAnnotation().getthemesentencebyuser(theme['id'], userid), theme['color'], theme['id'])
         for theme in themes]
    submission_sentences = self.get_sentence_array(essay)
    theme_sentences_array = [self.get_sentence_array(item[1]) for item in x]
    num_themes = len(theme_sentences_array)
    theme_embedding = []
    for i in range(0, len(theme_sentences_array)):
      phrasevector = []
      for theme_sentence in theme_sentences_array[i]:
        tokenized_sentence = self.tokenize(theme_sentence)
        phrasevector.append(get_embedding_for_words(tokenized_sentence))
      theme_embedding.append(phrasevector)
    themeMarker = []
    themeColors = []
    selectedThemeSentences = []
    for sent in submission_sentences:
      candidate_embedding = get_embedding_for_words(self.tokenize(sent)) #embed([sent])
      most_similar_sentences = []
      for i in range(0, len(theme_embedding)):  # for each theme
        sent_embeddings = np.array(theme_embedding[i])
        dists = distance.cdist([candidate_embedding], sent_embeddings, 'cosine')[0, :]
        tuples = [tup for tup in sorted(enumerate(dists), key=lambda x: x[1])]
        for j in range(0, len(tuples)):
          most_similar_sentences.append(
            (tuples[j][1], x[i][0], x[i][2], theme_sentences_array[i][tuples[j][0]], x[i][3]))  # x[i][0] is themeName
      most_similar_sentences = sorted(most_similar_sentences, key=lambda t: t[0])
      if most_similar_sentences[0][0] <= distance_threshold: #threshold is less for phrase2vec
        themeMarker.append(most_similar_sentences[0][1])
        themeColors.append(most_similar_sentences[0][2])
        selectedThemeSentences.append((most_similar_sentences[0][3], most_similar_sentences[0][4]))
      else:
        themeMarker.append("No theme")
        themeColors.append("None")
        selectedThemeSentences.append(("No theme sentence", -1))
    return {'sentences': submission_sentences, 'themeMarkers': themeMarker, 'colors': themeColors, 'themes': themes,
            'submissionName': submission.submissionName, 'themeSentences': [t[0] for t in selectedThemeSentences],
            'themeids': [t[1] for t in selectedThemeSentences]}
  def get_sentence_array(self, essaystr):
    essaystr = essaystr.replace("\r", " ")
    essaystr = essaystr.replace("\n", " ")
    essaystr = ' '.join(essaystr.split())
    sentences = sent_tokenize(essaystr)
    ngrams = []
    for sentence in sentences:
      ngrams.append(sentence)
    return ngrams

class DeleteSentenceFromTheme(Resource):
  def patch(self):
    parser = reqparse.RequestParser()
    parser.add_argument('themesentence', type=str, help="theme sentence")
    parser.add_argument('selectedtheme', type=int, help='Selected theme')
    args = parser.parse_args()
    theme_query = Theme.query.get_or_404(args['selectedtheme'])
    result = ThemeSchema().dump(theme_query).data
    print result
    print args['themesentence']
    themeSentenceArray = WholeSubmissionHighlight().get_sentence_array(result['themeSentences'])
    themeSentenceArray = [sentence for sentence in themeSentenceArray if sentence != args['themesentence']]
    theme = Theme.query.get_or_404(args['selectedtheme'])
    setattr(theme, 'themeSentences', ' '.join(themeSentenceArray))
    theme.update()
    return 201
class AddEssaySentenceToTheme(Resource):
  def patch(self):
    parser = reqparse.RequestParser()
    parser.add_argument('essaysentence', type=str, help="Essay sentence")
    parser.add_argument('selectedtheme', type=int, help='Selected theme')
    args = parser.parse_args()
    theme_query = Theme.query.get_or_404(args['selectedtheme'])
    result = ThemeSchema().dump(theme_query).data

    theme = Theme.query.get_or_404(args['selectedtheme'])
    setattr(theme, 'themeSentences', result['themeSentences'] + ' ' + args['essaysentence'])
    theme.update()
    return 201



api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Logout, '/api/logout')
api.add_resource(Status, '/api/status')

api.add_resource(AssignmentList, '/api/assignments')
api.add_resource(AssignmentUpdate, '/api/assignments/<int:id>')
api.add_resource(AssignmentDelete, '/api/assignment_delete/<int:id>')

api.add_resource(SubmissionList, '/api/submissions')
api.add_resource(SubmissionHighlight, '/api/submissions/<int:submission_id>/<int:assignment_id>')
api.add_resource(WholeSubmissionHighlight, '/api/wholesubmissions/<int:assignment_id>/<int:userid>')
api.add_resource(AnnotateWholeSubmissions, '/api/annotatewholesubmissions/<int:assignment_id>')

api.add_resource(ThemeList, '/api/themes')
api.add_resource(ThemeData, '/api/themes/<int:themeId>')
api.add_resource(ThemeDelete, '/api/theme_delete/<int:themeId>')
api.add_resource(ThemeByAssignment, '/api/themes_filterbyassignment/<int:assignment_id>')


api.add_resource(SaveAnnotation, '/api/saveAnnotation')
api.add_resource(GetAnnotation, '/api/GetAnnotation/<int:annotatorID>')
api.add_resource(GetUserAnnotation, '/api/GetUserBasedAnnotation/<int:userid>/<int:selectedtheme>')
api.add_resource(DeleteAnnotation, '/api/DeleteAnnotation/<int:id>')

api.add_resource(DeleteSentenceFromTheme, '/api/deletethemesentence')
api.add_resource(AddEssaySentenceToTheme, '/api/AddEssaySentence')
