from collections import Counter
import math
import numpy as np
from sklearn import metrics
import subprocess

for run_times in range(1,11):
    print('epoch %d'%run_times)
    tags = ['B-ORG', 'I-ORG', 'I-PER', 'MO', 'B-LOC', 'I-LOC', 'B-MISC', 'I-MISC', 'O']

    W = {}

    def refer_W(feature): # feature: ('equit','NN');('NN','VB')
        if feature not in W:
            return -1
        else:
            return W[feature]

    def tag_tag(): # ('NN','NN')
        P_tags  =[] 
        for i in tags:
            tp_P_tags = []
            for j in tags:
                tp_P_tags.append(refer_W((j,i)))
            P_tags.append(tp_P_tags)
        P_tags = np.asarray(P_tags)
        return P_tags

    def Viterbi(sentence): # Sentence: ['equit','will','increase'] --> []
        predic_label = []
        for i in range(len(sentence)):
            if i == 0:
                data = sentence[i]
                first_level = []
                for tag in tags:   
                    first_level.append((refer_W(('<s>',tag))+refer_W((data,tag))))
                predic_label.append(tags[first_level.index(max(first_level))])
                next_value = first_level
            else:
                data = sentence[i]
                probility = ((next_value + tag_tag()).T + [refer_W((data,tag)) for tag in tags]).T
                predic_label.append(tags[probility.max(axis=1).argmax()])
                next_value = probility.max(axis=1)
        return predic_label


    def create_features(sentence,tags): # sentence :['equit','will','increase'] ; tags: ['nn','nn','nn'] --> {}
        changed = {}
        for i in range(len(tags)+1):
            if i == 0:
                first_tag = '<s>'
            else:
                first_tag = tags[i-1]

            if i == len(tags):
                next_tag = '<s>'
            else:
                next_tag = tags[i]

                if (tags[i-1],tags[i]) not in changed:
                    changed[(tags[i-1],tags[i])] = 0.01#create_trans((tags[i-1],tags[i]))
                else:
                    changed[(tags[i-1],tags[i])] += 0.01#create_trans((tags[i-1],tags[i]))

        for i in range(len(tags)):
            if (sentence[i],tags[i]) is not changed:
                changed[(sentence[i],tags[i])] = 1#create_emit((sentence[i],tags[i]))
            else:
                changed[(sentence[i],tags[i])] += 1#create_emit((sentence[i],tags[i]))
        return changed

    def training(data):
        for epoch in range(run_times):
            sum_lost = 0
            for each in data:
                pre_label = Viterbi(each[0])
                true_changed = create_features(each[0],each[1])
                pre_changed = create_features(each[0],pre_label)
                # add

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

                for i in range(len(each[1])):
                    if tags.index(each[1][i]) != tags.index(pre_label[i]):
                        sum_lost += 1
            print('The epoch:%d : '%epoch,'Loss:',sum_lost)

    def test(data):
        subprocess.run("rm -r result.txt", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        for each in data:
            pred_label = Viterbi(each[0])

            with open('result.txt','a+') as w:
                w.write('\n')
                for i in range(len(each[0])):
                    w.write(each[0][i]+' '+each[1][i]+' '+pred_label[i]+'\n')
        # 3
        print('\nEnvoluation:\n')
        output = subprocess.run("/usr/bin/perl -w conlleval < result.txt", shell=True, stdout=subprocess.PIPE, 
                                universal_newlines=True)
        print(output.stdout)


    training_data = 'conll03/deu.train'
    testing_data = 'conll03/deu.testa'

    data = []
    sentence_word = []
    sentence_tag = []
    with open(training_data,'r+',encoding='cp1252') as f: # Generate the Log of emission
        lines = f.readlines()
        lines_ = list(filter(lambda x: x !=lines[0], lines))
        for item in lines_:
            if item == '\n':
                if sentence_word != []:
                    data.append((sentence_word,sentence_tag))
                sentence_word = []
                sentence_tag = []

            else:
                sentence_word.append(item.strip().split(' ')[0])
                sentence_tag.append(item.strip().split(' ')[-1])   


    training(data)


    data = []
    sentence_word = []
    sentence_tag = []
    with open(testing_data,'r+',encoding='cp1252') as f: # Generate the Log of emission
        lines = f.readlines()
        lines_ = list(filter(lambda x: x !=lines[0], lines))
        for item in lines_:
            if item == '\n':
                if sentence_word != []:
                    data.append((sentence_word,sentence_tag))
                sentence_word = []
                sentence_tag = []

            else:
                sentence_word.append(item.strip().split(' ')[0])
                sentence_tag.append(item.strip().split(' ')[-1])
    test(data)