import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

import numpy
import tflearn
from tensorflow.python.framework import ops
import random
import json
import pickle

with open("Data\\ChatBot_Data\\Data\\intents.JSON") as file:
    data = json.load(file)

try:
    with open("Data\\ChatBot_Data\\Model\\data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data['intents']:
        for pattern in intent['patterns']:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent['tag'])
            
            if intent['tag'] not in labels:
                labels.append(intent['tag'])

    words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        
        bag=[]
        wrds = [stemmer.stem(w) for w in doc]
        
        for w in words:
            
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        
        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)
    
    with open("Data\\ChatBot_Data\\Model\\data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

ops.reset_default_graph()

# creating a neural network
# defining an input shape for the model
net = tflearn.input_data(shape=[None, len(training[0])])
# adding this fully connected layer to the neural network and it will have 8 neurons for the hidden layer
net = tflearn.fully_connected(net, int(((len(training[0])+len(output[0]))*2)/3))
print(int(((len(training[0])+len(output[0]))*2)/3))
net = tflearn.fully_connected(net, int(((len(training[0])+len(output[0]))*2)/3))
# this allow us to get probabilities for each output 
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)
# type of neural network DNN
model = tflearn.DNN(net)

try:
    model.load("Data\\ChatBot_Data\\Model\\model.tflearn")
except:
# epoch is the number of times the model will see the data
    model.fit(training,output,n_epoch=1000, batch_size=8, show_metric=True)
    model.save("Data\\ChatBot_Data\\Model\\model.tflearn")
# model.fit(training,output,n_epoch=1000, batch_size=8, show_metric=False)
# model.save("Data\\ChatBot_Data\\Model\\model.tflearn")

def bag_of_words(s, words):
    
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)

def chat(command):
    
    result = model.predict([bag_of_words(command, words)])
    result_index = numpy.argmax(result)
    tag = labels[result_index]
    
    for tg in data['intents']:
        if tg['tag'] == tag:
            responses = tg['responses']
            context = tg["context"][0]
            
    response=random.choice(responses)
    
    bot_response = [response,context]
    
    return bot_response