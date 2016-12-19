#!/usr/bin/env python


# This script prints out symptom entities found in NHS sample pages
# You can either pass a single URL or a json file with a list of URLs
# Check -h for more info

import nltk
from html_reader import HTMLReader
from nltk.tag.stanford import NERTagger
import json
import argparse

def print_symptoms_from_json(json_file = '', model = '', stanford_jar = ''):
    with open(json_file) as url_file:
        urls = json.load(url_file)['urls']
    for url in urls:
        print "Symptoms in URL: %s" % url
        print_symptoms_from_page(url = url, model = model, stanford_jar = stanford_jar)

def print_symptoms_from_page(url = '', model = '', stanford_jar = ''):
    html_reader = HTMLReader(url)
    cleaned_text = html_reader.get_text_from_page()
    symptoms = set()

    st = NERTagger(model, stanford_jar, encoding='utf-8')
    sentences = nltk.sent_tokenize(cleaned_text)
    for sentence in sentences:
        tags = st.tag(nltk.word_tokenize(sentence))
        tag_index = 0
        while tag_index < len(tags):
            if tags[tag_index][1] == 'SYMP':
                symptom = []
                while tag_index < len(tags) and tags[tag_index][1] != 'O':
                    symptom.append(tags[tag_index][0])
                    tag_index += 1
                symptoms.add(' '.join(symptom))
            else:
                tag_index += 1
    print "Found %d symptoms:" % len(symptoms)
    for symptom in symptoms:
        print symptom

parser = argparse.ArgumentParser(description = 'This script is used to print symptom entities in NHS pages')
parser.add_argument('-u', '--url', default = '',
                    help = 'URL of the page to find symptom entities in')
parser.add_argument('-j', '--json', default = '',
                    help = 'The json file containing a list of pages to find symptom entities in')
parser.add_argument('-m', '--model', default = 'model/medical-er-model.ser2.gz',
                    help = 'The trained model to use in classification')
parser.add_argument('-jar', '--jar', default = 'stanford-ner/stanford-ner.jar',
                    help = 'The Stanford NER jar file')
args = parser.parse_args()

if args.url:
    print_symptoms_from_page(url = args.url, model = args.model, stanford_jar = args.jar)
elif args.json:
    print_symptoms_from_json(args.json, model = args.model, stanford_jar = args.jar)
    