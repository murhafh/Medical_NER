# Symptoms Entity Recognition

### Approach:
The problem of finding symptom entities in text is similar to Named Entity Recognition problem, the issue is that it was very difficult to find datasets where the symptoms are tagged so can be used in training a model to predict whether some word sequence is a symptom.

This [website](http://biotext.berkeley.edu/data/dis_treat_data.html) has some tagged data. The dataset is not very big which makes it less suitable to use in a Word2Vec model, and also the symptoms are not tagged as symptoms but are actually mixed with disease tags, it also has some tag info for treatments.

To create a named entity recognition model I converted the dataset into tsv format where each token is mapped with a "SYMP" (Symptom) tag or "O" (Other). 
Then I used StanfordNLP Ner module to build a CRF model using the created dataset. Used standard features as shown "medical_er.prop".
Training the model was done following info in [Stanford NER CRF FAQ](http://nlp.stanford.edu/software/crf-faq.shtml#a)

Trained two models 1 ignoring all treatment tags, 2 with treatment tags. Then I used the model the predict the symptom entities in a list of NHS pages.

### Content:
- convert_to_tsv.py:
This script is responsible for changing the dataset format from [website](http://biotext.berkeley.edu/data/dis_treat_data.html) into the tsv format which can be used to train a model using Stanford NER.
- html_reader.py
This class can be used to extract the meaningful text out of the NHS pages, using BeautifulSoup. It has some hardcoded div/classnames only relevant to NHS pages, in order to capture main content.
- find_entities.py
This script is used to print out the entities in a webpage by passing the page URL. It can be also used with a json file conaining a list of URLs "urls.json" so it prints out all the entities found in those pages.
It assumes by default that stanford-ner.jar is in "stanford-ner/" directory. And the model "medical-er-model.ser2.gz" is in "model/" directory. Otherwise they can be provided by command line arguments to the script, can run ```./find_entities.py -h``` to get help info.
- urls.json
This json file contains a URL list of NHS symptom pages.
- sample_output.txt
This file contains a sample output of the find_entities.py script when run against urls in urls.json
- ear_glue.tsv
a tsv file contains the tokens from one of the URLs in the urls.json where the tokens were manually tagged from symptoms so the file can be then used as a test dataset to evaluate the model.

### Evaluation
I tested the model with a manually tagged example "ear_glue.tsv", both models didn't perform well. The F score for model 2 was better at 0.2857, however since the test set is very small due to lack of tagged data, this evaluation is not very representative, but rather for demo purposes only.

The reason why the performance is low can be due to few main factors:
1. The training data does not specify symptoms only, but a mix of disease and treatment info.
2. The training data is relatively small
3. The test data (from the NHS pages) is formatted differently than the training data, it has most symptoms listed as stand alone entries so the contextual features lose their value.

- Model 1
```shell
CRFClassifier tagged 222 words in 1 documents at 3171.43 words per second.
         Entity	P	    R	    F1	    TP	FP	FN
           SYMP	1.0000	0.0833	0.1538	1	0	11
         Totals	1.0000	0.0833	0.1538	1	0	11
```

- Model 2
```shell
CRFClassifier tagged 222 words in 1 documents at 3217.39 words per second.
	     Entity	P	    R	    F1	    TP	FP	FN
	       SYMP	1.0000	0.1667	0.2857	2	0	10
	     Totals	1.0000	0.1667	0.2857	2	0	10
```

### Improvements
Future improvements can include adding larger datasets for training, or making some adjustments to the features and making the test data have a closer format to the training data.
Also trying possible alternative to CRF such as Word2Vec or with enough data (not annotated) and great computing power, CNN can be also used.

### Versions used:
- Python 2.7.10
- nltk 3.0.1.
- Stanford NER - v3.6.0