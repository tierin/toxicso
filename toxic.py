# coding: utf-8

import pickle
import re
import string

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from collections import namedtuple

train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')
subm = pd.read_csv('data/sample_submission.csv')

label_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
train['none'] = 1 - train[label_cols].max(axis=1)

COMMENT = 'comment_text'
train[COMMENT].fillna("unknown", inplace=True)
test[COMMENT].fillna("unknown", inplace=True)


def tokenize(s):
    re_tok = re.compile('([{}“”¨«»®´·º½¾¿¡§£₤‘’])'.format(string.punctuation))
    return re_tok.sub(r' \1 ', s).split()


n = train.shape[0]
vec = TfidfVectorizer(ngram_range=(1, 2), tokenizer=tokenize,
                      min_df=3, max_df=0.9, strip_accents='unicode', use_idf=1,
                      smooth_idf=1, sublinear_tf=1)

trn_term_doc = vec.fit_transform(train[COMMENT])

test_term_doc = vec.transform(test[COMMENT])

vec_filename = 'models/vectorizer.pkl'

with open(vec_filename, 'wb') as vec_file:
    pickle.dump(vec, vec_file)


def pr(y_i, y):
    p = x[y == y_i].sum(0)
    return (p + 1) / ((y == y_i).sum() + 1)


x = trn_term_doc

test_x = test_term_doc


def get_mdl(y):
    y = y.values
    r = np.log(pr(1, y) / pr(0, y))
    m = LogisticRegression(C=4, dual=True)
    x_nb = x.multiply(r)
    return m.fit(x_nb, y), r


preds = np.zeros((len(test), len(label_cols)))

Models = namedtuple('models', 'model ratio')


def save_models():
    for i, j in enumerate(label_cols):
        print('fit', j)
        m, r = get_mdl(train[j])
        preds[:, i] = m.predict_proba(test_x.multiply(r))[:, 1]
        model = Models(model=m, ratio=r)
        model_filename = f'models/{j}_model.pkl'
        with open(model_filename, 'wb') as m_file:
            pickle.dump(model, m_file)


save_models()
