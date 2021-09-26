
# Sentiment analysis is a technique that detects the underlying sentiment in a piece of text.
# It is the process of classifying text as either positive, negative, or neutral. Machine learning techniques are used to evaluate a 
# piece of text and determine the sentiment behind it.


from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from statistics import mean
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
import nltk
import time
import pickle as cPickle

import collections

from nltk.sentiment import SentimentIntensityAnalyzer

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import  matplotlib.pyplot as plt

from textstat.textstat import textstatistics,legacy_round

from random import shuffle
import pdb

import sys

import excel_helper_functions as ehf


# To do list:
# > Get all occurrences of a word, so clicking on it will highlight all
# 

def text_classification20():

    twenty_train = fetch_20newsgroups(subset='train', shuffle=True)
    twenty_test = fetch_20newsgroups(subset='test', shuffle=True)

    # prints all the categories
    for cat in (twenty_train.target_names):
        # print(cat)
        pass

    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(twenty_train.data)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    print(X_train_tfidf.shape)

    # print(twenty_train.target_names[twenty_train.target[0]])

    text_clf_svm = Pipeline([('vect', CountVectorizer(stop_words='english')),
                             ('tfidf', TfidfTransformer()),
                             ('clf', MultinomialNB()),
                             ])
    _ = text_clf_svm.fit(twenty_train.data, twenty_train.target)
    # predicted_svm = text_clf_svm.predict(twenty_test.data)

    
    # save the classifier
    with open('./my_dumped_classifier.pkl', 'wb') as fid:
        cPickle.dump(text_clf_svm, fid)

    text = [
        r"he rule of six inside private homes will be removed and work-from-home guidance abolished as 16 months of on-off restrictions on daily life end.The PM said he expected the final step would go ahead as planned on 19 July. This will be confirmed on 12 July after a review of the latest data. Further updates on school bubbles, travel and self-isolation will follow in the coming days, Mr Johnson told a Downing Street news conference. He said that even after the removal of the legal requirement to wear a face covering, he would continue to wear one himself in crowded places as a courtesy."]

    predicted_svm = text_clf_svm.predict(text)
    print(twenty_train.target_names[predicted_svm[0]])
    # print(np.mean(predicted_svm == twenty_test.target))

# .......................................
def predict_likely_topic(text):
    likely_topic = 'none predicted'
    twenty_train_topics = ['Atheism', 'computer-related topics', 'computer-related topics',
                           'computer-related topics',
                           'computer-related topics', 'computer-related topics ', 'Entertainment', 'recreational activities/ autos',
                           'recreational activities/Entertainment', 'recreational activities/Entertainment/sport', 'Recreational activities/Entertainment',
                           'Science/Computers',
                           'Science', 'Medical', 'Science/ space', 'Social',
                           'Talk/ politics', 'Talk/ Politics', 'Talk/Politics', 'Talk/ religion.Miscellaneous']


    # load it again
    with open('./my_dumped_classifier.pkl', 'rb') as fid:
        text_clf_svm = cPickle.load(fid)

        predicted_svm = text_clf_svm.predict([text])
        print(twenty_train_topics[predicted_svm[0]])
        likely_topic = twenty_train_topics[predicted_svm[0]]

    return likely_topic

def FleschReadabilityEase(text):

    """"
    90-100 -> easily understood by an average 11-year old
    60-70 -> easily understood by 13-15-year-old students
    0-30 -> best understood by university graduates
    """

    words = len(text.split())
    if (words) > 0 and (words) < 4:
        return 95
    if len(text) > 0:
        return 206.835 - (1.015 * len(text.split()) / len(text.split('.')) ) - 84.6 * (sum(list(map(lambda x: 1 if x in ["a","i","e","o","u","y","A","E","I","O","U","y"] else 0,text))) / len(text.split()))



def convert_Flesch_percentage(score):

    return (100 -score)



# ...................................

def word_frequency(text):
    freq_data = []
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    # text_words = word_tokenize(text)
    # text_words = word_tokenize(text)
    text_words = []
    text_words = tokenizer.tokenize(text)
    
    stop_words = set(stopwords.words('english'))
    text_words = [w for w in text_words if not w.lower() in stop_words]

    data_analysis = nltk.FreqDist(text_words)
    # Let's take the specific words only if their frequency is greater than 3.
    filter_words = dict([(m, n) for m, n in data_analysis.items() if len(m) > 0])
    for key in sorted(filter_words):
        print("%s: %s" % (key, filter_words[key]))

    data_analysis = nltk.FreqDist(filter_words)

    new_dict = {}
    for k,v in data_analysis.items():
        new_dict[k] = v

    sorted_dict = dict(sorted(new_dict.items(), key=lambda item: item[1], reverse=True))

    

    return sorted_dict, len(text_words)
    
# ..................................

def generate_word_cloud(text):

    wordcloud = WordCloud(background_color="white").generate(text)

    ts = str(time.time())
    word_cloud_url = 'word_cloud' + ts + '.png'
    word_cloud_url = 'word_cloud' + '.png'

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    plt.savefig(f'./media/{word_cloud_url}')
    # plt.show()

    plt.close()
    return word_cloud_url

# ..................................

def convert_to_data_array(freq_dict):
    data_array = []

    for k,v in freq_dict.items():
        data_obj = {}
        data_obj['word'] = k
        data_obj['count'] = v
        data_array.append(data_obj)

    return data_array


# .................................



# ...................................

def sentiment_analysis():


    return


if __name__ == "__main__":
    text ="A frequency distribution records the number of times each outcome of an experiment has occurred. For example, a frequency distribution could be used to record the frequency of each word type in a document. Formally, a frequency distribution can be defined as a function mapping from each sample to the number of times that sample occurred as an outcome.Frequency distributions are generally constructed by running a number of experiments, and incrementing the count for a sample every time it is an outcome of an experiment."

    
    d, wc = word_frequency(text)
    f = convert_to_data_array(d)
    # generate_word_cloud(text)
    print(f)
    print(wc)
    print('...')
    score = (FleschReadabilityEase(text))
    pc = convert_Flesch_percentage(score)
    print(pc)
    print(d)

    text_classification20()
    predict_likely_topic(text)