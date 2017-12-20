# -*- coding: UTF-8 -*-
import os, sys
import json, pickle, csv
import emoji
import re
import collections, itertools, operator
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy, pandas

datadirectory = "/YOURDIRECTORY"

emojiset = set()
utf8set = set()
userdict = dict()

print('STARTING LOADING DATA')

with open(os.getcwd()+datadirectory+'/emojidb.pkl','rb') as fin:
    emojidb = pickle.load(fin)

csvdataset = pandas.read_csv(os.getcwd()+datadirectory+'/emojiprojecttotal.csv')


print('FINISHED LOADING DATA')

emojis_dataset = emojidb['emojis_dataset']
emojiset = emojidb['emojiset']
utf8set = emojidb['utf8set']
userdict = emojidb['userdict']

print('emojis_dataset length', len(emojis_dataset))
print('utf8set length', len(utf8set))
print('emojiset length', len(emojiset))
print('userdict length', len(userdict))
print('emojiset\n', emojiset)

############################################################################
#min date / max date (forgot to check this before... sorry for the following brute force full search)
############################################################################
mindate = '2018-12-31'
maxdate = '2010-01-01'

for user in userdict:
    if len(userdict[user]['msgids']) > 0:
        for msgid in userdict[user]['msgids']:
            if userdict[user]['msgids'][msgid]['sent'] <= mindate:
                mindate = userdict[user]['msgids'][msgid]['sent']
            if userdict[user]['msgids'][msgid]['sent'] >= maxdate:
                maxdate = userdict[user]['msgids'][msgid]['sent']

print("mindate : {0}, maxdate : {1}".format(mindate, maxdate))

#sys.exit()

############################################################################
#counting number of active / no-active emojiers against total active users
############################################################################

count_activeusers = 0
count_emojieractive = 0
count_emojiernotactive = 0
for user in userdict:
    if len(userdict[user]['msgids']) > 10:
        count_activeusers += 1
        for mid in userdict[user]['msgids']:
            if userdict[user]['msgids'][mid]['exist_emoji']:
                count_emojieractive += 1
                break
    else:
        for mid in userdict[user]['msgids']:
            if userdict[user]['msgids'][mid]['exist_emoji']:
                count_emojiernotactive += 1
                break        

val = count_emojiernotactive+count_emojieractive
print("number of active users: {0}\nnumber of active emojiers: {1}\nnumber of nonactive emojiers: {2}\n\nactive emojiers vs total active: {3:.1%}\nactive+nonactive emojiers vs total active: {4:.1%}"
    .format(
    count_activeusers,
    count_emojieractive,
    count_emojiernotactive,
    count_emojiernotactive/count_activeusers,
    val/count_activeusers))


############################################################################
#collective vocabulary
############################################################################

print("number of emojis used collectively by emojiers during the period: {0}".format(len(emojiset)))

#calculating individual vocabularies
indvoc = collections.defaultdict(set) #set will give an error (https://stackoverflow.com/questions/23577724/type-error-unhashable-typeset)
for user in userdict:
    if len(userdict[user]['msgids']) > 0:
        for mid in userdict[user]['msgids']:
            if userdict[user]['msgids'][mid]['exist_emoji']:

                indvoc[user] = indvoc[user] | userdict[user]['msgids'][mid]['setemojis']

print('indvoc length', len(indvoc))

############################################################################
#average vocabulary size, min and max individual vocabulary
############################################################################
maxindvoc = 0
minindvoc = float("inf")
sumindvoc = 0

print("min voc : {0}\nmax voc : {1}".format(len(sorted(indvoc.items(), key=lambda x: len(x[1]))[0][1]), len(sorted(indvoc.items(), key=lambda x: len(x[1]))[-1][1])))

for user in indvoc:
    sumindvoc += len(indvoc[user])
    
print("average vocabulary : {0:.1f}".format(sumindvoc/len(indvoc)))

#creating the tables for the billboard
#https://stackoverflow.com/questions/993358/creating-a-range-of-dates-in-python

##Observations:
##there are many ways to set monthly batches that are more programatic, for example
##https://stackoverflow.com/questions/34898525/generate-list-of-months-between-interval-in-python/34899127
##
##but if you know something about the problem that is not going to change anyway, why not to use it?
##


billboard = dict()

#months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
date_generated_ymonth = []

for y in range(2014, 2018):
    if y == 2014:
        date_generated_ymonth.append(str(y)+'-Dec')
        continue
    for m in months:
        date_generated_ymonth.append(str(y)+'-'+m)

print(date_generated_ymonth)

for em in emojiset:
    billboard[em] = collections.OrderedDict()
    for ym in date_generated_ymonth:                        #<--- by using this range in advance, I can add ALL dates to each character
        billboard[em].update({ym:{'count':0, 'order':-1}})

