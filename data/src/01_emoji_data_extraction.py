import os, sys
import json, pickle
import emoji
import re

datadirectory = "/YOURDIRECTORY"

#control of file
f = "GIVE A NUMBER"
f = '3'

print('STARTING LOADING DATA')

#with open(drtin+'/freecodecamp_test.pkl','rb') as fin: #<------------ previous file
with open(os.getcwd()+datadirectory+'/freecodecamp'+str(f)+'_test.pkl','rb') as fin:
    fileddata = pickle.load(fin)


print('FINISHED LOADING DATA')

emojiset = set()
utf8set = set()
userdict = {}

for msg in fileddata:
    ###OJO!!! Last msgid from first file: '574eaf7f6bbc2d1d4df01af5'
    ###OJO!!! Last msgid from second file AROUND: '58b600e17ceae5376a526d13'
    if f == '3' and msg['id'] == '58b600e17ceae5376a526d13': #find overlapping data; if some collected, start all over
        emojiset = set()
        utf8set = set()
        userdict = {}
        continue
    try:
        lwstrpmsg = msg['text'].lower().replace('.', ' ').replace(',', ' ').replace(';', ' ').replace('!', ' ').replace('?', ' ').strip(' ')
        if msg['fromUser'] != None:
            user = msg['fromUser']['username']
        else:
            user = 'unsubscribedusers'
        datum = msg['sent'][0:10]
        msgid = msg['id']
    except:
        print('an error; skipping this message ', msg)
        continue
    if user not in list(userdict.keys()):
        userdict[user] = {}
        userdict[user]['msgids'] = {}
    if msgid not in userdict[user]['msgids']:
        userdict[user]['msgids'][msgid] = {}
        userdict[user]['msgids'][msgid]['sent'] = datum
        userdict[user]['msgids'][msgid]['text'] = None
        userdict[user]['msgids'][msgid]['exist_emoji'] = False
        userdict[user]['msgids'][msgid]['listemojis'] = []
        userdict[user]['msgids'][msgid]['setemojis'] = set()
    for tk in lwstrpmsg:
        if re.match(r'[^\w\s]',tk) != None:
            utf8set.add(tk)
        if tk in emoji.UNICODE_EMOJI:
            if userdict[user]['msgids'][msgid]['exist_emoji'] == False:
                userdict[user]['msgids'][msgid]['exist_emoji'] = True
                userdict[user]['msgids'][msgid]['text'] = msg['text']
            #print(tk)
            emojiset.add(tk)
            userdict[user]['msgids'][msgid]['listemojis'].append(tk)
            userdict[user]['msgids'][msgid]['setemojis'].add(tk)

emojidata = {}

emojidata['emojiset'] = emojiset
emojidata['utf8set'] = utf8set
emojidata['userdict'] = userdict


with open(os.getcwd()+datadirectory+'/emojiproject0'+str(f)+'.pkl','wb') as fout:
    pickle.dump(emojidata, fout)

