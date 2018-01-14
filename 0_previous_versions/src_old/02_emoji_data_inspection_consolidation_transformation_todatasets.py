import os, sys
import json, pickle, csv
import emoji
import collections, operator
import pandas

datadirectory = "/YOURDIRECTORY"

emojiset = set()
utf8set = set()
userdict = dict()

print('STARTING LOADING DATA')

for ix in range(1,4):

    with open(os.getcwd()+datadirectory+'/emojiproject0'+str(ix)+'.pkl','rb') as fin:
        emojidata = pickle.load(fin)

    emojiset = emojiset | emojidata['emojiset']
    utf8set = utf8set | emojidata['utf8set']
    if len(userdict) == 0:
        userdict = emojidata['userdict']
    else:
        for user in emojidata['userdict']:
            if user in list(userdict.keys()):
                #if exists, update its nested msgids with new values, they are believed to be unique and not in the previous dict
                for msg in emojidata['userdict'][user]['msgids']:
                    userdict[user]['msgids'][msg] = emojidata['userdict'][user]['msgids'][msg]
            else:
                #otherwise add the value to the parent dict
                userdict[user] = emojidata['userdict'][user]
            assert user != 'msgids'
        
print('FINISHED LOADING DATA')

print('utf8set length', len(utf8set))
print('emojiset length', len(emojiset))
print('userdict length', len(userdict))


count_activeusers = 0
count_emojiusers = 0

for user2 in userdict:
    if len(userdict[user2]['msgids']) > 10:
        count_activeusers += 1
        for mid in userdict[user2]['msgids']:
            if userdict[user2]['msgids'][mid]['exist_emoji']:
                count_emojiusers += 1
                break

emojis_dataset = dict([(em,{'CLRDname':'', 'Index':'', 'count':0, 'total': 0, 'posnetneg':'', 'unicodeorgmediumclass': '', 'unicodeorgbigclass': '', 'UnicodeAbstraction': '', 'first':'2018-12-31', 'last':'2010-01-01', 'unicodeyear':'', 'userunknown':False}) for em in emojiset])

for em in emojis_dataset:
    emojis_dataset[em]['CLRDname'] = emoji.UNICODE_EMOJI[em]

for u in userdict:
    for mid in userdict[u]['msgids']:
        if userdict[u]['msgids'][mid]['exist_emoji']:
            for em in userdict[u]['msgids'][mid]['setemojis']:
                emojis_dataset[em]['count'] += 1
            for em in userdict[u]['msgids'][mid]['listemojis']:
                emojis_dataset[em]['total'] += 1
            if userdict[u]['msgids'][mid]['sent'] <= emojis_dataset[em]['first']:
                emojis_dataset[em]['first'] = userdict[u]['msgids'][mid]['sent']
            if userdict[u]['msgids'][mid]['sent'] >= emojis_dataset[em]['last']:
                emojis_dataset[em]['last'] = userdict[u]['msgids'][mid]['sent']
            if u == 'unsubscribedusers':
                emojis_dataset[em]['userunknown'] = True


import requests
from bs4 import BeautifulSoup
from collections import OrderedDict


url = 'http://www.unicode.org/emoji/charts/emoji-list.html'


response = requests.get(url)
response.raise_for_status()
soup1 = BeautifulSoup(response.text, "html.parser")

header = [
    'Index', 'Code', 'Sample', 'CLR_Name', 'keywords', 'BigHead', 'MediumHead', 'UnicodeAbstraction'
]

output = {}
currentbighead = ''
currentmediumhead = ''
count_rows = 0
output = {}
for row in soup1.find('table').find_all('tr'):
    count_rows += 1
    if count_rows > 5:
        #break
        pass
    if row.find("th",{"class":"bighead"}):
        currentbighead = row.find("th",{"class":"bighead"}).text
    if row.find("th",{"class":"mediumhead"}):
        currentmediumhead = row.find("th",{"class":"mediumhead"}).text
    if row.find("td"):
        cols = row.find_all('td')
        print("len of row.find_all('td') = ", len(cols))
        cols = [e.text.strip() for e in cols]
        cols = cols + [currentbighead, currentmediumhead, '']
        d = {}
        d = OrderedDict(zip(header, [e.strip() for e in cols]))
        print(d)
        if d:
            _code = []
            for c in d['Code'].split(' '):
                if len(c) == 6:
                    _code.append(c.replace('+', '0000'))
                else:
                    _code.append(c.replace('+', '000'))
            code = ' '.join(_code)
            name = d['CLR_Name'].replace(' ', '_') \
                            .replace(':', '') \
                            .replace(',', '') \
                            .replace('"', '') \
                            .replace('"', '') \
                            .strip()
            char = "u'" + code.replace('U', '\\U') + "',"
            d['UnicodeAbstraction'] = char
            d['CLR_Name'] = name
            output[name] = d
        else:
            print(d)
            
