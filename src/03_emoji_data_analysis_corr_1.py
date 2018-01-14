# -*- coding: UTF-8 -*-
import os, sys, gc
import json, pickle, csv
import emoji
import re
import collections, itertools, operator
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy, pandas


datadirectory = "/1_archive"

############################################################################
## LOADING THE DATASETS
############################################################################

emojiset_kw = set()
userdict_kw = dict()

print('STARTING LOADING DATA')

with open(os.getcwd()+datadirectory+'/emojidb01_corr.pkl','rb') as fin:
    emojidb_kw = pickle.load(fin)

print('FINISHED LOADING DATA')

emojisk_dataset = emojidb_kw['emojisk_dataset']
emojiset_kw = emojidb_kw['emojiset_kw']
userdict_kw = emojidb_kw['userdict_kw']

del emojidb_kw
gc.collect()

print('emojisk_dataset length', len(emojisk_dataset))
print('emojiset_kw length', len(emojiset_kw))
print('userdict_kw length', len(userdict_kw))
#print('emojiset_kw\n', emojiset_kw)

# sys.exit()
#

#####################################################################
## Some corrections
#####################################################################


## OJO: fixing the :poop:
emojisk_dataset[':poop:']['count_kw'] = emojisk_dataset[':poop:']['count_kw'] + emojisk_dataset[':shit:']['count_kw'] + emojisk_dataset[':hankey:']['count_kw']
emojisk_dataset[':poop:']['total_kw'] = emojisk_dataset[':poop:']['total_kw'] + emojisk_dataset[':shit:']['total_kw'] + emojisk_dataset[':hankey:']['total_kw']
emojisk_dataset[':poop:']['first_kw'] = min([emojisk_dataset[':poop:']['first_kw'], emojisk_dataset[':shit:']['first_kw'], emojisk_dataset[':hankey:']['first_kw']])
emojisk_dataset[':poop:']['last_kw'] = max([emojisk_dataset[':poop:']['last_kw'], emojisk_dataset[':shit:']['last_kw'],emojisk_dataset[':hankey:']['last_kw']])
del emojisk_dataset[':shit:']
emojiset_kw.remove(':shit:')
del emojisk_dataset[':hankey:']
emojiset_kw.remove(':hankey:')

## OJO: :shipit: image
emojisk_dataset[':shipit:']['Apple_img'] = 'https://assets-cdn.github.com/images/icons/emoji/shipit.png'
emojisk_dataset[':shipit:']['inGithub'] = 'Yes'


## OJO: :rage1: image
emojisk_dataset[':rage1:']['Apple_img'] = 'https://assets-cdn.github.com/images/icons/emoji/rage1.png'
emojisk_dataset[':rage1:']['inGithub'] = 'Yes'

## OJO: :wave: image
emojisk_dataset[':wave:']['Apple_img'] = 'https://assets-cdn.github.com/images/icons/emoji/wave.png'

## OJO: :clap: image
emojisk_dataset[':clap:']['Apple_img'] = 'https://assets-cdn.github.com/images/icons/emoji/clap.png'

## OJO: :thumbsup: image
emojisk_dataset[':thumbsup:']['Apple_img'] = 'https://assets-cdn.github.com/images/icons/emoji/thumbsup.png'

## OJO: :point_up: image
emojisk_dataset[':point_up:']['Apple_img'] = 'https://assets-cdn.github.com/images/icons/emoji/point_up.png'

#####################################################################
### ANALYSES
#####################################################################

sys.exit()

############################################################################
## some preliminary analyses
############################################################################