for user in userdict:
    if len(userdict[user]['msgids']) > 0:
        for mid in userdict[user]['msgids']:
          if userdict[user]['msgids'][mid]['exist_emoji']:
            for em in userdict[user]['msgids'][mid]['listemojis']:
                msgdate = userdict[user]['msgids'][mid]['sent']
                if msgdate[:7] in date_generated_ymonth:
                    billboard[em][ msgdate[:7] ]['count'] += 1



for ym in date_generated_ymonth:
    #print('Y-MONTH ', ym)
    tempdict = collections.defaultdict(int)
    for em in emojiset:
        tempdict[em] = billboard[em][ym]['count'] #create a dict only for emoji counts for that week
        if billboard[em][ym]['count'] > 0:
            #print(em, week, billboard[em][week]['count'])
            pass
    prev_c = 0
    o = 0
    #print(sorted(tempdict.items(), key = lambda x: x[1], reverse = True)[:6])
    if ym == '2015-Jul':
        #break
        pass
    for i, val in enumerate(sorted(tempdict.items(), key = lambda x: x[1], reverse = True)): #order the emojis based on counts of that week
        emojilist = list(billboard.keys())
        if val[0].encode('unicode_escape').decode('utf8') in ['\\u262f', '\\u2744', '\\U0001f525']: # 'CHAR'.encode('unicode_escape').decode('utf8'); these were considered outliers
            continue
        c = val[1]
        if c == 0:       #if no more counts, break
            break
        if i == 0:          #if counts and first, initialize order and prev_val
            o = 1
            prev_c = c
        if prev_c != c: #if current val different to prev_val, update o and prev_val
            o += 1
            prev_c = c
        if o == 6:          #trying to report only those first 5 places the most
            break    
        #print(i, val, o, prev_val)
        #print(billboard[em][week]['order'])
        billboard[val[0]][ym]['order'] = o
        #print(ym, val[0], billboard[val[0]][ym]['order'])
  

print('billboard length', len(billboard))

for em in emojiset: #now let's keep only the records that had at least one assignment in the ordering at any point of the study
    has_o = False
    for ym in date_generated_ymonth:
        if billboard[em][ym]['order'] != -1:
            has_o = True
            #print(em)
            break
    if has_o == False:
        del billboard[em]
       #pass

print('billboard length', len(billboard))




############################################################################
#added analyses and figures
############################################################################

### pies without outliers
nooutliers = (csvdataset['CLRDname'] != ':snowflake:') & (csvdataset['CLRDname'] != ':fire:') & (csvdataset['CLRDname'] != ':yin_yang:') & (csvdataset['CLRDname'] != ':trade_mark:')

csvdataset[nooutliers].groupby('unicodeorgbigclass')['unicodeorgbigclass'].count().plot(kind='pie')
plt.axis('equal')
plt.show()

csvdataset[nooutliers].groupby('unicodeorgbigclass')['count'].sum().plot(kind='pie')
plt.axis('equal')
plt.show()

csvdataset[nooutliers].groupby('unicodeorgmediumclass')['unicodeorgmediumclass'].count().plot(kind='pie')
plt.axis('equal')
plt.show()


csvdataset[nooutliers].groupby('unicodeorgmediumclass')['count'].sum().plot(kind='pie')
plt.axis('equal')
plt.show()

csvdataset[(csvdataset['unicodeorgbigclass']=='Symbols') & nooutliers].groupby('unicodeorgmediumclass')['count'].sum().plot(kind='pie')
plt.axis('equal')
plt.show()

###quick frequency table of Symbols category

print(csvdataset[nooutliers].groupby('unicodeorgmediumclass')['count'].sum().order(ascending=False))

print(csvdataset[(csvdataset['unicodeorgbigclass']=='Symbols') & nooutliers].groupby('unicodeorgmediumclass')['count'].sum().order(ascending=False))


###frequency bar chart of emoji counts, without outliers 

count_emojis = collections.defaultdict(list)

for em in emojis_dataset:
    count_emojis[emojis_dataset[em]['count']].append(em)

count_emojis = sorted(count_emojis.items(), key=operator.itemgetter(0))

ylabels = []
for counte in count_emojis:
    if len(counte[1]) == 1:
        ylabels.append(counte[1][0])
    else:
        ylabels.append(str(len(counte[1]))+' emojis')

fig, ax = plt.subplots()
ax.set_ylim(bottom=-1, top=len(count_emojis))
plt.yticks(fontname = "symbola")
ax.barh([y for y in range(len(count_emojis))][2:], [xemo[0] for xemo in count_emojis][:-2], align='center', tick_label=ylabels[:-2] )
plt.show()

###list of top 20 most popular emojis

print(count_emojis[-20:])