url = 'http://unicode.org/emoji/charts-11.0/emoji-versions-sources.html'
response = requests.get(url)
response.raise_for_status()
soup2 = BeautifulSoup(response.text, "html.parser")

years = list(range(1994,2018))


yearoutput = {}
count = 0
for row in soup2.find('table').find_all('tr'):
    count += 1
    year = '-'
    if count > 5:
        #break
        pass
    if row.find_all('td'):
        
        if int(row.find_all('td')[0].text) in years:
            year = row.find_all('td')[0].text
        if not row.find_all('td', {'class':'lchars'}):
            continue
        allu = []
        for x in [a['href'].split('#')[1].split('_') for a in row.find_all('td', {'class':'lchars'})[0].find_all('a')]:
            allu.extend(x)
        allu = ['\\U0000'+x if len(x) == 4 else '\\U000'+x for x in set(allu)]
        for emoj in allu:
            yearoutput[emoj] = year


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

            
count_matches = 0
l_yearoutkeys_encoded = [em.encode('utf-8').decode('unicode_escape') for em in yearoutput]
l_yearoutkeys = list(yearoutput.keys())
for em_char in emojiset:
    _code = em_char.encode('unicode_escape').decode('utf-8')
    if len(_code) == 6:
       _code = _code.replace('\\u', '\\U0000')
    elif len(_code) == 7:
       _code = _code.replace('\\u', '\\U000')
    elif len(_code) not in [6,7]:
        print("got a problem with this _code : ", _code.upper(), em_char)
    if em_char in emojiset:
        if _code in l_yearoutkeys:
        #if em_char in l_yearoutkeys_encoded:
            emojis_dataset[em_char]['unicodeyear'] = yearoutput[_code]
        for k in output:
            if _code.upper() in output[k]['UnicodeAbstraction']:
                gotit = True
                print(_code.upper(), ' correctly matched to output!')
 
                emojis_dataset[em_char]['unicodeorgbigclass'] = output[k]['BigHead']
                emojis_dataset[em_char]['unicodeorgmediumclass'] = output[k]['MediumHead']
                emojis_dataset[em_char]['UnicodeAbstraction'] = output[k]['UnicodeAbstraction']
                emojis_dataset[em_char]['Index'] = output[k]['Index']
                count_matches += 1
                break
        if gotit == False:
            print("this em is not referring to output correctly ", _code.upper(), em_char)

with open(os.getcwd()+datadirectory+'/emojiprojecttotal.csv','w') as f_out:
    writer = csv.writer(f_out)
    writer.writerow(['emoji','CLRDname','Index','count','first','last','posnetneg','total','unicodeorgmediumclass', 'unicodeorgbigclass', 'unicodeyear','userunknown','UnicodeAbstraction'])
    for em in emojis_dataset:
        writer.writerow([em.encode('unicode_escape').decode('utf-8'),
                         emojis_dataset[em]['CLRDname'],
                         emojis_dataset[em]['Index'],
                         emojis_dataset[em]['count'],
                         emojis_dataset[em]['first'],
                         emojis_dataset[em]['last'],
                         emojis_dataset[em]['posnetneg'],
                         emojis_dataset[em]['total'],
                         emojis_dataset[em]['unicodeorgmediumclass'],
                         emojis_dataset[em]['unicodeorgbigclass'],
                         emojis_dataset[em]['unicodeyear'],
                         emojis_dataset[em]['userunknown'],
                         emojis_dataset[em]['UnicodeAbstraction']])

with open(os.getcwd()+datadirectory+'/emojidb.pkl','wb') as fout:
    emojidb = {}
    emojidb['emojis_dataset'] = emojis_dataset
    emojidb['emojiset'] = emojiset
    emojidb['utf8set'] = utf8set
    emojidb['userdict'] = userdict
    pickle.dump(emojidb, fout)


finaldataset = pandas.read_csv(os.getcwd()+datadirectory+'/emojiprojecttotal.csv')