# findingnemo = []
# for e in emojisk_dataset:
#     if emojisk_dataset[e]['inFull']:
#         if not any([lt.isdigit() for lt in e]):
#             findingnemo.append((e, emojisk_dataset[e]['count_kw']))
# print(len(findingnemo)) #480     
# print(sorted(findingnemo, key=lambda x: x[1], reverse=True)[:20])
# 
# inFull = set([x[0] for x in findingnemo])
# 
# sumupdictagain = collections.defaultdict(int)
# 
# for user in userdict_kw:
#     if user == 'camperbot':
#         continue
#     if len(userdict_kw[user]) > 0:
#         for msgid in userdict_kw[user]:
#             for top in inFull.intersection(userdict_kw[user][msgid]['setemojis_kw']):
#                 sumupdictagain[top] += 1
# 
# for k,v in sorted(sumupdictagain.items(), key=lambda x: x[1], reverse=True)[:150]:
#     print(k,v)
# 
# 
# 
# thup = 0           
# for user in userdict_kw:
#     if user == 'camperbot':
#         continue
#     if len(userdict_kw[user]) > 0:
#         for msgid in userdict_kw[user]:
#             if {':+1:'} in userdict_kw[user][msgid]['setemojis_kw']:
#                 thup += 1



############################################################################
#min date / max date (forgot to check this before... sorry for the following brute force full search)
############################################################################

mindate = '2018-12-31'
maxdate = '2010-01-01'

for user in userdict_kw:
    if len(userdict_kw[user]) > 0:
        for msgid in userdict_kw[user]:
            if userdict_kw[user][msgid]['sent'] == "-99": continue
            if userdict_kw[user][msgid]['sent'] <= mindate:
                mindate = userdict_kw[user][msgid]['sent']
            if userdict_kw[user][msgid]['sent'] >= maxdate:
                maxdate = userdict_kw[user][msgid]['sent']

print("mindate : {0}, maxdate : {1}".format(mindate, maxdate))

#sys.exit()
############################################################################
#counting number of active / no-active emojiers against total active users
############################################################################

count_activeusers = 0
count_emojieractive = 0
count_emojiernotactive = 0
aver_emojiPERmsg = []
for user in userdict_kw:
    if len(userdict_kw[user]) > 10:
        count_activeusers += 1
        for mid in userdict_kw[user]:
            if userdict_kw[user][mid]['exist_emkw']:
                count_emojieractive += 1
                break
    else:
        for mid in userdict_kw[user]:
            if userdict_kw[user][mid]['exist_emkw']:
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
#collective and individual vocabulary
############################################################################

print("number of emojis used collectively by emojiers during the period: {0}".format(len([k for k in emojisk_dataset.keys() if emojisk_dataset[k]['inFull']])))

############################################################################
#calculating individual vocabularies AND total of totals and total of counts AND emojis per message
############################################################################

totals_kw = 0
counts_kw = 0
average_emojisPERmsg = []
indvoc = collections.defaultdict(set) #set will give an error (https://stackoverflow.com/questions/23577724/type-error-unhashable-typeset)
for user in userdict_kw:
    mark = False
    if len(userdict_kw[user]) > 0:
        for mid in userdict_kw[user]:
            if userdict_kw[user][mid]['exist_emkw']:
                #print(len(userdict_kw[user][mid]['setemojis']))
                #print(len(indvoc[user]))
                #print(userdict_kw[user][mid]['setemojis'] | indvoc[user])
                mark = True
                indvoc[user] = indvoc[user] | userdict_kw[user][mid]['setemojis_kw'] #a set operation
                counts_kw += len(userdict_kw[user][mid]['setemojis_kw'])
                totals_kw += len(userdict_kw[user][mid]['listemojis_kw'])
    if mark == True:
        totalmsgs = len(userdict_kw[user])
        totalemojis = 0
        for mid in userdict_kw[user]:
            if userdict_kw[user][mid]['exist_emkw']:
                totalemojis += len(userdict_kw[user][mid]['listemojis_kw'])
        average_emojisPERmsg.append(totalemojis/totalmsgs)
            

print('total of totals emojis used ', totals_kw)
print('total of counts emojis used ', counts_kw)
print('average emoji per msg ', sum(average_emojisPERmsg)/len(average_emojisPERmsg))

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



#sys.exit()

############################################################################
#FIGURES AND VISUALIZATIONS
############################################################################

#####################################################################
### testing and preparing pandas
#####################################################################

emojisk_dataset_pandaslike = {
                                'alias': [],
                                'conds': [],
                                'inFull':[],
                                'inGithub':[],
                                'inYear': [],
                                'Index': [],
                                'count_kw': [],
                                'total_kw': [],
                                'count_kw_camperbot': [],
                                'total_kw_camperbot': [],
                                'first_kw': [],
                                'last_kw': [],
                                'unicodeyear': [],
                                'unicodeorgbigclass':[],
                                'unicodeorgmediumclass':[],
}

