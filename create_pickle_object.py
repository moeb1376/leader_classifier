import pickle
from hazm import *
import os

root = os.getcwd()
data_root = os.path.join(root, "data_class_base")
print(data_root)
print(os.listdir(data_root))
president_data = {}
for president in os.listdir(data_root):
    president_data[president] = os.listdir(os.path.join(data_root, president))
print(president_data)
tagger = POSTagger(model='resources/postagger.model')
for president in president_data:
    file_name = os.path.join(data_root, president) + "/%s"
    data = president_data[president]
    stop_tag = ["NUM","P","PUNC",'CONJ','DET','POSTP']
    word_dict = {}
    tag_word_dict = {}
    for fileN in data:
        with open(file_name % fileN, 'r') as f:
            for line in f:
                normalizer = Normalizer()
                normal_line = normalizer.normalize(line)
                words = word_tokenize(normal_line)
                tag_words = tagger.tag(words)
                for word in tag_words:
                    if word[1] not in stop_tag:
                        word_dict[word[0]] = word_dict.get(word[0], 0) + 1
                    if word[1] == "N":
                        tag_word_dict[word[0]] = tag_word_dict.get(word[0], 0) + 1

    print("pickle object save")
    with open('model/model_' + president, 'wb') as handle:
        pickle.dump(word_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('model/tag_model_' + president, 'wb') as handle:
        pickle.dump(tag_word_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
