import os
import pickle


def get_name_pickle():
    result = {}
    for filename in os.listdir('model'):
        if "tag" not in filename:
            continue
        with open("model/" + filename, 'rb') as handle:
            params = pickle.load(handle)
        item = list(params.items())
        item.sort(key=lambda x: x[1], reverse=True)
        result[filename.replace('model_', '')] = item.copy()
    return result


def get_all_words_pickle():
    result = {}
    for filename in os.listdir('model'):
        if "tag" in filename:
            continue
        with open("model/" + filename, 'rb') as handle:
            params = pickle.load(handle)
        item = list(params.items())
        item.sort(key=lambda x: x[1], reverse=True)
        result[filename.replace('model_', '')] = item.copy()
    return result