for emk in emojisk_dataset:
    emojisk_dataset_pandaslike['alias'].append(emojisk_dataset[emk]['alias'])
    emojisk_dataset_pandaslike['conds'].append(emojisk_dataset[emk]['conds'])
    emojisk_dataset_pandaslike['inFull'].append(emojisk_dataset[emk]['inFull'])
    emojisk_dataset_pandaslike['inGithub'].append(emojisk_dataset[emk]['inGithub'])
    emojisk_dataset_pandaslike['inYear'].append(emojisk_dataset[emk]['inYear'])
    emojisk_dataset_pandaslike['Index'].append(emojisk_dataset[emk]['Index'])
    emojisk_dataset_pandaslike['count_kw'].append(emojisk_dataset[emk]['count_kw'])
    emojisk_dataset_pandaslike['total_kw'].append(emojisk_dataset[emk]['total_kw'])
    emojisk_dataset_pandaslike['count_kw_camperbot'].append(emojisk_dataset[emk]['count_kw_camperbot'])
    emojisk_dataset_pandaslike['total_kw_camperbot'].append(emojisk_dataset[emk]['total_kw_camperbot'])
    emojisk_dataset_pandaslike['first_kw'].append(emojisk_dataset[emk]['first_kw'])
    emojisk_dataset_pandaslike['last_kw'].append(emojisk_dataset[emk]['last_kw'])
    emojisk_dataset_pandaslike['unicodeyear'].append(emojisk_dataset[emk]['unicodeyear'])
    emojisk_dataset_pandaslike['unicodeorgbigclass'].append(emojisk_dataset[emk]['unicodeorgbigclass'])
    emojisk_dataset_pandaslike['unicodeorgmediumclass'].append(emojisk_dataset[emk]['unicodeorgmediumclass'])


csvdataset = pandas.DataFrame.from_dict(emojisk_dataset_pandaslike)

# del emojisk_dataset
# gc.collect()
# del emojiset_kw
# gc.collect()
# del userdict_kw
# gc.collect()

#sys.exit()

##some test...
#csvdataset[['emoji','alias','Index']]
#csvdataset.groupby('unicodeorgbigclass')['unicodeorgbigclass'].count()
#csvdataset[csvdataset['unicodeorgbigclass']=='Smileys & People']
#csvdataset[csvdataset['unicodeorgbigclass']=='Smileys & People'].groupby('unicodeorgmediumclass')['unicodeorgmediumclass'].count()
#csvdataset[csvdataset['unicodeorgbigclass']=='Smileys & People'].groupby('count_kw')['unicodeorgmediumclass'].sum()
#csvdataset[csvdataset['unicodeorgbigclass']=='Smileys & People'].groupby('count_kw')[['unicodeorgmediumclass','alias']].sum()

##################################################################
### pies
##################################################################
### 

# csvdataset.groupby('unicodeorgbigclass')['count_kw'].sum().plot(kind='pie')
# plt.axis('equal')
# plt.show()

fig, axes = plt.subplots(1,1)
csvdataset[csvdataset['unicodeorgbigclass']!=''].groupby('unicodeorgbigclass')['count_kw'].sum().plot(kind='pie', ax=axes)
axes.set_ylabel('')
axes.set_xlabel('unique counts per msg\n(proportions)')
plt.axis('equal')
plt.show()


##################################################################
### The top-ever 25 emojis in the freeCodeCamp chatroom counting from 2015 to 2017 (Nov)
##################################################################

# ### fixing the :poop:
# csvdataset.loc[csvdataset['alias'] == ':poop:','count_kw'] = csvdataset[csvdataset['alias'] == ':poop:']['count_kw'].values + csvdataset[csvdataset['alias'] == ':shit:']['count_kw'].values

