from collections import Counter
import math
import numpy as np
from sklearn import metrics
import subprocess
import re
import pandas as pd
import numpy as np

for test_number in range(1,100):
    print('epoch',test_number)
    tags = ['B-ORG', 'I-ORG', 'I-PER', 'MO', 'B-LOC', 'I-LOC', 'B-MISC', 'I-MISC', 'O']

    W = {}

    def refer_W(feature): # feature: ('equit','NN');('NN','VB')
        if feature not in W:
            return 0
        else:
            return W[feature]

    def tag_tag(): # ('NN','NN')
        P_tags  =[] 
        for i in tags:
            tp_P_tags = []
            for j in tags:
                tp_P_tags.append(refer_W(('pt '+j,'t '+i)))
            P_tags.append(tp_P_tags)
        P_tags = np.asarray(P_tags)
        return P_tags


    def Viterbi(sentence): # Sentence: ['equit','will','increase'] --> []
        predic_label = []

        aug_tokens = ['__SENTINEL__ O', '__SENTINEL__ O'] + sentence + ['__SENTINEL__ O', '__SENTINEL__ O']
        i= 0

        for ppw_, pw_, w_, nw_, nnw_ in zip(aug_tokens, aug_tokens[1:], aug_tokens[2:], aug_tokens[3:], aug_tokens[4:]):
            # NOTE: No pt, ppt attribs currently
            ppw = ppw_.split(' ')[0]
            pw = pw_.split(' ')[0]
            w = w_.split(' ')[0]
            nw = nw_.split(' ')[0]
            nnw = nnw_.split(' ')[0]
            
            ppt = ppw_.split(' ')[1]
            pt = pw_.split(' ')[1]
            t = w_.split(' ')[1]
            nt = nw_.split(' ')[1]
            nnt = nnw_.split(' ')[1]
            
            
            attribs = {'ppw ' + ppw,
                       'pw ' + pw,
                       'w ' + w,
                       'nw ' + nw,
                       'nnw ' + nnw,
                       'ppt '+ppt,
                       'pt '+pt,
                       't '+t,
                       'nt '+nt,
                       'nnt '+nnt
                       }
            
#             for j in range(1, 5):
#                 attribs.add('pref ' + w[:j])
#                 attribs.add('suff ' + w[-j:][::-1])
            if re.search('[0-9]', w):
                attribs.add('dig __NONE__')
            if re.search('[A-Z]', w):
                attribs.add('uc __NONE__')
            if '-' in w:
                attribs.add('hyph __NONE__')

            tag_list = []
            for tag in tags:
                tag_number = 0
                for each in attribs:
                    if each+'\t'+tag in W:
                        tag_number += W[each+'\t'+tag]

                tag_list.append(tag_number)
                
            if i == 0:
                data = sentence[i]
                first_level = []
                for tag_number in range(len(tags)):   
                    first_level.append((refer_W(('pt'+'','t '+tag))+tag_list[tag_number]))
                predic_label.append(tags[first_level.index(max(first_level))])
                next_value = first_level
            else:
                data = sentence[i]
                probility = ((next_value + tag_tag()).T + [tag_list[tag_number] for tag_number in range(len(tags))]).T
                predic_label.append(tags[probility.max(axis=1).argmax()])
                next_value = probility.max(axis=1)

            i+=1
    #         predic_label.append(tags[tag_list.index(max(tag_list))])
        return predic_label

    def create_features(sentence,tags): # sentence :['equit','will','increase'] ; tags: ['nn','nn','nn'] --> {}
        changed = {}
        aug_tokens = ['__SENTINEL__ O', '__SENTINEL__ O'] + sentence + ['__SENTINEL__ O', '__SENTINEL__ O']

        index_number = 0
        for ppw_, pw_, w_, nw_, nnw_ in zip(aug_tokens, aug_tokens[1:], aug_tokens[2:], aug_tokens[3:], aug_tokens[4:]):
        # NOTE: No pt, ppt attribs currently
            ppw = ppw_.split(' ')[0]
            pw = pw_.split(' ')[0]
            w = w_.split(' ')[0]
            nw = nw_.split(' ')[0]
            nnw = nnw_.split(' ')[0]
            
            ppt = ppw_.split(' ')[1]
            pt = pw_.split(' ')[1]
            t = w_.split(' ')[1]
            nt = nw_.split(' ')[1]
            nnt = nnw_.split(' ')[1]
            
            
            attribs = {'ppw ' + ppw,
                       'pw ' + pw,
                       'w ' + w,
                       'nw ' + nw,
                       'nnw ' + nnw
                       }
