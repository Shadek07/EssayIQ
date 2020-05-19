from appModule import db, bcrypt
from sqlalchemy.dialects.postgresql import JSON, ARRAY, BIGINT
import datetime
# from marshmallow_jsonapi import  fields, Schema
from marshmallow import validate, fields, Schema
import json
from sqlalchemy.ext.hybrid import hybrid_property

class CRUD():
	def add(self, resource):
		db.session.add(resource)
		return db.session.commit()

	def update(self):
		return db.session.commit()

	def delete(self, resource):
		db.session.delete(resource)
		return db.session.commit()


class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255), nullable=True, default="User")
  email = db.Column(db.String(255), index=True, unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)
  registered_on = db.Column(db.DateTime, nullable=False)
  admin = db.Column(db.Boolean, nullable=False, default=False)
  concepts = db.relationship('Concepts', backref="users", cascade="all, delete-orphan", lazy="dynamic")
  assignments = db.relationship('Assignment', backref="users", cascade="all, delete-orphan", lazy="dynamic")
  submissions = db.relationship('Submission', backref="users", cascade="all, delete-orphan", lazy="dynamic")

  def __init__(self, name, email, password, admin=False):
    self.name = name
    self.email = email
    self.password = bcrypt.generate_password_hash(password)
    self.registered_on = datetime.datetime.now()
    self.admin = admin

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return self.id

  def __repr__(self):
    return '<id {}>'.format(self.id)


class Concepts(db.Model, CRUD):
	__tablename__ = 'concepts'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(255), nullable=False, unique=True)
	help_text = db.Column(db.String(255))
	created_on = db.Column(db.DateTime, nullable=False)
	edited_on = db.Column(db.DateTime, nullable=False)
	creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	creator = db.relationship("User", back_populates="concepts")
	creator_name = db.Column(db.String(255), nullable=False)

	concept_type=db.Column(db.String(20), default='bipolar', nullable=False)
	input_terms=db.Column(JSON)

	def __init__(self, name, creator_id, concept_type, input_terms, creator_name ):
		self.name = name
		self.creator_id = creator_id
		self.concept_type = concept_type
		self.input_terms = input_terms
		self.created_on = datetime.datetime.now()
		self.edited_on = datetime.datetime.now()
		self.creator_name = creator_name

	def get_id(self):
		return self.id

	def __repr__(self):
		return '<id {}>'.format(self.id)

class ConceptsSchema(Schema):

	not_blank = validate.Length(min=1, error='Field cannot be blank')
	id = fields.Integer(dump_only=False)
	name = fields.Str()
	created_on = fields.DateTime()
	creator_id = fields.Integer()
	concept_type = fields.Str()
	input_terms = fields.Raw()
	creator_name = fields.Str()
	help_text = fields.Str()

	#self links
	def get_top_level_links(self, data, many):
		if many:
			self_link = "/concepts/"
		else:
			self_link = "/concepts/{}".format(data['id'])
		return {'self': self_link}

	class Meta:
		type_ = 'concepts'

class Article(db.Model):
	__tablename__ = 'articles'

	url = db.Column(db.String)
	adx_keywords = db.Column(db.String)
	column = db.Column(db.String)
	section = db.Column(db.String)
	byline = db.Column(db.String)
	type= db.Column(db.String)
	title = db.Column(db.String)
	abstract = db.Column(db.String)
	published_date = db.Column(db.DateTime)
	source= db.Column(db.String)
	id = db.Column(BIGINT, primary_key=True)
	asset_id = db.Column(BIGINT)
	views = db.Column(db.Integer)
	des_facet = db.Column(ARRAY(db.String))
	org_facet = db.Column(ARRAY(db.String))
	per_facet = db.Column(ARRAY(db.String))
	geo_facet = db.Column(ARRAY(db.String))
	media = db.Column(ARRAY(db.String))
	comments = db.relationship("Comment", back_populates="article")

	@hybrid_property
	def comments_count(self):
	    return len(self.comments)

	@comments_count.expression
	def comments_count(cls):
		return select([func.count(Comment)]).\
				where(Comment.asset_id==cls.id).\
				label('num_comments')


	def __init__(self, apiResult):
		apiResult['media'] = [ json.dumps(i) for i in apiResult['media']]
		for key, value in apiResult.iteritems():
			setattr(self, key, value)

	def __repr__(self):
		return '<URL {}>'.format(self.url)