#print(csvdataset.groupby('count_kw')[['unicodeorgbigclass','unicodeorgmediumclass','alias']].sum().tail(25))
top25 = csvdataset.groupby('count_kw')[['unicodeorgbigclass','unicodeorgmediumclass','alias']].sum().tail(25)
'''
TODO:
-- eventually, improve the layout (horrible!)
-- repeat the color mapping technique with the category pie
'''
##correcting/adding data
top25.reset_index(level=0, inplace=True)
top25.loc[top25['alias']==':trollface:', 'unicodeorgmediumclass'] = 'face-negative'
top25.loc[top25['alias']==':trollface:', 'unicodeorgbigclass'] = 'Smileys & People'
top25.loc[top25['alias']==':shipit:', 'unicodeorgmediumclass'] = 'face-neutral'
top25.loc[top25['alias']==':shipit:', 'unicodeorgbigclass'] = 'Smileys & People'
top25.loc[top25['alias']==':wink2:', 'unicodeorgmediumclass'] = 'face-positive'
top25.loc[top25['alias']==':wink2:', 'unicodeorgbigclass'] = 'Smileys & People'

top25['unichar'] = top25['alias'].apply(lambda x: emoji.emojize(x, use_aliases = True))
top25.loc[top25['alias']==':wink2:', 'unichar'] = emoji.emojize(':stuck_out_tongue_winking_eye:', use_aliases = True)

##figures
##https://matplotlib.org/users/colors.html
#https://stackoverflow.com/questions/16006572/plotting-different-colors-in-matplotlib
#https://stackoverflow.com/questions/11927715/how-to-give-a-pandas-matplotlib-bar-graph-custom-colors
#https://matplotlib.org/gallery/images_contours_and_fields/custom_cmap.html
##https://stackoverflow.com/questions/14777066/matplotlib-discrete-colorbar
##https://stackoverflow.com/questions/14908576/how-to-remove-frame-from-matplotlib-pyplot-figure-vs-matplotlib-figure-frame

##layout initialization
fig, axes = plt.subplots(nrows=1, ncols=3, gridspec_kw = {'width_ratios':[1,.5,1]})

##chart 1
cmap_pie = plt.get_cmap('Oranges', 35)
#cmap = plt.get_cmap('Greys', 35)

##The assigning of values by subcategory could be done programatically; I did it manually while learning...
#colors = {'face-positive':'green', 'face-negative':'navy', 'face-fantasy':'sienna', 'face-neutral':'yellowgreen', 'body':'tomato', 'family':'red', 'tool':'indigo', 'event':'orchid', 'drink':'tan', 'sky & weather':'gold', }
colors_pie = {'face-positive': 2, 'body': 29, 'face-negative': 5, 'event':8, 'drink':11, 'sky & weather':14, 'face-neutral':17,'face-fantasy':20,'family':23, 'tool':26,  }


top25.groupby('unicodeorgmediumclass')['count_kw'].sum().sort_values().plot(kind='pie',ax=axes[0], colors=[cmap_pie(colors[i] + 3) for i in top25.groupby('unicodeorgmediumclass')['count_kw'].sum().sort_values().index])
axes[0].axis('equal')
axes[0].set_ylabel('')
axes[0].set_xlabel('unique counts per msg\n(proportions)')

##inter-space
axes[1].grid(False)
axes[1].axis('off')
axes[1].patch.set_visible(False)


##chart 2
cmap_hbar = plt.get_cmap('YlGn', 7)

top25.plot(kind='barh', x='unicodeorgmediumclass', y='count_kw',ax=axes[2], width=.9, color=top25['unicodeorgmediumclass'].apply(lambda i: cmap_hbar(5) if i == "body" else cmap_hbar(2)))
#http://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html
#https://stackoverflow.com/questions/25447700/annotate-bars-with-values-on-pandas-bar-plots
# # create a list to collect the plt.patches data
# totals = []
# 
# # find the values and append to list
# for i in axes[0].patches:
#     totals.append(i.get_height())
# 
# # set individual bar lables using above list
# total = sum(totals)
# 
# # set individual bar lables using above list
# for i in axes[0].patches:
#     # get_x pulls left or right; get_height pushes up or down
#     axes[0].text(i.get_x()-.03, i.get_height()+.5, \
#             str(round((i.get_height()/total)*100, 2))+'%', fontsize=15,
#                 color='dimgrey')

