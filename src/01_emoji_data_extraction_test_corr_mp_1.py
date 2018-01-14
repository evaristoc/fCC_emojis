import os, sys
import json, pickle
import emoji
import collections
import re
import random
import time
import multiprocessing
#sys.exit()

##https://gitter.im/FreeCodeCamp/FreeCodeCamp?at=58b600e17ceae5376a526d13 last message 28 FEB 2017
def dataset_transf(f,datadirectory):
    
    if f == '1':
        f = ''
    
    print('STARTING LOADING DATA')
    
    #with open(drtin+'/freecodecamp_test.pkl','rb') as fin: #<------------ previous file
    with open(datadirectory+'/freecodecamp'+str(f)+'_test.pkl','rb') as fin:
        fileddata = pickle.load(fin)
    
    
    print('FINISHED LOADING DATA')
    
    
    print('STARTING TRANSFORMING DATA')

    ############
    ## Comment the test...
    ############
    start = time.time()
    print('I am solving the file number '+str(f)+'. It will take a lot of memory.')
    time.sleep(5)
    end = time.time()
    print('Data was saved at emojiproject0'+str(f)+'_corr.pkl after {} secs. DONE.'.format(end-start))


    ############
    ## ... and uncomment the tasks
    ############
    
    # emojiset_kw = set()
    # userdict_kw = collections.defaultdict(dict)
    # resttime = 75 #5min, 2.5min, 1.25min
    # resttimemin = resttime//60
    # #breaking = False
    # 
    # countermsg = 0
    # start = time.time()
    # for msg in fileddata:
    #     if countermsg == 100000:
    #         end = time.time()
    #         minutes = (end-start)//60
    #         seconds = (end-start) - minutes*60
    #         length = len(userdict_kw)
    #         #print("100000 messages in around {:.0f} mins {:.0f} secs for an increase in userdict_kw length of {}: going for a 5 min rest...".format(minutes, seconds, length), end=" ")
    #         print("100000 messages in around {:.0f} mins {:.0f} secs for an increase in userdict_kw length of {}: going for about {} min rest...".format(minutes, seconds, length, resttimemin))
    #         time.sleep(resttime)
    #         start = time.time()
    #         print("I am back to work!")
    #         countermsg = 0
    #     if f == '3' and msg['sent'][0:10] <= '2017-03-31': #find overlapping data; if some collected, skip it
    #         continue
    #     else:
    #         countermsg += 1
    #         try:
    #             lwstrpmsg = msg['text'].lower().replace('.', ' ').replace(',', ' ').replace(';', ' ').replace('!', ' ').replace('?', ' ').strip(' ')
    #             #lwstrpmsg = msg['text'].lower().replace('::',' ').replace('.', ' ').replace(',', ' ').replace(';', ' ').replace('!', ' ').replace('?', ' ').strip(' ')    
    #             datum = msg['sent'][0:10]
    #             msgid = msg['id']
    #             if msg['fromUser'] != None:
    #                 user = msg['fromUser']['username']
    #             else:
    #                 user = 'unsubscribedusers'
    #         except:
    #             print('an error; skipping this message ', msg)
    #             continue
    #         userdict_kw[user][msgid] = {}
    #         userdict_kw[user][msgid]['sent'] = '-99'
    #         userdict_kw[user][msgid]['text'] = ''
    #         userdict_kw[user][msgid]['exist_emkw'] = False
    #         userdict_kw[user][msgid]['listemojis_kw'] = []
    #         userdict_kw[user][msgid]['setemojis_kw'] = set()
    #         emkws = re.findall(r":\w+:", msg['text'])
    #         if len(emkws):
    #             for emkw in re.findall(r":\w+:", msg['text']):
    #                 userdict_kw[user][msgid]['exist_emkw'] = True
    #                 userdict_kw[user][msgid]['listemojis_kw'].append(emkw)
    #                 userdict_kw[user][msgid]['setemojis_kw'].add(emkw)
    #                 userdict_kw[user][msgid]['text'] = msg['text']
    #                 userdict_kw[user][msgid]['sent'] = datum
    #                 emojiset_kw.add(emkw)
    # 
    # 
    # 
    # #sys.exit()
    # end = time.time()
    # minutes = (end-start)//60
    # seconds = (end-start) - minutes*60
    # length = len(userdict_kw)
    # print("{} messages in around {:.0f} mins {:.0f} secs for an increase in userdict_kw length of {}: Finished...".format(countermsg, minutes, seconds, length), end=" ")
    # print()
    print('ENDING TRANSFORMING DATA')
    print()
    # 
    # emojikwdata = {}
    # 
    # emojikwdata['emojiset_kw'] = emojiset_kw
    # emojikwdata['userdict_kw'] = userdict_kw
    # 
    # ##sys.exit()
    # #with open(datadirectory+'/emojiproject0'+str(f)+'.pkl','wb') as fout:
    # if f == '':
    #     f = '1'
    # with open(datadirectory+'/emojiproject0'+f+'_corr.pkl','wb') as fout:
    #     pickle.dump(emojikwdata, fout)
    #     print('Data was saved at emojiproject0'+f+'_corr.pkl. DONE.')


##https://stackoverflow.com/questions/20887555/dead-simple-example-of-using-multiprocessing-queue-pool-and-locking
##https://www.ploggingdev.com/2017/01/multiprocessing-and-multithreading-in-python-3/

def feeder(feederQ):
    for i in range(1,4):
        feederQ.put(i)

def preparing_file(feederQ, datadirectory):
    ##https://gitter.im/FreeCodeCamp/FreeCodeCamp?at=58b600e17ceae5376a526d13 last message 28 FEB 2017
    
    while True:
        
        try:
            f = feederQ.get()
            if f is None:
                # Poison pill means shutdown
                print('%s: Exiting process %s from parent %s' % (multiprocessing.Process.name, os.getpid(), os.getppid()))
                feederQ.task_done()
                break
            with lock:
                try:
                    f = str(f)
                    dataset_transf(f, datadirectory)
                    feederQ.task_done()
                except:
                    print("do something with error handling file")
                    feederQ.task_done()
                    break
        except:
            print("do something with error handling queue")
            feederQ.task_done()
            break
        
        
            
        
if __name__ == '__main__':
    
    directory = os.getcwd()+"/1_archive"
    
    lock = multiprocessing.Lock()
    feederQueue = multiprocessing.JoinableQueue()
    feederWorker = multiprocessing.Process(target=feeder, args=(feederQueue,))
    dataWorkers = [multiprocessing.Process(target=preparing_file, args=(feederQueue,directory,)) for i in range(3)]
    feederWorker.start()
    for dataWorker in dataWorkers:
        dataWorker.deamon = True
        dataWorker.start()
        
    feederWorker.join()

    # stop workers
    for i in range(3):
        feederQueue.put(None)
    
    for i in range(3):
        dataWorker.join()
        print(dataWorker.is_alive())
    
    print(feederWorker.is_alive())

