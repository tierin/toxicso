import json
import os
import pickle
import re
import string


def tokenize(s):
    re_tok = re.compile('([{}“”¨«»®´·º½¾¿¡§£₤‘’])'.format(string.punctuation))
    return re_tok.sub(r' \1 ', s).split()


def load_models():
    models = {}
    for file in os.listdir('models'):
        with open(os.path.join('models', file), 'rb') as m, \
                open(os.path.join('ratio', file.replace('model', 'r')), 'rb') as r:
            models[file] = {'model': pickle.load(m), 'ratio': pickle.load(r)}
    return models


def evaluate_toxicity(body, vec):

    text = vec.transform([body])
    pred_sum = 0
    for one_model in models:
        model = models[one_model]['model']
        ratio = models[one_model]['ratio']
        predict = model.predict_proba(text.multiply(ratio))[:, 1]
        pred_sum += float(predict[0])
    return pred_sum


def evaluate_posts():
    file_dir = os.listdir('comments2018')
    num = 1
    index = 1
    with open('data/vectoriser.pkl', 'rb') as vec:
        vec = pickle.load(vec)
    so_results = []
    for file in file_dir:
        with open(os.path.join('comments2018', file), 'r') as f:
            so_dict = json.load(f)
            for post in so_dict:
                post['Toxicity'] = evaluate_toxicity(post['Body'], vec)
                if post['Toxicity'] > 0.5:
                    so_results.append(post)
                    num += 1
                if num % 1000 == 0:
                    with open('results/so_results_com_2018_{}.json'.format(index), 'w') as f:
                        json.dump(so_results, f)
                        so_results = []
                        print('file {}'.format(index))
                        index += 1

    with open('results/so_results_com_2018_{}.json'.format(index+1), 'w') as f:
        json.dump(so_results, f)


if __name__ == "__main__":
    print('start')
    models = load_models()
    print('load models')
    evaluate_posts()
