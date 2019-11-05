import os
import pandas as pd
import pickle
import re, string

from sklearn.feature_extraction.text import TfidfVectorizer

text = ['fuck you, nigger', 'i think you should use sklearn instead', 'it is bullshit']

re_tok = re.compile(f'([{string.punctuation}“”¨«»®´·º½¾¿¡§£₤‘’])')


def tokenize(s): return re_tok.sub(r' \1 ', s).split()


#with open('models/vocabulary.pkl', 'rb') as vocab:
#    trn_term_doc = pickle.load(vocab)

train = pd.read_csv('train.csv')

label_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
train['none'] = 1 - train[label_cols].max(axis=1)

COMMENT = 'comment_text'
train[COMMENT].fillna("unknown", inplace=True)

vec = TfidfVectorizer(ngram_range=(1, 2), tokenizer=tokenize,
                      min_df=3, max_df=0.9, strip_accents='unicode', use_idf=1,
                      smooth_idf=1, sublinear_tf=1)
trn_term_doc = vec.fit_transform(train[COMMENT])

text = vec.transform(text)

for file in os.listdir('models'):
    with open(os.path.join('models', file), 'rb') as m, \
            open(os.path.join('r', file.replace('model', 'r')), 'rb') as r:
        model = pickle.load(m)
        r = pickle.load(r)
        predict = model.predict_proba(text.multiply(r))[:, 1]
        print(file.replace('_model.pkl', ''))
        print(predict[0])
