import os.path
import io
import re
import time
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.metrics import confusion_matrix
import collections
#import constants
#import lcs
import string
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
#import bokeh_utils
from itertools import compress, product
import ast
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import cohen_kappa_score


#all different combinations of a list
def get_combinations(items):
    return ( set(compress(items,mask)) for mask in product(*[[0,1]]*len(items)) )
#import mpld3

plt.rcParams['figure.figsize'] = (40,40)
#plt.locator_params(axis='y', nbins=3)

#print(mp.keys())
#print(mp.values())

essayiq = []
cnt = 0

essayiqarray = []


#filestr = '_1_coach_7sentsize_10dist_0.6run_2'
#filestr = '_2_coach_7sentsize_15dist_0.7run_2'
filestr = '_3_coach_7sentsize_10dist_0.7run_2'

with open('essayiq' + filestr + '.txt') as fp:
      cnt = 0
      prev = ""
      for line in fp:
        if len(line) < 10:
          continue
        data = ast.literal_eval(line)
        themeid = data['themeid']
        essayiqarray.append([cnt, data['sentenceindex'], data['submissionname'], data['themeMarker'],data['sentence'],data['color']])
        #essayiq.append([cnt, data['sentenceindex'], data['submissionname'], data['themeMarker'],data['sentence'],data['color']])
        if prev != data['submissionname']:
            cnt += 8
            prev = data['submissionname']
#dfessayiq = pd.DataFrame(essayiq,columns=['submission','sentenceindex','submissionname','themeMarker','sentence','color'])         


phrase2vecarray = []
with open('phrase2vec' + filestr + '.txt') as fp:
      cnt = 0
      prev = ""
      for line in fp:
        if len(line) < 10:
          continue
        data = ast.literal_eval(line)
        themeid = data['themeid']
        phrase2vecarray.append([cnt, data['sentenceindex'], data['submissionname'], data['themeMarker'],data['sentence'],data['color']])
        #essayiq.append([cnt, data['sentenceindex'], data['submissionname'], data['themeMarker'],data['sentence'],data['color']])
        if prev != data['submissionname']:
            cnt += 8
            prev = data['submissionname']
print(len(phrase2vecarray))
goldarray = []
with open('essayiqgold' + filestr + '.txt') as fp:
      cnt = 2
      prev = ""
      for line in fp:
        if len(line) < 10:
          continue
        data = ast.literal_eval(line)
        themeid = data['themeid']
        goldarray.append([cnt, data['sentenceindex'], data['submissionname'], data['themeMarker'], data['sentence'],data['color']])
        if prev != data['submissionname']:
            cnt += 8
            prev = data['submissionname']


#combined
#df = pd.DataFrame(essayiq,columns=['submission','sentenceindex','submissionname','themeMarker','sentence','color']) 
#only gold standard
#dfgold = pd.DataFrame(goldarray,columns=['submission','sentenceindex','submissionname','themeMarker','sentence','color'])

#dfessayiq['match'] = np.where(dfessayiq['submissionname'] == dfgold['submissionname'] & dfessayiq['sentenceindex'] == dfgold['sentenceindex'], 'True', 'False')

#plot1 = bokeh_utils.scatter_with_hover(df, 'submission', 'sentenceindex',fig_width=1000, fig_height=600, cols=['submission','sentenceindex','submissionname','themeMarker','sentence','color'])
#bokeh_utils.draw_multiple_plot(plot1)
#print(confusion_matrix(y_true, y_pred, labels=["ant", "cat", "bird"]))
candidate_sentences = dict()
with open('candidate_sentences' + filestr + '.txt') as fp:
    for line in fp:
        if len(line) < 10:
          continue
        data = ast.literal_eval(line)
        candidate_sentences[(data['sentenceindex'], data['submissionname'])] = 1
#themelabels = ['Culture in a working environment','Learning','Non-blaming culture','Administrative leadership','Humility']
#themelabels = ['Fast Paced environment','Short Staffing','Home life responsibilities','Negative Impact on Patient Safety','Utilization of IAMSAFE Checklist']
themelabels = ['Examples of bad designs similar to the "tricky doors"','Impacts from bad designs','Barriers to improvement to non-user-friendly design','Mis-attribution of user errors caused by bad designs', 'Workplace examples of bad and good design']


##### Comparison between EssayIQ and Gold Standard ######
both_match_with_theme = 0
both_match_with_none = 0
mismatch = 0
marked_by_essayiq_only = 0
markedbycoach_only = 0

predicted_themes_by_essayiq = []
annotator_themes = []

