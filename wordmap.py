import open_pickle


def get_all_word_frequency():
    all_words_list = open_pickle.get_all_words_pickle()
    for president in all_words_list:
        all_word = sum([i[1] for i in all_words_list[president][0:100]])
        print(president, all_word, len(all_words_list[president]))
        with open('all_words_%s.txt' % president, 'w') as f:
            temp_dict = {}
            for i in range(100):
                word, number = all_words_list[president][i]
                f.write(str(number // 100) + '\t' + word + '\n')


def get_tag_word_frequency():
    tag_words_list = open_pickle.get_name_pickle()
    for president in tag_words_list:
        with open('tag_words_%s.txt' % president, 'w') as f:
            for i in range(100):
                word, number = tag_words_list[president][i]
                f.write(str(number // 10) + ' ' + word + '\n')


def get_comparison_frequency(president1, president2):
    tag_words_list = open_pickle.get_name_pickle()
    print(tag_words_list.keys())
    dict1 = dict(tag_words_list["tag_" + president1])
    dict2 = dict(tag_words_list["tag_" + president2])
    dict1_dict2 = {}
    dict2_dict1 = {}
    for i in dict1:
        dict1_dict2[i] = dict1.get(i, 0) - dict2.get(i, 0)
    for i in dict2:
        dict2_dict1[i] = dict2.get(i, 0) - dict1.get(i, 0)
    item1 = list(dict1_dict2.items())
    item1.sort(key=lambda x: x[1], reverse=True)
    item2 = list(dict2_dict1.items())
    item2.sort(key=lambda x: x[1], reverse=True)
    with open("%sVS%s.text" % (president1, president2), 'w') as f:
        for i in range(100):
            word, number = item1[i]
            f.write(str(number) + ' ' + word + '\n')
    with open("%sVS%s.text" % (president2, president1), 'w') as f:
        for i in range(100):
            word, number = item2[i]
            f.write(str(number) + ' ' + word + '\n')


if __name__ == '__main__':
    get_comparison_frequency("Hashemi", "Khatami")
