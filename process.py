from collections import defaultdict
import openai
import csv
from main import remove_quotes
import random


def getCommonalities(index_dict):
    openai.api_key = "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"

    # read text file and store sentences in the list
    with open('RandomSents.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        sentences = [remove_quotes(row[0]) for row in reader]
    # dictionary to store the corresponding sentences for each key
    sentence_dict = defaultdict(list)

    # populate sentence_dict with sentences for each key
    for key in index_dict:
        for index in index_dict[key]:
            sentence_dict[key].append(sentences[index])

    # dictionary to store GPT-3 responses for each key
    gpt3_dict = defaultdict(str)

    # loop through sentence_dict and prompt GPT-3 to find linguistic patterns
    # in the sentences associated with each key
    for key in sentence_dict:
        # create prompt for GPT-3
        prompt = "Please find any commonalities or linguistic patterns in the following sentences. Note that it is also okay to say there is no pattern where necessary:\n"
        sent_list = sentence_dict[key]
        if len(sent_list) > 50:
            # in the future change this to randomly pick 50 sentences - Done
            sent_list = random.sample(sent_list, k=50)
        if len(sent_list) < 2:
            continue
        for sentence in sent_list:
            prompt += "- " + sentence + "\n"
        # make request to GPT-3 API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # extract GPT-3 response
        gpt3_response = response.choices[0].text.strip()
        # add GPT-3 response to gpt3_dict with its associated key
        gpt3_dict[key] = gpt3_response

        print(f"For neuron #{key}, the GPT-3 response generated is the following:\n{gpt3_response}")
    # print the final dictionary that maps integer keys to GPT-3 responses
    return gpt3_dict


def finalProcess():
    # create a defaultdict of int keys that map to lists of ints
    index_dict = defaultdict(list)

    # iterate through each line in the input file
    with open('strIndOutput.txt', 'r') as f_in:
        for idx, line in enumerate(f_in):
            # split the line into a list of integers
            num_list = [int(num) for num in line.strip().split(',') if num.isdigit()]
            # iterate through each number in the list
            for num in num_list:
                # append the current line index to the list of values for this number key
                index_dict[num].append(idx)
    # only 65 neurons are ever activated?? - update: now 2991 (L6)
    #print(index_dict)
    '''

    # read text file and store sentences in the list
    with open('RandomSents.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        sentences = [remove_quotes(row[0]) for row in reader]
    # dictionary to store the corresponding sentences for each key
    sentence_dict = defaultdict(list)

    # populate sentence_dict with sentences for each key
    for key in index_dict:
        for index in index_dict[key]:
            sentence_dict[key].append(sentences[index])

    with open('neuronToSentence.txt', 'w') as f_out:
        for sent in sentence_dict:
            f_out.write(str(sent) + ': ' + str(sentence_dict[sent]) + '\n') '''

    return index_dict


def getIndices():
    # open the input and output text files
    with open('outAllLayers6.txt', 'r') as f_in, open('strIndOutput.txt', 'w') as f_out:
        # initialize the neuron list variable
        NeuronList = ''
        # iterate through each line in the input file
        for line in f_in:
            # check if the line starts with "(array"
            if line.startswith('Generated'):
                # append the current neuron list to the output file
                f_out.write(NeuronList + '\n')
                # set the neuron list variable to the current line parsed from index 7 till the end of the line
                NeuronList = ''
            # check if the line starts with some space characters followed by a number character
            elif line.strip().isdigit():
                # concatenate this line to the current neuron list
                if line.strip() not in NeuronList:
                    NeuronList += (line.strip() + ',')
            # ignore the line if it starts with "Index" or "Generated"
            elif line.startswith('Index'):
                continue
        # append the final neuron list to the output file
        f_out.write(NeuronList + '\n')


def removeEnds():
    with open('processedOutput.txt', 'r') as f_in, open('finalOutput.txt', 'w') as f_out:
        for line in f_in:
            f_out.write(line[:-4] + '\n')


if __name__ == "__main__":
    #getIndices()
    #removeEnds()
    #finalProcess()
    getCommonalities(finalProcess())