axes[2].grid(False)
axes[2].patch.set_visible(False)
# Only show ticks on the left and bottom spines
axes[2].yaxis.set_ticks_position('left')
axes[2].xaxis.set_ticks_position('bottom')
axes[2].legend_.remove()
#https://stackoverflow.com/questions/43419590/matplotlib-annotate-plot-with-emoji-labels
for i, v in enumerate(axes[2].patches):
    width = v.get_width()
    print(top25['unichar'][i])
    em = top25['unichar'][i]
    axes[2].text(width+100, v.get_y() - v.get_height()/5, '%s' % em, ha='left', va='bottom', fontname='symbola')
    ###If the bar are vertical then...
    # height = v.get_height()
    # if em in (':trollface:', ':shipit:'):
    #     axes[0].text(v.get_x() + v.get_width()/2.0, height, '%s' % em, ha='center', va='bottom', rotation='vertical', fontname='symbola')
    # else:
    #     axes[0].text(v.get_x() + v.get_width()/2.0, height, '%s' % em, ha='center', va='bottom', fontname='symbola')
        

#top25.groupby('unicodeorgmediumclass')['count_kw'].sum().sort_values(ascending=False).plot(kind='pie',ax=axes[1], colors=[colors[i] for i in top25.groupby('unicodeorgmediumclass')['count_kw'].sum().sort_values(ascending=False).index]) ##sortear!!!
axes[2].set_ylabel('unicode.org subcategories')
axes[2].set_xlabel('unique counts per msg')


plt.show()


##Colormap YlGr is not recognized. Possible values are: Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spectral, spectral_r, spring, spring_r, summer, summer_r, terrain, terrain_r, viridis, viridis_r, winter, winter_r


##nice reference:
##https://www.datascience.com/learn-data-science/tutorials/creating-data-visualizations-matplotlib-data-science-python
##
##matplotlib figure grid manipulation and subplotting:
##https://www.python-course.eu/matplotlib_multiple_figures.php
##https://jakevdp.github.io/PythonDataScienceHandbook/04.08-multiple-subplots.html
##https://scientificallysound.org/2016/06/09/matplotlib-how-to-plot-subplots-of-unequal-sizes/
##https://stackoverflow.com/questions/14770735/changing-figure-size-with-subplots
##https://matplotlib.org/gallery/subplots_axes_and_figures/subplots_demo.html
##https://stackoverflow.com/questions/12998430/remove-xticks-in-a-matplotlib-plot

##################################################################
### preparing the dataset for the d3.js visualizations
##################################################################

#https://stackoverflow.com/questions/993358/creating-a-range-of-dates-in-python

##Observations:
##there are many ways to set monthly batches that are more programatic, for example
##https://stackoverflow.com/questions/34898525/generate-list-of-months-between-interval-in-python/34899127
##
##but if you know something about the problem that is not going to change anyway, why not to use it?
##

#months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
date_generated_ymonth = []

for y in range(2014, 2018):
    if y == 2014:
        date_generated_ymonth.append(str(y)+'-12')
        continue
    for m in months:
        date_generated_ymonth.append(str(y)+'-'+m)

print(date_generated_ymonth)

def Apple_exists(emojisk_dataset, em):
    if 'Apple_img' in list(emojisk_dataset[em].keys()):
        return emojisk_dataset[em]['Apple_img']
    else:
        return '---'

viz = dict()

for em in emojiset_kw:
    if em == ':wink2:':
        em = ':stuck_out_tongue_winking_eye:'
    viz[emoji.emojize(em, use_aliases=True)] = collections.OrderedDict()
    viz[emoji.emojize(em, use_aliases=True)].update({'data':{'billboard':'false','inFull':emojisk_dataset[em]['inFull'],'inGithub':emojisk_dataset[em]['inGithub'],'total':emojisk_dataset[em]['total_kw'],'alias':emojisk_dataset[em]['alias'],'first':emojisk_dataset[em]['first_kw'],'last':emojisk_dataset[em]['last_kw'],'Apple_img':Apple_exists(emojisk_dataset, em)}})
    for ym in date_generated_ymonth:                        #<--- by using this range in advance, I can add ALL dates to each character
        viz[emoji.emojize(em, use_aliases=True)].update({ym:{'count':0, 'order':-1}})
        
