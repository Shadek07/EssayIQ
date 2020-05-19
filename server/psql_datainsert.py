import psycopg2
import glob
connection = psycopg2.connect(
    host="localhost",
    database="conceptvectorDB",
    port='5432',
    user="postgres",
    password='postgres',
)
connection.autocommit = True

'''cur = connection.cursor()
cur.execute("SELECT * from  themes")
rows = cur.fetchall()
for row in rows:
    print row'''

cursor = connection.cursor()
cursor.execute("Select * FROM submissions LIMIT 0")
colnames = [desc[0] for desc in cursor.description]
print colnames

files = glob.glob('./StudentEssay/M2V3/*.txt')
for i, file in enumerate(files):
    f = open(file, mode='r')
    all_of_it = f.read()
    username = 'shadek'
    cursor.execute("""INSERT INTO submissions ("userDisplayName", "submissionName", "submissionBody", "userID", "assignmentID") values (%s, %s, %s, %s, %s)""", ('shadek', file[file.rfind('/')+1:], all_of_it, 1, 1))


files = glob.glob('./StudentEssay/M2V2/*.txt')
for i, file in enumerate(files):
    f = open(file, mode='r')
    all_of_it = f.read()
    username = 'shadek'
    cursor.execute("""INSERT INTO submissions ("userDisplayName", "submissionName", "submissionBody", "userID", "assignmentID") values (%s, %s, %s, %s, %s)""", ('shadek', file[file.rfind('/')+1:], all_of_it, 1, 2))


files = glob.glob('./StudentEssay/M2V4/*.txt')
for i, file in enumerate(files):
    f = open(file, mode='r')
    all_of_it = f.read()
    username = 'shadek'
    cursor.execute("""INSERT INTO submissions ("userDisplayName", "submissionName", "submissionBody", "userID", "assignmentID") values (%s, %s, %s, %s, %s)""", ('shadek', file[file.rfind('/')+1:], all_of_it, 1, 3))


#to find pattern when two sentences are separated by only single '.' and no space after '.'
#nltk sentence tokenizer can't separate those sentence
'''import re
files = glob.glob('./StudentEssay/M2V2/*.txt')
for i, file in enumerate(files):
    f = open(file, mode='r')
    all_of_it = f.read()
    patterns = re.findall(r"\?\w+",all_of_it)
    if len(patterns) > 0:
        print file, patterns
'''