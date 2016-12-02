import sys
import os
import math

class nblearn(object):


    global vsize            # vocabulary size
    global email_num        # the count of email in total
    global ham_num          # the count of ham email
    global spam_num         # the count of spam email
    global word_ham         # the count of word in ham email
    global word_spam        # the count of word in spam email
    global map_ham          # the hashmap of ham email
    global map_spam         # the hashmap of spam email


    def main(self, filename):
        global vsize
        global email_num
        global ham_num
        global spam_num
        global word_ham
        global word_spam
        global map_ham
        global map_spam
        vsize = 0
        email_num = 0
        ham_num = 0
        spam_num = 0
        word_ham = 0
        word_spam = 0
        map_ham = {}
        map_spam = {}

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
        # print(ham_num)
        # print(spam_num)
        p_ham = ham_num/email_num          #the p of ham
        p_spam = spam_num/email_num        #the p of spam
        p_ham_map = {}                     #the p of each word in ham
        p_spam_map = {}                    #the p of each word in spam
        self.compute_ham_map(p_ham_map)
        self.compute_spam_map(p_spam_map)


        outfile = open("nbmodel.txt", "w", encoding="latin1")
        outfile.write('p_ham' + ":" + str(p_ham) + '\n')
        outfile.write('p_spam' + ":" + str(p_spam) + '\n')
        outfile.write('p_ham_map' + ":" + str(p_ham_map) + '\n')
        outfile.write('p_spam_map' + ":" + str(p_spam_map)+ '\n')
        # print(len(map_ham))
        outfile.close()


        # common_word = []
        # for ele in map_ham.keys():
        #     if map_ham[ele] > 200 and map_spam[ele] > 200:
        #         common_word.append(ele)
        # outfile = open("nbmodel.txt", "a", encoding="latin1")
        # outfile.write('common_word' + ":" + str(common_word) + '\n')
        # outfile.close()




    def count(self, infile):
        global vsize
        global email_num
        global ham_num
        global spam_num
        global word_ham
        global word_spam
        global map_ham
        global map_spam
        # if (ham_num == 953 and 'ham' in infile) or (spam_num == 749 and 'spam' in infile):
        #     return

        email_num += 1
        mail = open(infile, "r", encoding="latin1")
        if 'ham' in infile:
            type = True         #True means it's ham email
            ham_num += 1
        else:
            type = False        #False means it's spam email
            spam_num += 1

        if type == True:                              #if it's spam email
            for line in mail:
                word_array = line.split(" ")
                for word in word_array:
                    word_ham += 1
                    if word in map_ham.keys() and word in map_spam.keys():
                        map_ham[word] += 1
                    elif word in map_ham.keys() and word not in map_spam.keys():
                        map_ham[word] += 1
                        map_spam[word] = 0
                    elif word not in map_ham.keys() and word in map_spam.keys():
                        map_ham[word] = 1
                    else:
                        map_ham[word] = 1
                        map_spam[word] = 0
                        vsize += 1
        else:                                         #if it's spam email
            for line in mail:
                word_array = line.split(" ")
                for word in word_array:
                        word_spam += 1
                        if word in map_spam.keys() and word in map_ham.keys():
                            map_spam[word] += 1
                        elif word in map_spam.keys() and word not in map_ham.keys():
                            map_spam[word] += 1
                            map_ham[word] = 0
                        elif word not in map_spam.keys() and word in map_ham.keys():
                            map_spam[word] = 1
                        else:
                            map_spam[word] = 1
                            map_ham[word] = 0
                            vsize += 1
        mail.close()



    def compute_ham_map(self, p_ham_map):
        global word_ham
        global map_ham
        for key in map_ham:
            p_key = math.log2((map_ham[key] + 1) / (word_ham + vsize))
            # p_key = math.log2((map_ham[key] + 1) / (word_ham + vsize))
            p_ham_map[key] = p_key

    def compute_spam_map(self, p_spam_map):
        global vsize
        global word_spam
        global map_spam
        for key in map_spam:
            p_key = math.log2((map_spam[key] + 1) / (word_spam + vsize))
            # p_key = math.log2((map_ham[key] + 1) / (word_ham + vsize))
            p_spam_map[key] = p_key


if __name__ == '__main__':
    filename = sys.argv[-1]
    new_nblearn = nblearn()
    new_nblearn.main(filename)