for user in userdict_kw:
    if user == "camperbot":
        continue
    if len(userdict_kw[user]) > 0:
        for mid in userdict_kw[user]:
          if userdict_kw[user][mid]['exist_emkw']:
            for em in set(userdict_kw[user][mid]['listemojis_kw']):
                ### fixing the :poop:
                if em == ':shit:' or em == ':hankey:':
                    em = ':poop:'
                if em == ':wink2:':
                    em = ':stuck_out_tongue_winking_eye:'
                msgdate = userdict_kw[user][mid]['sent']
                if msgdate[:7] in date_generated_ymonth:
                    viz[emoji.emojize(em, use_aliases=True)][ msgdate[:7] ]['count'] += 1

for ym in date_generated_ymonth:
    #print('Y-MONTH ', ym)
    tempdict = collections.defaultdict(int)
    for em in emojiset_kw:
        ### fixing the :poop:
        # if em == ':shit:':
        #     em = ':poop:'
        if em == ':wink2:':
            em = ':stuck_out_tongue_winking_eye:'
        tempdict[emoji.emojize(em, use_aliases=True)] = viz[emoji.emojize(em, use_aliases=True)][ym]['count'] #create a dict only for emoji counts for that week
        if viz[emoji.emojize(em, use_aliases=True)][ym]['count'] > 0:
            #print(em, week, billboard[em][week]['count'])
            pass
    prev_c = 0
    o = 0
    #print(sorted(tempdict.items(), key = lambda x: x[1], reverse = True)[:6])
    if ym == '2015-Jul':
        #break
        pass
    for i, val in enumerate(sorted(tempdict.items(), key = lambda x: x[1], reverse = True)): #order the emojis based on counts of that week
        emojilist = list(viz.keys())
        #if val[0].encode('unicode_escape').decode('utf8') in ['\\u262f', '\\u2744', '\\U0001f525']: # 'CHAR'.encode('unicode_escape').decode('utf8'); these were considered outliers
        #    continue
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
        viz[val[0]][ym]['order'] = o
        #print(ym, val[0], billboard[val[0]][ym]['order'])
  

print('viz length', len(viz))

for em in emojiset_kw: #now let's keep only the records that had at least one assignment in the ordering at any point of the study
    if em == ':wink2:':
        em = ':stuck_out_tongue_winking_eye:'
    has_o = False
    if not viz[emoji.emojize(em, use_aliases=True)]['data']['inFull'] and viz[emoji.emojize(em, use_aliases=True)]['data']['inGithub']=='No':
        del viz[emoji.emojize(em, use_aliases=True)]
        continue
    for ym in date_generated_ymonth:
        if viz[emoji.emojize(em, use_aliases=True)][ym]['order'] != -1:
            has_o = True
            #print(em)
            break
    if has_o != False:
       viz[emoji.emojize(em, use_aliases=True)]['data']['billboard'] = 'true'
       #del viz[em]
       #pass

print('viz length', len(viz))

for v in viz:
    if viz[v]['data']['billboard'] == 'true':
        print(v)


#####################################################################
### preparing the introduction year dataset
#####################################################################
### 
# 
# billboard_corr = {}
# 
# for k in billboard:
#     billboard_corr[] = billboard[k]


with open(os.getcwd()+datadirectory+'/emojis_viz_final_corr.json','w') as fout:
        json.dump(viz, fout)  


#####################################################################
### REFERENCES
#####################################################################

##d3.js point interpolation through a line path and path animation:
##https://bl.ocks.org/mbostock/1705868
##http://bl.ocks.org/duopixel/4063326
##http://bl.ocks.org/KoGor/8162640
##https://stackoverflow.com/questions/28682454/moving-a-circle-along-a-d3-path-animating-at-varying-speeds
##http://jsfiddle.net/mbrownshoes/k86fbade/4/
##http://www.thesoftwaresimpleton.com/blog/2016/06/12/animate-path-arc/
##http://tommykrueger.com/projects/d3tests/animation-path.php
##http://bl.ocks.org/zanarmstrong/e2d22ae47d24179b574c

