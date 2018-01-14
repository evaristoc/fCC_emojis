import os, sys, gc
import json, pickle, csv
import emoji
import re
import collections, itertools, operator
import matplotlib.pyplot as plt
import time
plt.style.use('ggplot')
import numpy, pandas

def datagathering(ix, previous_keys, current_keys, emojiset_kw, userdict_kw):
    start = time.time()
    with open(os.getcwd()+datadirectory+'/emojiproject0'+str(ix)+'_corr.pkl','rb') as fin:
        emojidata = pickle.load(fin)
    
    print("dealing with file ", ix)
    emojiset_kw = emojiset_kw | emojidata['emojiset_kw']
    current_keys = set(emojidata['userdict_kw'].keys())
    print("all people in this set ", len(current_keys))
    if not previous_keys:
        previous_keys = set(emojidata['userdict_kw'].keys())
        userdict_kw.update(emojidata['userdict_kw'])
        end = time.time()
        print("tempo : {:.0f}min {:.0f}sec".format((end-start)//60, (end-start) - (end-start)//60*60))
        start = time.time()
        print()
        print()
        del emojidata
        return previous_keys, current_keys, emojiset_kw, userdict_kw
    else:
        print("new people ", len(current_keys.difference(previous_keys)))
        for newuser in current_keys.difference(previous_keys):
            userdict_kw[newuser] = emojidata['userdict_kw'][newuser]
        print("old people ", len(current_keys.intersection(previous_keys)))
        for olduser in current_keys.intersection(previous_keys):
            userdict_kw[olduser].update(emojidata['userdict_kw'][olduser])
        end = time.time()
        print("tempo : {:.0f}min {:.0f}sec".format((end-start)//60, (end-start) - (end-start)//60*60))
        start = time.time()    
    print()
    print()
    del emojidata
    gc.collect()
    return previous_keys, current_keys, emojiset_kw, userdict_kw


#################################################################################
## start getting the files and consolidate datasets
##################################################################################


datadirectory = "/1_archive"

emojiset_kw = set()
userdict_kw = {}
current_keys = {}
previous_keys = {}

print('STARTING LOADING DATA')
print()
for ix in range(1,4):
    previous_keys, current_keys, emojiset_kw, userdict_kw = datagathering(ix, previous_keys, current_keys, emojiset_kw, userdict_kw)
print('FINISHED LOADING DATA')

print('emojiset_kw length', len(emojiset_kw))
print('userdict_kw length', len(userdict_kw))
#print('emojiset\n', emojiset)

#sys.exit()

count_activeusers = 0
count_emojiusers = 0

#################################################################################
## Outlier1: checking who the @#%$#$ is reporting more  [':warning:', ':star2:', ':star:', ':cookie:', ':sparkles:']
##################################################################################

# outliers1 = collections.defaultdict(int)
# 
# ind_outliers1 = set([':warning:', ':star2:', ':star:', ':cookie:', ':sparkles:'])
# 
# for user in userdict_kw:
#     if user == "camperbot":
#         continue
#     for mid in userdict_kw[user]:
#         if userdict_kw[user][mid]['exist_emkw']:
#             if userdict_kw[user][mid]['setemojis_kw'].intersection(ind_outliers1):
#                 outliers1[user] += 1
# 
# 
# for k, v in sorted(outliers1.items(), key=lambda x: x[1]):
#     print(k, v)
# 
# #sys.exit()


#################################################################################
## using the scraped datafiles of emojis to update current data
##################################################################################

with open(os.getcwd()+datadirectory+'/fullemoji_unicodeorg.pkl','rb') as ffull:
    fullemoji_unicodeorg = pickle.load(ffull)

fullemoji_unicodeorglist = list(fullemoji_unicodeorg.keys())
    
with open(os.getcwd()+datadirectory+'/emojiyear_unicodeorg.pkl','rb') as fyear:
    emojiyear_unicodeorg = pickle.load(fyear)

fullemoji_unicodeorglist = list(fullemoji_unicodeorg.keys())
emojiyear_unicodeorglist = list(emojiyear_unicodeorg.keys())

emojisk_dataset = dict([(emk,{
                'alias': emk,
                'conds': False,
                'inFull':False,
                'inYear':False,
                'inGithub':'No',
                'unicodeorgbigclass':'',
                'unicodeorgmediumclass':'',
                'Apple_img':'',
                'Index':'',
                'count_kw':0,
                'total_kw': 0,
                'count_kw_camperbot':0,
                'total_kw_camperbot': 0,
                'first_kw':'2018-12-31',
                'last_kw':'2010-01-01',
                'unicodeyear':'',
                'UnicodeAbstraction': '',
                'userunknown':False})for emk in emojiset_kw])

for u in userdict_kw:
    if u == "camperbot":
        #continue
        pass
    else:
        for mid in userdict_kw[u]:
            #if "camperbot" in userdict_kw[u][mid]['text']:
            #    camperbotinmsg.append(mid)
            if userdict_kw[u][mid]['exist_emkw']:
                for emk in userdict_kw[u][mid]['setemojis_kw']:
                    if len(emk) >= 3 and  sum([lt.isdigit() for lt in emk]) <= 3 and not any([lt.isupper() for lt in emk]):
                        unicodeform = emoji.emojize(emk, use_aliases=True).encode('unicode_escape').decode('utf8')
                        if '\\u' in unicodeform:
                            #print(unicodeform)
                            if len(unicodeform) == 6:
                                #pass
                                unicodeform = unicodeform.upper().replace('\\U','\\U0000')
                            if len(unicodeform) == 7:
                                pass
                                unicodeform = unicodeform.upper().replace('\\U','\\U000')
                            #print(unicodeform)
                        if unicodeform != emk:
                            #look unicodeform in unicodeorglist
                            for CLRDname in fullemoji_unicodeorglist:
                                if unicodeform.upper() in fullemoji_unicodeorg[CLRDname]['UnicodeAbstraction'] and len(fullemoji_unicodeorg[CLRDname]['UnicodeAbstraction'].split(',')) <= 2: #find match only for NOT composed unicodes 
                                    if emojisk_dataset[emk]['conds'] == False:
                                        emojisk_dataset[emk]['conds'] = True
                                    if emojisk_dataset[emk]['inFull'] == False:
                                        emojisk_dataset[emk]['Apple_img'] = fullemoji_unicodeorg[CLRDname]['Apple_img']
                                        emojisk_dataset[emk]['Index'] = fullemoji_unicodeorg[CLRDname]['Index']
                                        emojisk_dataset[emk]['unicodeorgbigclass'] = fullemoji_unicodeorg[CLRDname]['BigHead']
                                        emojisk_dataset[emk]['unicodeorgmediumclass'] = fullemoji_unicodeorg[CLRDname]['MediumHead']
                                        emojisk_dataset[emk]['UnicodeAbstration'] = unicodeform.upper()
                                        if unicodeform in emojiyear_unicodeorglist:
                                            emojisk_dataset[emk]['unicodeyear'] = emojiyear_unicodeorg[unicodeform]
                                        elif unicodeform.upper() in emojiyear_unicodeorglist:
                                            emojisk_dataset[emk]['unicodeyear'] = emojiyear_unicodeorg[unicodeform.upper()]
                                        emojisk_dataset[emk]['inFull'] = True
                                    if u != 'camperbot':
                                        if userdict_kw[u][mid]['sent'] <= emojisk_dataset[emk]['first_kw']:
                                            emojisk_dataset[emk]['first_kw'] = userdict_kw[u][mid]['sent']
                                        if userdict_kw[u][mid]['sent'] >= emojisk_dataset[emk]['last_kw']:
                                            emojisk_dataset[emk]['last_kw'] = userdict_kw[u][mid]['sent']
                                        #I had a loop in the counting sections over the setemojis_kw AGAIN!! Corrected...
                                        emojisk_dataset[emk]['count_kw'] += 1
                                        #below is slightly less efficient than a gewond loop, but more elegant
                                        emojisk_dataset[emk]['total_kw'] += len([x for x in userdict_kw[u][mid]['listemojis_kw'] if x == emk])
                                             
                                    else:
                                        emojisk_dataset[emk]['count_kw_camperbot'] += 1
                                        emojisk_dataset[emk]['total_kw_camperbot'] += len([x for x in userdict_kw[u][mid]['listemojis_kw'] if x == emk])
                                    if u == 'unsubscribedusers':
                                        emojisk_dataset[emk]['userunknown'] = True
                                    break #we found it and updated it! stop searching in the fullemoji_unicodeorglist
                            
                            #didn't find a match for the unicodeform in the unicodeorglist but has still a unicodeform
                            if emojisk_dataset[emk]['inFull'] == False:
                                if emojisk_dataset[emk]['conds'] == False:
                                    emojisk_dataset[emk]['UnicodeAbstration'] = unicodeform.upper()
                                    emojisk_dataset[emk]['conds'] = True
                                if u != 'camperbot':
                                    if unicodeform in emojiyear_unicodeorglist:
                                        emojisk_dataset[emk]['unicodeyear'] = emojiyear_unicodeorg[unicodeform]
                                    elif unicodeform.upper() in emojiyear_unicodeorglist:
                                        emojisk_dataset[emk]['unicodeyear'] = emojiyear_unicodeorg[unicodeform.upper()]
                                    if userdict_kw[u][mid]['sent'] <= emojisk_dataset[emk]['first_kw']:
                                        emojisk_dataset[emk]['first_kw'] = userdict_kw[u][mid]['sent']
                                    if userdict_kw[u][mid]['sent'] >= emojisk_dataset[emk]['last_kw']:
                                        emojisk_dataset[emk]['last_kw'] = userdict_kw[u][mid]['sent']
                                    emojisk_dataset[emk]['count_kw'] += 1
                                    emojisk_dataset[emk]['total_kw'] += len([x for x in userdict_kw[u][mid]['listemojis_kw'] if x == emk])
                                else:
                                    emojisk_dataset[emk]['count_kw_camperbot'] += 1
                                    emojisk_dataset[emk]['total_kw_camperbot'] += len([x for x in userdict_kw[u][mid]['listemojis_kw'] if x == emk])
                                if u == 'unsubscribedusers':
                                    emojisk_dataset[emk]['userunknown'] = True
                        
                        #meet conditions but alias doesn't convert into an unicodeform
                        else:
                            if emojisk_dataset[emk]['conds'] == False:
                                emojisk_dataset[emk]['conds'] = True
                            if u != 'camperbot':
                                if userdict_kw[u][mid]['sent'] <= emojisk_dataset[emk]['first_kw']:
                                    emojisk_dataset[emk]['first_kw'] = userdict_kw[u][mid]['sent']
                                if userdict_kw[u][mid]['sent'] >= emojisk_dataset[emk]['last_kw']:
                                    emojisk_dataset[emk]['last_kw'] = userdict_kw[u][mid]['sent']
                                emojisk_dataset[emk]['count_kw'] += 1
                                emojisk_dataset[emk]['total_kw'] += len([x for x in userdict_kw[u][mid]['listemojis_kw'] if x == emk])
                            else:
                                emojisk_dataset[emk]['count_kw_camperbot'] += 1
                                emojisk_dataset[emk]['total_kw_camperbot'] += len([x for x in userdict_kw[u][mid]['listemojis_kw'] if x == emk])
                            if u == 'unsubscribedusers':
                                emojisk_dataset[emk]['userunknown'] = True                        
    #                            if any([x.islower() for x in unicodeform]):
    #                                print(unicodeform)
                                    #unicodeform = unicodeform.upper()


##########################
## preliminary evaluation
##########################


findingnemo = []
for e in emojisk_dataset:
    if emojisk_dataset[e]['inFull']:
        if not any([lt.isdigit() for lt in e]):
            findingnemo.append((e, emojisk_dataset[e]['count_kw']))
print(len(findingnemo)) #480     
print(sorted(findingnemo, key=lambda x: x[1], reverse=True)[:20])

inFull = set([x[0] for x in findingnemo])

sumupdictagain = collections.defaultdict(int)

for user in userdict_kw:
    if user == 'camperbot':
        continue
    if len(userdict_kw[user]) > 0:
        for msgid in userdict_kw[user]:
            for top in inFull.intersection(userdict_kw[user][msgid]['setemojis_kw']):
                sumupdictagain[top] += 1

for i,e in enumerate(list(sumupdictagain.keys())):
    assert sumupdictagain[e] == emojisk_dataset[e]['count_kw'], "{} is not correct : sumupdictagain = {}, emojisk_dataset = {}\nvisited {} elements".format(e, sumupdictagain[e], emojisk_dataset[e]['count_kw'], i)



infullok = 0
for e in emojisk_dataset:
    if emojisk_dataset[e]['inFull']:
        infullok += 1
        
condsok = 0
for e in emojisk_dataset:
    if emojisk_dataset[e]['conds']:
        condsok += 1

print(infullok, condsok, infullok/condsok) #so far: condsok: 1706 possible emojis; infullok: 790 with apparently full data; proportion: 0.4631

infullnotok = 0
for e in emojisk_dataset:
    if emojisk_dataset[e]['conds'] and not emojisk_dataset[e]['inFull']:
        infullnotok += 1
        #print(e)
        
for e in emojisk_dataset:
    if emojisk_dataset[e]['conds'] and not emojisk_dataset[e]['inFull'] and emojisk_dataset[e]['UnicodeAbstraction'] != '':
        #infullnotok += 1
        print(e)
#empty!!! probably good...

findingnemo = []
for e in emojisk_dataset:
    if emojisk_dataset[e]['conds'] and not emojisk_dataset[e]['inFull']:
        if not any([lt.isdigit() for lt in e]):
            findingnemo.append((e, emojisk_dataset[e]['total_kw']))
print(len(findingnemo)) #480     
print(sorted(findingnemo, key=lambda x: x[1], reverse=True)[:20])

noflags = []
for e in emojisk_dataset:
    if emojisk_dataset[e]['conds'] and not emojisk_dataset[e]['inFull']:
        if not any([lt.isdigit() for lt in e]) and len(e) > 4:
            noflags.append((e, emojisk_dataset[e]['total_kw']))
print(len(noflags)) #454      
print(sorted(noflags, key=lambda x: x[1], reverse=True)[:150])


#################################################################################
## updating some of the names manually 1: updating aliases for those found in the unicodeorglist
##################################################################################

unicodeorg_alias = {
            ':donut:':':doughnut:',
            ':fu:':':middle_finger:',
            ':it:':':Italy:',
            ':es:':':Spain:',
            ':uk:':':United_Kingdom:',
            ':gb:':':United_Kingdom:',
            ':us:':':United_States:',
            ':de:':':Germany:',
            ':jp:':':Japan:',
            ':fr:':':France:',
            ':cn:':':China:',
            ':ru:':':Russia:',
            }

for emk in unicodeorg_alias:
    _emk = unicodeorg_alias[emk]
    unicodeform = emoji.emojize(_emk, use_aliases=True).encode('unicode_escape').decode('utf8')
    if '\\u' in unicodeform:
        #print(unicodeform)
        if len(unicodeform) == 6:
            #pass
            unicodeform = unicodeform.upper().replace('\\U','\\U0000')
        if len(unicodeform) == 7:
            pass
            unicodeform = unicodeform.upper().replace('\\U','\\U000')
        #print(unicodeform)
    if unicodeform != _emk:
        for CLRDname in fullemoji_unicodeorglist:
            if unicodeform.upper() in fullemoji_unicodeorg[CLRDname]['UnicodeAbstraction']: #???
                if emojisk_dataset[emk]['conds'] == False:
                    emojisk_dataset[emk]['conds'] = True
                if emojisk_dataset[emk]['inFull'] == False:
                    emojisk_dataset[emk]['Apple_img'] = fullemoji_unicodeorg[CLRDname]['Apple_img']
                    emojisk_dataset[emk]['Index'] = fullemoji_unicodeorg[CLRDname]['Index']
                    emojisk_dataset[emk]['UnicodeAbstration'] = unicodeform.upper()
                    emojisk_dataset[emk]['unicodeorgbigclass'] = fullemoji_unicodeorg[CLRDname]['BigHead']
                    emojisk_dataset[emk]['unicodeorgmediumclass'] = fullemoji_unicodeorg[CLRDname]['MediumHead']
                    if unicodeform in emojiyear_unicodeorglist:
                        emojisk_dataset[emk]['unicodeyear'] = emojiyear_unicodeorg[unicodeform]
                    elif unicodeform.upper() in emojiyear_unicodeorglist:
                        emojisk_dataset[emk]['unicodeyear'] = emojiyear_unicodeorg[unicodeform.upper()]
                    emojisk_dataset[emk]['inFull'] = True


##########################
## preliminary evaluation
##########################
                        
nogithubsed = []
for e in emojisk_dataset:
    if emojisk_dataset[e]['conds'] and not emojisk_dataset[e]['inFull'] and emojisk_dataset[e]['inGithub'] == 'No':
        if not any([lt.isdigit() for lt in e]):
            nogithubsed.append((e, emojisk_dataset[e]['total_kw']))
print(len(nogithubsed))     
print(sorted(nogithubsed, key=lambda x: x[1], reverse=True)[:150])

#################################################################################
## completing images for those for which only images could be found: the Github list
##################################################################################

with open(os.getcwd()+datadirectory+'/emoji_aliases_github.pkl','rb') as fin:
    emojis_github = pickle.load(fin)
    
emojis_githublist = list(emojis_github.keys())

for e in emojisk_dataset:
    if emojisk_dataset[e]['conds'] and not emojisk_dataset[e]['inFull'] and emojisk_dataset[e]['inGithub'] == 'No':
        if e in emojis_githublist:
           emojisk_dataset[e]['inGithub'] = 'Yes'
           emojisk_dataset[e]['Apple_img'] = emojis_github[e]['img']


##########################
## preliminary evaluation
##########################

githubsed = []
for e in emojisk_dataset:
    if emojisk_dataset[e]['conds'] and not emojisk_dataset[e]['inFull'] and emojisk_dataset[e]['inGithub'] == 'Yes':
        githubsed.append((e, emojisk_dataset[e]['total_kw']))
print(len(githubsed)) #454      
print(sorted(githubsed, key=lambda x: x[1], reverse=True)[:150])

nogithubsed = []
for e in emojisk_dataset:
    if emojisk_dataset[e]['conds'] and not emojisk_dataset[e]['inFull'] and emojisk_dataset[e]['inGithub'] == 'No':
        if not any([lt.isdigit() for lt in e]):
            nogithubsed.append((e, emojisk_dataset[e]['total_kw']))
print(len(nogithubsed))     
print(sorted(nogithubsed, key=lambda x: x[1], reverse=True)[:150])



#################################################################################
## updating some of the names manually 2: no aliases for unicodeorglist so get only Github images
##################################################################################

github_image = {
            ':finnadie:':"https://assets-cdn.github.com/images/icons/emoji/finnadie.png",
            ':goberserk:':"https://assets-cdn.github.com/images/icons/emoji/goberserk.png",
            ':godmode:':"https://assets-cdn.github.com/images/icons/emoji/godmode.png",
            ':hurtrealbad:':"https://assets-cdn.github.com/images/icons/emoji/hurtrealbad.png",
            ':suspect:':"https://assets-cdn.github.com/images/icons/emoji/suspect.png",
            ':trollface:':"https://assets-cdn.github.com/images/icons/emoji/trollface.png",
            ':octocat:': "https://assets-cdn.github.com/images/icons/emoji/octocat.png",
            }

for emk in github_image:
    emojisk_dataset[emk]['inGithub'] = 'Yes'
    emojisk_dataset[emk]['Apple_img'] = github_image[emk]

##########################
## preliminary evaluation
##########################

nogithubsed = []
for e in emojisk_dataset:
    if emojisk_dataset[e]['conds'] and not emojisk_dataset[e]['inFull'] and emojisk_dataset[e]['inGithub'] == 'No':
        if not any([lt.isdigit() for lt in e]):
            nogithubsed.append((e, emojisk_dataset[e]['total_kw']))
print(len(nogithubsed))   #458  
print(sorted(nogithubsed, key=lambda x: x[1], reverse=True)[:150])

collected = []
for e in emojisk_dataset:
    if emojisk_dataset[e]['inFull'] or emojisk_dataset[e]['inGithub'] == 'Yes':
        collected.append((e, emojisk_dataset[e]['total_kw']))
print(len(collected)) #816


#################################################################################
## saving the file!!! finally!!
##################################################################################

with open(os.getcwd()+datadirectory+'/emojidb01_corr.pkl','wb') as fout:
    emojidb_kw = {}
    emojidb_kw['emojisk_dataset'] = emojisk_dataset
    emojidb_kw['emojiset_kw'] = emojiset_kw
    emojidb_kw['userdict_kw'] = userdict_kw
    pickle.dump(emojidb_kw, fout)
