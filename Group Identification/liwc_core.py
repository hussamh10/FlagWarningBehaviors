# -*- coding: utf-8 -*-
import argparse, codecs, os, sys

class liwc:
    def load_liwc_dict(self, liwcdic_file):
        file_content = codecs.open(liwcdic_file, "r", "utf-8").read()
        cate_text = file_content[file_content.find("%")+1:file_content[1:].find("%")].strip()
        for line in cate_text.split("\n"):
            self.liwc_cate_name_by_number[int(line.strip().split("\t")[0])] = line.strip().split("\t")[1]

        dict_text = file_content[file_content[1:].find("%")+2:].strip()
        for line in dict_text.split("\n"):
            self.liwc_cate_number_by_word[line.strip().split("\t")[0]] = set([int(item) for item in line.strip().split("\t")[1:]])

    def __init__(self, liwcdic_file):
        categories = ["WC","funct","pronoun","ppron","i","we","you","shehe","they","ipron","article","prep","auxverb","adverb","conj","negate","verb","adj","compare","interrog","number","quant","affect","posemo","negemo","anx","anger","sad","social","family","friend","female","male","cogproc","insight","cause","discrep","tentat","certain","differ","percept","see","hear","feel","bio","body","health","sexual","ingest","drives","affiliation","achieve","power","reward","risk","focuspast","focuspresent","focusfuture","relativ","motion","space","time","work","leisure","home","money","relig","death","informal","swear","netspeak","assent","nonflu","filler"]
        self.liwc_category_names = ["WC"] + categories
        self.liwc_cate_name_by_number = {}
        self.liwc_cate_number_by_word = {}

        if os.path.exists(liwcdic_file) == False:
            print ("Cannot find LIWC dict file (path: %s)"%(liwcdic_file))
            sys.exit()
        else:
            self.load_liwc_dict(liwcdic_file)

    def liwcify(self, text, percentage=False):
        count_by_categories = {"WC":0}
        for c in self.liwc_category_names:
            count_by_categories[c] = 0

        count_by_categories["WC"] = len(text.split())

        for word in text.split():

            cate_numbers_word_belongs = set([])
            if word in self.liwc_cate_number_by_word:
                cate_numbers_word_belongs = self.liwc_cate_number_by_word[word]

            else:

                word = word[:-1]
                while len(word) > 0:
                    if (word+"*") in self.liwc_cate_number_by_word:
                        cate_numbers_word_belongs = self.liwc_cate_number_by_word[word+"*"]
                        break
                    else:
                        word = word[:-1]

            for num in cate_numbers_word_belongs:
                count_by_categories[self.liwc_cate_name_by_number[num]] += 1

        if percentage:
            keys = list(count_by_categories.keys())
            percentages = {"WC": count_by_categories['WC']}
            for k in keys[1:]:
                percentages[k] = int((count_by_categories[k]/count_by_categories['WC'])*100)

            return percentages

        return count_by_categories
