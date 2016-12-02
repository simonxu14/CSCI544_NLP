import sys
import os
import json
import math

global map_all
global b
global bb
global map_all_avg
global type

class per_classify(object):

    def main(self, filename, filename_out):

        global map_all
        global b
        global bb
        global map_all_avg
        global type

        file = open('per_model.txt', "r", encoding="latin1")
        for line in file:
            if 'b:' == line[:2]:
                b = int(line[line.find(':') + 1: -1])
                type = "regular"
            if 'bb:' == line[:3]:
                bb = float(line[line.find(':') + 1: -1])
                type = "average"
            if 'map_all:' == line[:8]:
                temp = line[line.find(':') + 1: -1]
                map_all = {}
                temp = temp[1:]
                temp = temp[:-1]
                list = temp.split(", ")
                for ele in list:
                    keyvalue = ele.split(": ")
                    key = keyvalue[0][1:-1]
                    value = int(keyvalue[1])
                    map_all[key] = value
            if 'map_all_avg:' == line[:12]:
                temp = line[line.find(':') + 1: -1]
                map_all_avg = {}
                temp = temp[1:]
                temp = temp[:-1]
                list = temp.split(", ")
                for ele in list:
                    keyvalue = ele.split(": ")
                    key = keyvalue[0][1:-1]
                    value = float(keyvalue[1])
                    map_all_avg[key] = value
            else:
                continue
        file.close()

        outfile = open(filename_out, "w", encoding="latin1")
        # outfile = open("per_output.txt", "w", encoding="latin1")
        self.find(filename)
        outfile.close()

        outfile = open(filename_out, "r", encoding="latin1")
        # outfile = open("per_output.txt", "r", encoding="latin1")
        result_ham = 0
        result_spam = 0
        ham_correct = 0
        spam_correct = 0
        for line in outfile:
            list = line.split(" ")
            result = list[0]
            if 'ham' in list[1]:
                real = 'ham'
            else:
                real = 'spam'
            if result == 'ham':
                result_ham += 1
                if real == 'ham':
                    ham_correct += 1
            if result == 'spam':
                result_spam += 1
                if real == 'spam':
                    spam_correct += 1
        precision_ham = ham_correct / result_ham
        precision_spam = spam_correct / result_spam
        # print("the precision of ham is " + str(precision_ham))
        # print("the precision of spam is " + str(precision_spam))
        outfile.close()

        outfile = open(filename_out, "r", encoding="latin1")
        # outfile = open("per_output.txt", "r", encoding="latin1")
        real_ham = 0
        real_spam = 0
        ham_correct = 0
        spam_correct = 0
        for line in outfile:
            list = line.split(" ")
            result = list[0]
            if 'ham' in list[1]:
                real = 'ham'
            else:
                real = 'spam'
            if real == 'ham':
                real_ham += 1
                if result == 'ham':
                    ham_correct += 1
            if real == 'spam':
                real_spam += 1
                if result == 'spam':
                    spam_correct += 1
        recall_ham = ham_correct / real_ham
        recall_spam = spam_correct / real_spam
        # print("the recall of ham is " + str(recall_ham))
        # print("the recall of spam is " + str(recall_spam))
        outfile.close()

        f1_ham = (2*precision_ham*recall_ham) / (precision_ham+recall_ham)
        f1_spam = (2*precision_spam*recall_spam) / (precision_spam+recall_spam)
        # print("the f1 of ham is " + str(f1_ham))
        # print("the f1 of spam is " + str(f1_spam))




    def find(self, filename):
        # if not os.path.exists('dev'):                     #check if file name train exists
        #     print("There is no file named 'dev'!")
        #     exit()
        # path = os.getcwd() + '/' + 'dev'
        path = filename
        for file in os.listdir(path):                       #find the path of each email
            if '.' not in file:
                path2 = path + '/' + file
                for file2 in os.listdir(path2):
                    path3 = path2 + '/' + file2
                    if '.' not in file2:
                        for file3 in os.listdir(path3):
                            real_path = path3 + '/' + file3
                            if '.txt' in real_path:
                                self.check(real_path, filename_out)

    def check(self, infile, filename_out):

        global map_all
        global b
        global bb
        global map_all_avg
        global type

        mail = open(infile, "r", encoding="latin1")
        a = 0
        if type == "regular":
            for line in mail:
                word_array = line.split()
                for word in word_array:
                    if word == "Subject:":
                        continue
                    elif word not in map_all.keys():
                        continue
                    else:
                        a += map_all[word]

            if a+b > 0:
                result = "spam"
            else:
                result = "ham"
            file = open(filename_out, "a", encoding="latin1")
            # file = open("per_output.txt", "a", encoding="latin1")
            file.write(result + ' ' + infile + '\n')
            file.close()
        if type == "average":
            for line in mail:
                word_array = line.split()
                for word in word_array:
                    if word == "Subject:":
                        continue
                    elif word not in map_all_avg.keys():
                        continue
                    else:
                        a += map_all_avg[word]

            if a + bb > 0:
                result = "spam"
            else:
                result = "ham"
            file = open(filename_out, "a", encoding="latin1")
            # file = open("per_output.txt", "a", encoding="latin1")
            file.write(result + ' ' + infile + '\n')
            file.close()




if __name__ == '__main__':
    filename = sys.argv[1]
    filename_out = sys.argv[2]
    # filename = ""
    # filename_out = ""
    new_per_classify = per_classify()
    new_per_classify.main(filename, filename_out)