class ArticleSchema(Schema):

	#self links
	def get_top_level_links(self, data, many):
		if many:
			self_link = "/articles/"
		else:
			self_link = "/articles/{}".format(data['id'])
		return {'self': self_link}

	class Meta:
		type_ = 'articles'
		comments = fields.Nested('CommentSchema',many=True)
		# url = fields.Str()

		fields = ('id','url','adx_keywords','section','type','title','abstract',
			'published_date','comments_count','byline','media',
			'des_facet','org_facet','per_facet','geo_facet')




class Comment(db.Model):
	__tablename__ = 'comments'

	approveDate = db.Column(db.String)
	commentBody = db.Column(db.String)
	commentID = db.Column(db.Integer, primary_key=True)
	commentSequence = db.Column(db.Integer)
	commentTitle = db.Column(db.String)
	commentType = db.Column(db.String)
	createDate = db.Column(db.String)
	depth = db.Column(db.Integer)
	editorsSelection = db.Column(db.Boolean)
	parentID = db.Column(db.Integer, db.ForeignKey('comments.commentID'))
	parentUserDisplayName = db.Column(db.String)
	permID = db.Column(db.String)
	picURL = db.Column(db.String)
	recommendations = db.Column(db.Integer)
	replies = db.relationship("Comment")
	replyCount = db.Column(db.Integer)
	reportAbuseFlag = db.Column(db.String)
	status = db.Column(db.String)
	trusted = db.Column(db.Integer)
	updateDate = db.Column(db.String)
	userID = db.Column(db.Integer)
	userDisplayName = db.Column(db.String)
	userTitle = db.Column(db.String)
	userURL = db.Column(db.String)
	userLocation = db.Column(db.String)
	assetID = db.Column(BIGINT, db.ForeignKey('articles.id'))
	article = db.relationship("Article", back_populates="comments")


	def __init__(self, apiResult, assetID):
		try:
			if 'replies' in apiResult:
				del apiResult['replies']
			self.assetID = assetID
			for key, value in apiResult.iteritems():
				setattr(self, key, value)
		except Exception as e:
			pdb.set_trace()
			print apiResult
			print e

	def __repr__(self):
		return '<Commentid {}>'.format(self.commentID)

class CommentSchema(Schema):
		#self links
	class Meta:
		type_ = 'comments'
		fields = ('commentBody','commentID','createDate', 'commentTitle',
		  'editorsSelection', 'recommendations','userDisplayName', 'userLocation' )


class Assignment(db.Model, CRUD):
  __tablename__ = 'assignments'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255), nullable=False, unique=True)
  title = db.Column(db.String(255))
  description = db.Column(db.Text)
  created_on = db.Column(db.DateTime, nullable=False)
  edited_on = db.Column(db.DateTime, nullable=False)
  creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  creator = db.relationship("User", back_populates="assignments")
  creator_name = db.Column(db.String(255), nullable=False)
  submissions = db.relationship('Submission', backref='assignments') #lazy=True
  themes = db.relationship('Theme', backref='assignments')
  #submissions = db.relationship('Address', lazy='select', backref=db.backref('person', lazy='joined'))

  def __init__(self, name, title, desc, creator_id, creator_name):
    self.name = name
    self.title = title
    self.description = desc
    self.creator_id = creator_id
    self.created_on = datetime.datetime.now()
    self.edited_on = datetime.datetime.now()
    self.creator_name = creator_name

  def get_id(self):
    return self.id

  def __repr__(self):
    return '<id {}>'.format(self.id)


