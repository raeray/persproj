from nltk.corpus import wordnet
import nltk
import gensim
from gensim.utils import simple_preprocess
from gensim import corpora, models
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np

# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')

class ldaModel(object):
    '''
    example: 
    filter_params = {
    'no_below': 1,
    'no_above':0.2,
    'keep_n': 10000
    }

    model_params = {
        'num_topics': 10,
        'passes':2,
        'workers': 4
    }

    lda_class = lda.ldaModel(dim_sum_df,
                'text',
                filter_params,
                model_params)
    '''

    def __init__(self, review_df, review_text_field, filter_params):
        self.review_df = review_df
        self.filter_params = filter_params
        self.bow_corpus = None
        self.processed_docs = self.run_preprocess(review_df[review_text_field])
        self.dictionary = self.get_dictionary()

    def get_wordnet_pos(self, word):
        """Map POS tag to first character lemmatize() accepts"""
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

        return tag_dict.get(tag, wordnet.NOUN)


    def lemmatize(self, text):
        lemmatizer = WordNetLemmatizer()
        return lemmatizer.lemmatize(text, pos=self.get_wordnet_pos(text))


    def stem(self, text):
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
        return stemmer.stem(text)


    def preprocess(self, text):
        result = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
                result.append(self.stem(self.lemmatize(token)))

        return result
    
    def run_preprocess(self, review_series):

        processed_docs = review_series.map(self.preprocess)
        return processed_docs

    def get_dictionary(self):

        dictionary = corpora.Dictionary(self.processed_docs)
        print('original dict len: ', len(dictionary))

        # filter extreme values from dictionary
        dictionary.filter_extremes(
            **self.filter_params
            )
        print('after filter dict len: ', len(dictionary))
        return dictionary

    def run_model(self, **model_params):

        self.bow_corpus = [self.dictionary.doc2bow(doc) for doc in self.processed_docs]
        # if lda model based on bag of words 
        lda_model = gensim.models.LdaMulticore(self.bow_corpus,
                                            **model_params
                                            )

        return lda_model
