import sys
import os
import math
import random

class per_learn(object):


    global vsize            # vocabulary size
    global email_num        # the count of email in total
    global map_all
    global array_map_ham
    global array_map_spam
    global b


    def main(self, filename):
        global vsize
        global email_num
        global map_all
        global array_map_ham
        global array_map_spam
        global b

        vsize = 0
        email_num = 0
        map_all = {}
        array_map_ham = []
        array_map_spam = []

        # if not os.path.exists('train'):                     #check if file name train exists
        #     print("There is no file named 'train'!")
        #     exit()
        # path = os.getcwd() + '/' + 'train'
        path = filename
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
        self.compute()




        outfile = open("per_model.txt", "w", encoding="latin1")
        outfile.write('b' + ":" + str(b) + '\n')
        outfile.write('map_all' + ":" + str(map_all) + '\n')
        outfile.close()






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
                word_array = line.split(" ")
                for word in word_array:
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
                word_array = line.split(" ")
                for word in word_array:
                    if word not in map_all.keys():
                        map_all[word] = 0
                        vsize += 1
                    if word not in map_spam.keys():
                        map_spam[word] = 1
                    else:
                        map_spam[word] += 1
            array_map_spam.append(map_spam)
        mail.close()



    def compute(self):
        global vsize
        global email_num
        global map_all
        global array_map_ham
        global array_map_spam
        global b

        length_ham = len(array_map_ham)
        length_spam = len(array_map_spam)

        b = 0
        flag = 0
        while flag < 20:
            array_select = random.sample(range(length_ham+length_spam), length_ham+length_spam)
            # print(array_select)
            for i in range(len(array_select)):
                if array_select[i] < length_ham:
                    # print("A")
                    a = 0
                    map_ham = array_map_ham[array_select[i]]
                    for ele in map_ham:
                        a += map_all[ele] * map_ham[ele]
                    a += b  # a = wx + b
                    if a * (-1) <= 0:
                        for ele in map_ham:
                            map_all[ele] += (-1) * map_ham[ele]  # w = w + yx
                        b += (-1)
                else:
                    # print("B")
                    a = 0
                    map_spam = array_map_spam[array_select[i]-length_ham]
                    for ele in map_spam:
                        a += map_all[ele] * map_spam[ele]
                    a += b  # a = wx + b
                    if a * 1 <= 0:
                        for ele in map_spam:
                            map_all[ele] += (1) * map_spam[ele]  # w = w + yx
                        b += 1
            flag += 1







if __name__ == '__main__':
    filename = sys.argv[1]
    # filename = ""
    new_per_learn = per_learn()
    new_per_learn.main(filename)