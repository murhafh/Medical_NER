#!/usr/bin/env python

# This script is used to convert the corpus files in http://biotext.berkeley.edu/data/dis_treat_data.html
# to a tsv format where every word is tagged with a SYMP tag or O 
# The tsv files will be then used to train a Stanford NER model
# The script by default will take the three files in corpus/ directory with their original names 
# The file names can be also provided by a comand line argument as a coma separated list.
# The output tsv files will be stored in the same location as the original txt files.

import codecs
import re
import nltk
import argparse

def clean_text(line=''):
    # Remove relation info if exists
    if '||' in line:
        line = line.split('||')[0]
    # Remove irrelevant tags
    match = re.search(r'<(YES|TO_SEE)>(.*?)</(YES|TO_SEE)>',line)
    if match:
        line = match.group(1)

    # Sometimes they don't have closing tag
    line = re.sub('<TO_SEE>', '', line)

    # remove non tags > < symbols
    if '< ' in line or ' >' in line:
        line = re.sub('< ', 'less than ', line)
        line = re.sub(' >', ' greater than', line)
    return line
    
def convert_files(filenames = []):
    for filename in filenames:
        with codecs.open(filename, 'r', 'ISO-8859-1') as input_file:
            with codecs.open(re.sub('.txt', '_ner.tsv', filename), 'w', 'utf-8') as output_file:
                for line in input_file:
                    line = clean_text(line)
                    tokenized_words = nltk.word_tokenize(line)
                    i = 0
                    while i < len(tokenized_words):
                        tag = ''
                        entity = ''
                        if tokenized_words[i] == '<' and '/' not in tokenized_words[i+1]:
                            # Ignore treatment tags and set everything else to SYMP
                            # In another test try including all tags as SYMP
                            if 'TREAT' in tokenized_words[i + 1]:
                                tag = 'O'
                            else:
                                tag = 'SYMP'
                            i += 2

                            while i < len(tokenized_words):
                                i += 1
                                if tokenized_words[i] == '<':
                                    break
                                output_file.write(tokenized_words[i] + '\t' + tag + '\n')
                        elif tokenized_words[i] == '<' and '/' in tokenized_words[i+1]:
                            # ignore the closing tag
                            i += 3
                        else:
                            output_file.write(tokenized_words[i] + '\tO\n')
                            i += 1

default_filenames = 'corpus/sentences_with_roles_and_relations.txt,corpus/labeled_abstracts.txt,corpus/labeled_titles.txt'

parser = argparse.ArgumentParser(description = 'This script is used to convert the corpus .txt files into tsv files suitable for training')
parser.add_argument('-f', '--filenames', default = default_filenames,
                    help = 'filname or coma separated filenames to convert to tsv format')
args = parser.parse_args()

filenames = args.filenames.split(',')
convert_files(filenames)