candidate_sentence_cnt = 0
essay_level_themes_essayiq = dict() #
essay_level_themes_annotation = dict()
candidate_lines = set() #store line numbers from goldarray
for i, row1 in enumerate(essayiqarray):
    not_in_golddata = True #check if any sentence was not annotated by coach, but essayiq marked it
    for j, row2 in enumerate(goldarray):
        if row1[1] == row2[1] and row1[2] == row2[2]: #same sentence from same submission, row1 is essayiq prediction, row2 is annotation labelling 
            not_in_golddata = False
            if (row1[1], row1[2]) in candidate_sentences:
                candidate_sentence_cnt += 1
                candidate_lines.add(j)
                continue
            if row1[5] == row2[5]:
                both_match_with_theme += 1
                predicted_themes_by_essayiq.append(row1[3])
                annotator_themes.append(row2[3])
                
                #essaylevel theme existence
                if row1[2] in essay_level_themes_essayiq:
                    essay_level_themes_essayiq[row1[2]].append(row1[3])
                else:
                    essay_level_themes_essayiq[row1[2]] =  [row1[3]] #set([row1[3]])
                if row2[2] in essay_level_themes_annotation:
                    essay_level_themes_annotation[row2[2]].append(row2[3])
                else:
                    essay_level_themes_annotation[row2[2]] = [row2[3]] #set([row2[3]])                    
            else:
                if row1[5] != 'None':
                    mismatch += 1
                    predicted_themes_by_essayiq.append(row1[3])
                    annotator_themes.append(row2[3])                   
                    if row1[2] in essay_level_themes_essayiq:
                        essay_level_themes_essayiq[row1[2]].append(row1[3])
                    else:
                        essay_level_themes_essayiq[row1[2]] = [row1[3]] #set([row1[3]])
                    if row2[2] in essay_level_themes_annotation:
                        essay_level_themes_annotation[row2[2]].append(row2[3])
                    else:
                        essay_level_themes_annotation[row2[2]] = [row2[3]] #set([row2[3]])
                        
    if not_in_golddata:
        if row1[5] == 'None':
            both_match_with_none += 1
        else:
            marked_by_essayiq_only += 1          
for j, row2 in enumerate(goldarray):
    if j in candidate_lines:
        continue
    in_essayiq = False
    for i, row1 in enumerate(essayiqarray):
        if row1[1] == row2[1] and row1[2] == row2[2]:
            in_essayiq = True if row1[5] != 'None' else False
            break
    if in_essayiq == False:
        markedbycoach_only += 1

print ('experiment settings for USE')
print ('both hit:', both_match_with_theme)
print('mismatch when marked by both essayiq and annotator', mismatch) 
print('both miss:',both_match_with_none)
print('marked by only essayiq:', marked_by_essayiq_only)
print('marked by coach only:', markedbycoach_only)      
print ('candidate sentences: ', candidate_sentence_cnt)


mat = confusion_matrix(annotator_themes, predicted_themes_by_essayiq,labels=themelabels)
#print(themelabels)
#print (mat)
'''df_cm = pd.DataFrame(mat, index=themelabels, columns=themelabels)
plt.figure(figsize=(10,7))
sn.set(font_scale=1) # for label size
sn.heatmap(df_cm, annot=True, annot_kws={"size": 10}) # font size
#plt.show()'''

y_true = pd.Series(annotator_themes)
y_pred = pd.Series(predicted_themes_by_essayiq)

pd.crosstab(y_true, y_pred, rownames=['True'], colnames=['Predicted'], margins=True)
#pd.crosstab(y_true, y_pred, rownames=['True'], colnames=['Predicted']).apply(lambda r: 100.0 * r/r.sum() )
cohen_score = cohen_kappa_score(annotator_themes, predicted_themes_by_essayiq)
print ('kappa score: ', cohen_score)

#essaylevel theme existence experiment
thememap = dict()
for i,label in enumerate(themelabels):
    thememap[label] = i

essayiqvalues = []
annotatorvalues = []
essayiqvalues2 = [] #this array takes care of how many sentences contain a certain theme
annotatorvalues2 = [] #this array takes care of how many sentences contain a certain theme
for submission in essay_level_themes_essayiq:
    arr = [0]*len(themelabels)
    arr2 = [0]*len(themelabels)
    for theme in essay_level_themes_essayiq[submission]:
        arr[thememap[theme]] = 1
        arr2[thememap[theme]] += 1
    essayiqvalues.extend(arr)
    essayiqvalues2.extend(arr2)

for submission in essay_level_themes_annotation:
    arr = [0]*len(themelabels)
    arr2 = [0]*len(themelabels)
    for theme in essay_level_themes_annotation[submission]:
        arr[thememap[theme]] = 1
        arr2[thememap[theme]] += 1
    annotatorvalues.extend(arr)
    annotatorvalues2.extend(arr2)
print (len(essayiqvalues), len(annotatorvalues))
cohen_score = cohen_kappa_score(annotatorvalues, essayiqvalues)
print ('essay level kappa score: ', cohen_score)

cohen_score = cohen_kappa_score(annotatorvalues2, essayiqvalues2, weights='quadratic')
print ('essay level kappa score (with weights): ', cohen_score)


##### Comparison between Phrase2vec and Gold Standard  ####
both_match_with_theme = 0
both_match_with_none = 0
mismatch = 0
marked_by_phrase2vec_only = 0
markedbycoach_only = 0

