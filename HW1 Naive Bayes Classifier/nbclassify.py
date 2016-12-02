import sys
import os
import json
import math

global p_ham
global p_spam
global p_ham_map
global p_spam_map
# global common_word

class nbclassify(object):
    def main(self, filename):

        global p_ham
        global p_spam
        global p_ham_map
        global p_spam_map
        # global common_word
        common_word = []
        file = open('nbmodel.txt', "r", encoding="latin1")
        for line in file:
            if 'p_ham:' == line[:6]:
                p_ham = float(line[line.find(':') + 1 : -1])
            elif 'p_spam:' == line[:7]:
                p_spam = float(line[line.find(':') + 1 : -1])
            elif 'p_ham_map:' == line[:10]:
                temp = line[line.find(':') + 1 : -1]
                p_ham_map = {}
                temp = temp[1:]
                temp = temp[:-1]
                list = temp.split(", ")
                for ele in list:
                    keyvalue = ele.split(": ")
                    key = keyvalue[0][1:-1]
                    value = float(keyvalue[1])
                    p_ham_map[key] = value
            elif 'p_spam_map:' == line[:11]:
                temp = line[line.find(':') + 1: -1]
                p_spam_map = {}
                temp = temp[1:]
                temp = temp[:-1]
                list = temp.split(", ")
                for ele in list:
                    keyvalue = ele.split(": ")
                    key = keyvalue[0][1:-1]
                    value = float(keyvalue[1])
                    p_spam_map[key] = value
            # elif 'common_word:' == line[:12]:
            #     temp = line[line.find(':') + 1: -1]
            #     temp = temp[1:]
            #     temp = temp[:-1]
            #     list = temp.split(", ")
            #     for ele in list:
            #         key = ele[1:-1]
            #         common_word.append(key)
            #     print(common_word)
            else:
                continue
        file.close()
        outfile = open("nboutput.txt", "w", encoding="latin1")
        self.find(filename)
        outfile.close()

        outfile = open("nboutput.txt", "r", encoding="latin1")
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

        outfile = open("nboutput.txt", "r", encoding="latin1")
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
                                self.check(real_path)

    def check(self, infile):
        global p_ham
        global p_spam
        global p_ham_map
        global p_spam_map
        # global common_word

        result = 1
        p_msg_ham = 1
        p_msg_spam = 1
        mail = open(infile, "r", encoding="latin1")
        for line in mail:
            word_array = line.split()
            for word in word_array:
                if word == "Subject:":
                    continue
                elif word not in p_ham_map.keys():
                    continue
                # elif word in common_word:
                #     continue
                else:
                    p_msg_ham += p_ham_map[word]
                    p_msg_spam += p_spam_map[word]

        if p_ham + p_msg_ham > p_spam + p_msg_spam:
            result = "ham"
        else:
            result = "spam"
        file = open('nboutput.txt', "a", encoding="latin1")
        file.write(result + ' ' + infile + '\n')
        file.close()




if __name__ == '__main__':
    filename = sys.argv[-1]
    new_nbclassify = nbclassify()
    new_nbclassify.main(filename)