##Force Layout:
##https://github.com/d3/d3-force
##http://jsdatav.is/visuals.html?id=11560633
##http://bl.ocks.org/rpgove/10603627
##https://bl.ocks.org/HarryStevens/f636199a46fc4b210fbca3b1dc4ef372
##http://bl.ocks.org/GerHobbelt/3670903

##Heatmaps:
##http://bl.ocks.org/ianyfchang/8119685
##http://bl.ocks.org/umcrcooke/5703304
##https://bl.ocks.org/Bl3f/cdb5ad854b376765fa99
##http://bl.ocks.org/umcrcooke/5703304
##http://bl.ocks.org/ianyfchang/8119685
##http://bl.ocks.org/tjdecke/5558084
##https://bl.ocks.org/iblind/b394c943fef0aedc569d
##https://bl.ocks.org/nanu146/df39c69d1d0cb1b71429b2cd47e2a189

##Calendars with heatmaps:
##https://bl.ocks.org/alansmithy/6fd2625d3ba2b6c9ad48
##https://bl.ocks.org/mbostock/4063318
##https://github.com/g1eb/calendar-heatmap

##Beeswarm:
##https://bl.ocks.org/duhaime/14c30df6b82d3f8094e5a51e5fff739a
##http://bl.ocks.org/jkschneider/4732279
##https://stackoverflow.com/questions/7955098/beeswarm-plot-with-force-directed-layout-in-javascript-d3


##embeding images:
##https://stackoverflow.com/questions/11961120/load-src-content-to-svg-image-dynamically
##https://stackoverflow.com/questions/11753485/set-img-src-to-dynamic-svg-element

##Event handling:
##http://bl.ocks.org/WilliamQLiu/76ae20060e19bf42d774

####OTHERS###
##d3js data binding, etc.
##https://square.github.io/intro-to-d3/data-binding/
##https://www.dashingd3js.com/svg-group-element-and-d3js
##https://bl.ocks.org/d3noob/ced1b9b18bd8192d2c898884033b5529
##http://bl.ocks.org/enjalot/1425402 (enjalot)

##Scales:
##http://bl.ocks.org/emmasaunders/cebb1837530c876def717c0e5c61da31
##https://github.com/d3/d3-scale#ordinal-scales
##https://github.com/d3/d3-axis

##General, Emoji Sentiment Analysis:
##https://link.springer.com/chapter/10.1007/978-3-319-63564-4_4
##https://kth.diva-portal.org/smash/get/diva2:927073/FULLTEXT01.pdf
##https://web.stanford.edu/~jesszhao/files/twitterSentiment.pdf

##Convex Hull:
##https://bl.ocks.org/mbostock/4341699

##Transitions:
##http://bl.ocks.org/d3noob/7030f35b72de721622b8
##https://bl.ocks.org/mbostock/1345853
##https://www.dashingd3js.com/lessons/d3-transition-basics

##*.each() in d3.js
##http://bl.ocks.org/milroc/4254604

##d3.js + canvas:
##https://bl.ocks.org/pbeshai/65420c8d722cdbb0600b276c3adcc6e8

##scatterplot and charts:
##https://moderndata.plot.ly/ggplot2-docs-completely-remade-in-d3-js/
##http://www.saigesp.es/d3js-bubble-line-chart/
##https://bl.ocks.org/d3noob/0e276dc70bb9184727ee47d6dd06e915

##d3.js tweening
##http://andyshora.com/tweening-shapes-paths-d3-js.html
##https://www.safaribooksonline.com/blog/2013/07/11/reusable-d3-js-using-attrtween-transitions-and-mv/

##Functional Programming:
##http://plosquare.blogspot.nl/2014/01/some-functional-programming-tricks-and.html
##https://www.smashingmagazine.com/2014/07/dont-be-scared-of-functional-programming/

##Miscelaneous:
##https://heredragonsabound.blogspot.nl/2016/11/this-is-where-i-draw-line.html
##https://bl.ocks.org/hugolpz/7a2e24688591887f75c3
##https://freakalytics.com/
##http://learnjsdata.com/time.html