predicted_themes_by_phrase2vec = []
annotator_themes = []

essay_level_themes_phrase = dict() #
essay_level_themes_annotation = dict()

candidate_sentence_cnt = 0
candidate_lines = set()
for i, row1 in enumerate(phrase2vecarray):
    not_in_golddata = True #check if any sentence was not annotated by coach, but phrase2vec marked it
    for j, row2 in enumerate(goldarray):
        if row1[1] == row2[1] and row1[2] == row2[2]: #same sentence from same submission, row1 is phrase2vec prediction, row2 is annotation labelling 
            not_in_golddata = False
            if (row1[1], row1[2]) in candidate_sentences:
                candidate_lines.add(j)
                candidate_sentence_cnt += 1
                continue
            if row1[5] == row2[5]:
                both_match_with_theme += 1
                predicted_themes_by_phrase2vec.append(row1[3])
                annotator_themes.append(row2[3])
                
                #essaylevel theme existence
                if row1[2] in essay_level_themes_phrase:
                    essay_level_themes_phrase[row1[2]].append(row1[3])
                else:
                    essay_level_themes_phrase[row1[2]] = [row1[3]] #set([row1[3]])
                if row2[2] in essay_level_themes_annotation:
                    essay_level_themes_annotation[row2[2]].append(row2[3])
                else:
                    essay_level_themes_annotation[row2[2]] = [row2[3]] #set([row2[3]]) 
            
            else:
                if row1[5] != 'None':
                    mismatch += 1
                    predicted_themes_by_phrase2vec.append(row1[3])
                    annotator_themes.append(row2[3])
                    
                    if row1[2] in essay_level_themes_phrase:
                        essay_level_themes_phrase[row1[2]].append(row1[3])
                    else:
                        essay_level_themes_phrase[row1[2]] = [row1[3]] #set([row1[3]])
                    if row2[2] in essay_level_themes_annotation:
                        essay_level_themes_annotation[row2[2]].append(row2[3])
                    else:
                        essay_level_themes_annotation[row2[2]] = [row2[3]] #set([row2[3]])
            
    if not_in_golddata:
        if row1[5] == 'None':
            both_match_with_none += 1
        else:
            marked_by_phrase2vec_only += 1

for j, row2 in enumerate(goldarray):
    in_phrase2vec = False
    if j in candidate_lines:
        continue
    for i, row1 in enumerate(phrase2vecarray):       
        if row1[1] == row2[1] and row1[2] == row2[2]:
            in_phrase2vec = True if row1[5] != 'None' else False
            break
    if in_phrase2vec == False:
        markedbycoach_only += 1
        
print('experment settings for phrase2vec:')

print ('both hit:', both_match_with_theme)
print('mismatch when marked by both phrase2vec and annotator', mismatch) 
print('both miss:',both_match_with_none)
print('marked by only phrase2vec:', marked_by_phrase2vec_only)
print('marked by coach only:', markedbycoach_only)      
print ('candidate sentences: ', candidate_sentence_cnt)

mat = confusion_matrix(annotator_themes, predicted_themes_by_phrase2vec,labels=themelabels)
#print(themelabels)
#print (mat)
'''df_cm = pd.DataFrame(mat, index=themelabels, columns=themelabels)
plt.figure(figsize=(10,7))
sn.set(font_scale=1) # for label size
sn.heatmap(df_cm, annot=True, annot_kws={"size": 10}) # font size
plt.show()'''
cohen_score = cohen_kappa_score(annotator_themes, predicted_themes_by_phrase2vec)
print ('kappa score: ', cohen_score)

#essaylevel theme existence experiment
thememap = dict()
for i,label in enumerate(themelabels):
    thememap[label] = i

phrasevalues = []
annotatorvalues = []
phrasevalues2 = [] #this array takes care of how many sentences contain a certain theme
annotatorvalues2 = [] #this array takes care of how many sentences contain a certain theme
for submission in essay_level_themes_phrase:
    arr = [0]*len(themelabels)
    arr2 = [0]*len(themelabels)
    for theme in essay_level_themes_phrase[submission]:
        arr[thememap[theme]] = 1
        arr2[thememap[theme]] += 1
    phrasevalues.extend(arr)
    phrasevalues2.extend(arr2)

for submission in essay_level_themes_annotation:
    arr = [0]*len(themelabels)
    arr2 = [0]*len(themelabels)
    for theme in essay_level_themes_annotation[submission]:
        arr[thememap[theme]] = 1
        arr2[thememap[theme]] += 1
    annotatorvalues.extend(arr)
    annotatorvalues2.extend(arr2)
print (len(phrasevalues), len(annotatorvalues))
cohen_score = cohen_kappa_score(annotatorvalues, phrasevalues)
print ('essay level kappa score: ', cohen_score)

cohen_score = cohen_kappa_score(annotatorvalues2, phrasevalues2, weights='quadratic')
print ('essay level kappa score (with weights): ', cohen_score)
