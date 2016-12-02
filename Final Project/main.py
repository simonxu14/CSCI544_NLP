import os
import math
import sys

textNum = 17029
wordNum = 97818
ctgyNum = 2
weight = [[0 for x in range(ctgyNum)] for y in range(wordNum)]
ctgyName = ['spam', 'ham']
words = {}
E_P = [[0.0 for x in range(ctgyNum)] for y in range(wordNum)]
texts = [0 for x in range(textNum)]
category = [0 for x in range(textNum)]




def is_zero(x):
    return (x - 1e-17 < 0)


def updateWeight():
    E_P2 = [[0.0 for x in range(ctgyNum)] for y in range(wordNum)]
    prob = [[0.0 for x in range(ctgyNum)] for y in range(textNum)]
    for i in range(textNum):
        zw = 0.0
        for j in range(ctgyNum):
            tmp = 0.0
            for (k, v) in texts[i].items():
                tmp += weight[k][j] * v
            tmp = math.exp(tmp)
            zw += tmp
            prob[i][j] = tmp
        for j in range(ctgyNum):
            if is_zero(zw): continue
            prob[i][j] /= zw

    for x in range(textNum):
        ctgy = category[x]
        for (k, v) in texts[x].items():
            E_P2[k][ctgy] += (prob[x][ctgy] * v)

    for i in range(wordNum):
        for j in range(ctgyNum):
            if is_zero(E_P2[i][j]) | is_zero(E_P[i][j]):
                continue
            weight[i][j] += math.log(E_P[i][j] / E_P2[i][j])


def modelTest():
    testFiles = os.listdir(os.getcwd() + '/' + 'dev_new')
    errorCnt = 0
    totalCnt = 0
    matrix = [[0 for x in range(ctgyNum)] for y in range(ctgyNum)]
    for fname in testFiles:

        lines = open(os.getcwd() + '/' + 'dev_new/' + fname, "r", encoding="latin1").readlines()
        if "True" in fname:
            ctgy = 1
        else:
            ctgy = 0
        probEst = [0.0 for x in range(ctgyNum)]
        for line in lines:
            arr = line.split('\t')
            if arr[0] not in words: continue
            word_id = words[arr[0]]
            freq = float(arr[1])
            for index in range(ctgyNum):
                probEst[index] += (weight[word_id][index] * freq)
        ctgyEst = 0
        maxProb = -1
        for index in range(ctgyNum):
            if probEst[index] > maxProb:
                ctgyEst = index
                maxProb = probEst[index]
        totalCnt += 1
        if ctgyEst != ctgy: errorCnt += 1
        matrix[ctgy][ctgyEst] += 1
    print ("%-5s" % ("type"),)
    for i in range(ctgyNum):
        print ("%-5s" % (ctgyName[i]),)
    print ('\n',)
    for i in range(ctgyNum):
        print ("%-5s" % (ctgyName[i]),)
        for j in range(ctgyNum):
            print ("%-5d" % (matrix[i][j]),)
        print ('\n',)
    precision_ham = matrix[1][1]/(matrix[1][1] + matrix[1][0])
    precision_spam = matrix[0][0] / (matrix[0][1] + matrix[0][0])
    recall_ham = matrix[1][1]/(matrix[1][1] + matrix[0][1])
    recall_spam = matrix[0][0] / (matrix[0][0] + matrix[1][0])
    f1_ham = (2 * precision_ham * recall_ham) / (precision_ham + recall_ham)
    f1_spam = (2 * precision_spam * recall_spam) / (precision_spam + recall_spam)
    print("precision_ham:" + str(precision_ham))
    print("precision_spam:" + str(precision_spam))
    print("recall_ham:" + str(recall_ham))
    print("recall_spam:" + str(recall_spam))
    print("f1_ham:" + str(f1_ham))
    print("f1_spam:" + str(f1_spam))
    # print ("total num:" + str(totalCnt) + "  wrong:" + str(errorCnt) + "  wrong rate:" + str(errorCnt / float(totalCnt)))


def init():
    i = 0
    lines = open(os.getcwd() + '/' + 'word.txt',"r", encoding="latin1").readlines()
    for word in lines:
        word = word.strip()
        words[word] = i
        i += 1
    print(i)
    files = os.listdir(os.getcwd() + '/' + 'train_new')
    index = 0
    for fname in files:
        wf = {}
        lines = open(os.getcwd() + '/' + 'train_new/' + fname, "r", encoding="latin1").readlines()
        if "True" in fname:
            ctgy = 1
        else:
            ctgy = 0
        category[index] = ctgy
        for line in lines:
            arr = line.split('\t')
            word_id = words[arr[0]]
            freq = float(arr[1])
            wf[word_id] = freq
            E_P[word_id][ctgy] += freq
        texts[index] = wf
        index += 1
    print(wf)


def train():
    for loop in range(10):
        print ("result:")
        updateWeight()
        modelTest()


if __name__ == '__main__':
    print ("init")
    init()
    print ("tain")
    train()