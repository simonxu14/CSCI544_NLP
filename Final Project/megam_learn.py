import sys
import os
import math
import random

class megam_learn(object):


    global vsize            # vocabulary size
    global email_num        # the count of email in total
    global email_num_dev
    global map_all
    global array_map_ham
    global array_map_spam
    global b


    def main(self, filename):
        global vsize
        global email_num
        global email_num_dev
        global map_all
        global array_map_ham
        global array_map_spam
        global b

        vsize = 0
        email_num = 0
        email_num_dev = 0
        map_all = {}
        array_map_ham = []
        array_map_spam = []

        # if not os.path.exists('train'):                     #check if file name train exists
        #     print("There is no file named 'train'!")
        #     exit()

        path = os.getcwd() + '/' + 'train'
        # path = filename
        for file in os.listdir(path):                       #find the path of each email
            if '.txt' in file:
                real_path = path + '/' + file
                self.count(real_path)
            elif '.' not in file:
                path2 = path + '/' + file
                for file2 in os.listdir(path2):
                    if '.txt' in file2:
                        real_path = path2 + '/' + file2
                        self.count(real_path)
                    elif '.' not in file2:
                        path3 = path2 + '/' + file2
                        if '.' not in file2:
                            for file3 in os.listdir(path3):
                                if '.txt' in file3:
                                    real_path = path3 + '/' + file3
                                    self.count(real_path)
                                elif '.' not in file3:
                                    real_path = path3 + '/' + file3
                                    if '.txt' in real_path:
                                        self.count(real_path)


        # array_map_ham = array_map_ham[:int(len(array_map_ham)/10)]
        # array_map_spam = array_map_spam[:int(len(array_map_spam)/10)]
        # self.compute()


        outfile = open("word.txt", "w", encoding="latin1")
        i = 0
        for key in map_all:
            outfile.write(key + '\n')
            i += 1
        print(i)
        outfile.close()

        path = os.getcwd() + '/' + 'dev'
        # path = filename
        for file in os.listdir(path):                       #find the path of each email
            if '.txt' in file:
                real_path = path + '/' + file
                self.count_dev(real_path)
            elif '.' not in file:
                path2 = path + '/' + file
                for file2 in os.listdir(path2):
                    if '.txt' in file2:
                        real_path = path2 + '/' + file2
                        self.count_dev(real_path)
                    elif '.' not in file2:
                        path3 = path2 + '/' + file2
                        if '.' not in file2:
                            for file3 in os.listdir(path3):
                                if '.txt' in file3:
                                    real_path = path3 + '/' + file3
                                    self.count_dev(real_path)
                                elif '.' not in file3:
                                    real_path = path3 + '/' + file3
                                    if '.txt' in real_path:
                                        self.count_dev(real_path)

    def count_dev(self, infile):
        global email_num_dev

        if 'ham' in infile:
            type = True  # True means it's ham email
        else:
            type = False  # False means it's spam email

        email_num_dev += 1
        outfile = open("dev_new/" + str(email_num_dev) + "_" + str(type) + ".txt", "w", encoding="latin1")
        mail = open(infile, "r", encoding="latin1")
        cur_num = 0
        cur_map = {}
        for line in mail:
            line = line[:-1]
            word_array = line.split(" ")
            for word in word_array:
                if word == " " or word == "":
                    continue
                if not word.isalpha():
                    continue
                if word not in cur_map.keys():
                    cur_map[word] = 1
                else:
                    cur_map[word] += 1
                cur_num += 1
        for key in cur_map:
            outfile.write(key + '\t' + str(cur_map[key] / cur_num) + '\n')
        outfile.close()

        mail.close()



    def count(self, infile):
        global vsize
        global email_num
        global map_all
        global array_map_ham
        global array_map_spam

        # if (ham_num == 953 and 'ham' in infile) or (spam_num == 749 and 'spam' in infile):
        #     return


        email_num += 1
        mail = open(infile, "r", encoding="latin1")
        if 'ham' in infile:
            type = True  # True means it's ham email
        else:
            type = False  # False means it's spam email

        if type == True:
            map_ham = {}
            for line in mail:
                line = line[:-1]
                word_array = line.split(" ")
                for word in word_array:
                    if word == " " or word == "":
                        continue
                    if not word.isalpha():
                        continue
                    if word not in map_all.keys():
                        map_all[word] = 0
                        vsize += 1
                    if word not in map_ham.keys():
                        map_ham[word] = 1
                    else:
                        map_ham[word] += 1
            array_map_ham.append(map_ham)
        if type == False:
            map_spam = {}
            for line in mail:
                line = line[:-1]
                word_array = line.split(" ")
                for word in word_array:
                    if word == " " or word == "":
                        continue
                    if not word.isalpha():
                        continue
                    if word not in map_all.keys():
                        map_all[word] = 0
                        vsize += 1
                    if word not in map_spam.keys():
                        map_spam[word] = 1
                    else:
                        map_spam[word] += 1
            array_map_spam.append(map_spam)

        outfile = open("train_new/" + str(email_num) + "_" + str(type) + ".txt", "w", encoding="latin1")
        mail = open(infile, "r", encoding="latin1")
        cur_num = 0
        cur_map = {}
        for line in mail:
            line = line[:-1]
            word_array = line.split(" ")
            for word in word_array:
                if word == " " or word == "":
                    continue
                if not word.isalpha():
                    continue
                if word not in cur_map.keys():
                    cur_map[word] = 1
                else:
                    cur_map[word] += 1
                cur_num += 1
        for key in cur_map:
            outfile.write(key + '\t' + str(cur_map[key]/cur_num) + '\n')
        outfile.close()

        mail.close()





if __name__ == '__main__':
    # filename = sys.argv[1]
    filename = ""
    new_megam_learn = megam_learn()
    new_megam_learn.main(filename)