class AssignmentSchema(Schema):
  not_blank = validate.Length(min=1, error='Field cannot be blank')
  id = fields.Integer(dump_only=False)
  name = fields.Str()
  title = fields.Str()
  created_on = fields.DateTime()
  creator_id = fields.Integer()
  creator_name = fields.Str()
  description = fields.Str()

  # self links
  def get_top_level_links(self, data, many):
    if many:
      self_link = "/assignments/"
    else:
      self_link = "/assignments/{}".format(data['id'])
    return {'self': self_link}

  class Meta:
    type_ = 'assignments'
    fields = ('id', 'name', 'title', 'description', 'created_on', 'creator_id', 'creator_name')

class Theme(db.Model, CRUD):
  __tablename__ = 'themes'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
  themeName = db.Column(db.String, unique=True)
  color = db.Column(db.String)
  themeSentences = db.Column(db.Text)
  __table_args__ = (db.UniqueConstraint('assignment_id', 'color'), )

  #themeSentences = db.relationship('ThemeSentence', backref='themes')

  def __init__(self, themeName, themeSentences, assignment_id, color):
    self.themeName = themeName
    self.themeSentences = themeSentences
    self.assignment_id = assignment_id
    self.color = color

class ThemeSchema(Schema):
  class Meta:
    type = 'themes'
    fields = ('id', 'themeName', 'themeSentences', 'assignment_id', 'color')

class ThemeAssignmentJoinSchema(Schema):
  class Meta:
    fields = ('id', 'assignment_id', 'themeName', 'themeSentences', 'name', 'title', 'color')

class SubmissionAssignmentJoinSchema(Schema):
  class Meta:
    fields = ('submissionID', 'assignmentID', 'submissionName', 'submissionBody', 'name', 'title')

class ThemeSentence(db.Model):
  __tablename__ = 'themesentences'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  sentence = db.Column(db.String)
  #theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'))

class ThemeSentenceSchema(Schema):
  class Meta:
    type='themesentences'
    fields = ('sentence', 'theme_id')


class Submission(db.Model, CRUD):
  __tablename__ = 'submissions'
  submissionDate = db.Column(db.String)
  submissionName = db.Column(db.String)
  submissionBody = db.Column(db.Text)
  submissionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
  userID = db.Column(db.Integer, db.ForeignKey('users.id'))
  userDisplayName = db.Column(db.String)
  assignmentID = db.Column(db.Integer, db.ForeignKey('assignments.id'))
  assignment = db.relationship("Assignment", back_populates="submissions")

  def __init__(self, name, body, assignment, userID, username):
    self.submissionDate = datetime.datetime.now()
    self.submissionName = name
    self.submissionBody = body
    self.userID = userID
    self.assignmentID = assignment
    self.userDisplayName = username

  def __repr__(self):
    return '<Submissionid {}>'.format(self.submissionID)

class SubmissionSchema(Schema):
		#self links
	class Meta:
		type_ = 'submissions'
		fields = ('submissionName','submissionBody','submissionID', 'assignmentID','submissionDate', 'userID', 'userDisplayName')

class Annotation(db.Model, CRUD):
  __tablename__ = 'annotations'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
  submissionName = db.Column(db.String)
  submissionID = db.Column(db.Integer, db.ForeignKey('submissions.submissionID'))
  sentenceIndex = db.Column(db.Integer)
  sentence = db.Column(db.Text)
  selectedTheme = db.Column(db.Integer, db.ForeignKey('themes.id'))
  annotatorID = db.Column(db.Integer, db.ForeignKey('users.id'))
  annotatorName = db.Column(db.String)
  __table_args__ = (db.UniqueConstraint('assignment_id', 'submissionID', 'sentenceIndex', 'annotatorID' ), )

  def __init__(self, assignment_id, submissionID, sentenceIndex, selectedTheme, annotatorID, sentence, submissionName=None, annotatorName=None):
    self.assignment_id = assignment_id
    self.submissionID = submissionID
    self.sentenceIndex = sentenceIndex
    self.selectedTheme = selectedTheme
    self.annotatorID = annotatorID
    self.sentence = sentence
    self.annotatorName = annotatorName
    self.submissionName = submissionName

class AnnotationSchema(Schema):
  class Meta:
    type = 'annotations'
    fields = ('id', 'assignment_id', 'submissionName', 'submissionID', 'sentenceIndex', 'sentence', 'selectedTheme', 'annotatorID', 'annotatorName')
