#!/usr/bin/env python3

import nltk
nltk.download('averaged_perceptron_tagger')


TYPICAL = ['.', 'is', 'and', 'a', 'to', 'the', 'i', 'of', 'on', 'at', 'was', ]
SCI_TYP = ['scien', 'tech', 'research']
SCI_NEU = [321, 1105, 1486, 1595, 1978, 2166, 2138, 2384, 2466, 2640, 2682, 2991]


def find_pattern(sentences):
    """
    Given a list of sentences, finds a pattern about linguistic features in NLP.
    """
    # Tokenize the sentences into words
    words = [nltk.word_tokenize(sentence) for sentence in sentences]

    # Tag the words with their parts of speech
    tagged_words = [nltk.pos_tag(word) for word in words]

    # Extract the most common part-of-speech tags
    pos_tags = [tag for word in tagged_words for tag in word]
    common_tags = nltk.FreqDist(pos_tags).most_common()

    # Return the most common part-of-speech tags
    return common_tags


def str_to_lst(s):
    end = s.find(']')
    s = s[1:end]
    result = list(s.split(','))
    return [int(i) for i in result]


def sort_dict(d):
    result = {k:set() for k in sorted(d.values())}
    for key in d:
        result[d[key]].add(key)
    return result




def write_on(outfile, result, counts, always_zero):
    of = open(outfile, 'w')
    of.write("FINDINGS FOR 6TH COMPONENT OF SPARSE LAYER:\n")
    of.write("Dictionary where keys are neurons and values are indices of sentences where they're activated:\n")
    for i in range(3072):
        if len(result[i]) > 0:
            cur_s = "Neuron #" + str(i) + ":  " + str(result[i]) + '\n'
            of.write(cur_s)
        else:
            cur_s = "Neuron #" + str(i) + ":  {}" + '\n'
            of.write(cur_s)
    of.write('\n\n\n\n')
    of.write("How many times it was activated / Neurons for which this is true:\n")
    of.write(str(counts))
    of.write('\n\n')
    of.write("The following neurons are never activated:\n")
    of.write(str(always_zero))
    of.close()



def func(filename):
    f = open(filename)
    fileinfo = f.readlines()
    result = {k: set() for k in range(3072)}
    for si, arr in enumerate(fileinfo):
        arr = str_to_lst(arr)  # pseudocode
        for ni in arr:
            result[ni].add(si)
    counts = {k: len(result[k]) for k in range(3072)}
    always_zero = [n for n in range(3072) if counts[n] == 0]
    counts = sort_dict(counts)
    write_on('results.txt', result, counts, always_zero)
    return result
    # print("results: \n", result)
    # print("counts: \n", sort_dict(counts))
    # print("constant zeroes: \n", always_zero)


def freq_count(d):
    sf = open('RandomSents.csv')
    sentences = sf.readlines()
    i_to_sent = {i: sent for i, sent in enumerate(sentences)}
    # d2 = {}
    for neu in SCI_NEU:
        curr_sents = [i_to_sent[i] for i in d[neu]]
        count = 0
        for sent in curr_sents:
            bool = False
            for scikey in SCI_TYP:
                if scikey in sent.lower():
                    bool = True
            if bool:
                count += 1
        print(neu, ": ", count / len(curr_sents), "....", len(curr_sents), '\n')




def commonalities2(d, filename):
    of = open(filename, 'w')
    of.write("")
    of.close()
    sf = open('RandomSents.csv')
    sentences = sf.readlines()
    i_to_sent = {i:sent for i,sent in enumerate(sentences)}
    d2 = {}
    for key in range(3072):
        curr_sents = [i_to_sent[i] for i in d[key]]
        if len(curr_sents) > 1:
            str_pattern = find_pattern(curr_sents)
            str_pattern = [s for s in str_pattern if s[1] > 1 and s[0][0][0].isalpha() and s[0][0] not in typical]
            for wpc, count in str_pattern:
                if (wpc not in d2 or d2[wpc][1] <= count) and count > 2:
                    d2[wpc] = (key, count)
    result_d = {k[0]:[] for k in sorted(d2.values())}
    for keywpc in d2:
        (neu, count) = d2[keywpc]
        s = ": This neuron captured " + keywpc[0] + "(" + keywpc[1] + ") " + str(count) + " times, the most of any neuron."
        result_d[neu].append(s)
    for k in result_d:
        of = open(filename, 'a')
        of.write('\n')
        for sent in result_d[k]:
            of.write("Neuron " + str(k) + sent + '\n')
        of.close()
    print(result_d.keys())


def commonalities(d, filename):
    of = open(filename, 'w')
    of.write("")
    of.close()
        for key in range(3072):
        curr_sents = [i_to_sent[i] for i in d[key]]
        if len(curr_sents) > 1:
            str_pattern = find_pattern(curr_sents)
            sf = open('RandomSents.csv')
            sentences = sf.readlines()
            i_to_sent = {i:sent for i,sent in enumerate(sentences)}
            of = open(filename, 'a')
            of.write('\n')
            of.write('a pattern was found for neuron #')
            of.write(str(key))
            of.write(': ')
            of.write(str(str_pattern))
            of.close()





def main():
    filename = 'finalOutput.txt'
    main_d = func(filename)
    commonalities(main_d, 'patterns.txt')
    commonalities2(main_d, 'frequent.txt')




# Python boilerplate.
if __name__ == '__main__':
    main()