#             for j in range(1, 5):
#                 attribs.add('pref ' + w[:j])
#                 attribs.add('suff ' + w[-j:][::-1])
            if re.search('[0-9]', w):
                attribs.add('dig __NONE__')
            if re.search('[A-Z]', w):
                attribs.add('uc __NONE__')
            if '-' in w:
                attribs.add('hyph __NONE__')

            for each in attribs:
                if each+'\t'+tags[index_number] not in changed:
                    changed[each+'\t'+tags[index_number]] = 1
                else:
                    changed[each+'\t'+tags[index_number]] += 1
                    
            attribs = {
                       'ppt '+ppt,
                       'pt '+pt,
                       't '+t,
                       'nt '+nt,
                       'nnt '+nnt
                        }
            
            for each in attribs:
                if each+'\t'+tags[index_number] not in changed:
                    changed[each+'\t'+tags[index_number]] = 0.01
                else:
                    changed[each+'\t'+tags[index_number]] += 0.01

            index_number += 1

        for i in range(len(tags)+1):
            if i == 0:
                first_tag = 'pt '+''
            else:
                first_tag = 'pt '+tags[i-1]

            if i == len(tags):
                next_tag = 't '+''
            else:
                next_tag = 't '+tags[i]

                if (first_tag,next_tag) not in changed:
                    changed[(first_tag,next_tag)] = 0.01#create_trans((tags[i-1],tags[i]))
                else:
                    changed[(first_tag,next_tag)] += 0.01#create_trans((tags[i-1],tags[i]))

        return changed

    def training(data):

        for epoch in range(test_number):
            for each in data:
                pre_label = Viterbi(each[0])
                # add
                if each[1] != pre_label:
    #                 print(' '.join(each[1])+'->'+' '.join(pre_label))
                    true_changed = create_features(each[0],each[1])
                    pre_changed = create_features(each[0],pre_label)
    #                 print(true_changed)
                    for add in true_changed:
                        if add not in W:
                            W[add] = true_changed[add]
                        else:
                            W[add] += true_changed[add]

                    # minus
                    for minus in pre_changed:
                        if minus not in W:
                            W[minus] = -pre_changed[minus]
                        else:
                            W[minus] -= pre_changed[minus]



    def test(data):
        subprocess.run("rm -r result.txt", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        for each in data:
            pred_label = Viterbi(each[0])
    #         true_changed = create_features(each[0],each[1])
    #         pre_changed = create_features(each[0],pred_label)
            # add

            with open('result.txt','a+') as w:
                w.write('\n')
                for i in range(len(each[0])):
                    w.write(each[0][i]+' '+each[1][i]+' '+pred_label[i]+'\n')


    training_data = 'conll03/eng.train'
    testing_data = 'conll03/eng.testa'

    data = []
    sentence_word = []
    sentence_tag = []
    with open(training_data,'r+') as f: # Generate the Log of emission
        lines = f.readlines()
        lines_ = list(filter(lambda x: x !=lines[0], lines))
        for item in lines_:
            if item == '\n':
                if sentence_word != []:
                    data.append((sentence_word,sentence_tag))
                sentence_word = []
                sentence_tag = []

            else:
                sentence_word.append(' '.join(item.strip().split(' ')[:2]))
#                 sentence_word.append(item.strip().split(' ')[0])
                sentence_tag.append(item.strip().split(' ')[-1])  

    training(data)

    data = []
    sentence_word = []
    sentence_tag = []
    with open(testing_data,'r+') as f: # Generate the Log of emission
        lines = f.readlines()
        lines_ = list(filter(lambda x: x !=lines[0], lines))
        for item in lines_:
            if item == '\n':
                if sentence_word != []:
                    data.append((sentence_word,sentence_tag))
                sentence_word = []
                sentence_tag = []

            else:
                sentence_word.append(' '.join(item.strip().split(' ')[:2]))
#                 sentence_word.append(item.strip().split(' ')[0])
                sentence_tag.append(item.strip().split(' ')[-1])
    test(data)

    print('\nEnvoluation:\n')
    output = subprocess.run("/usr/bin/perl -w conlleval < result.txt", shell=True, stdout=subprocess.PIPE, 
                            universal_newlines=True)
    print(output.stdout)