from log_message_adaptation import adapt_log_message

from os import walk
from os.path import isfile, join
import mimetypes

import random

# copy log messages into new variable before adapting them
def adapt_log_messages(log_messages):
    adapted_messages = []
    for message in log_messages:
        message = adapt_log_message(message)
        adapted_messages.append(message)
    return adapted_messages

def load_log_file(file, index):
    with open(file) as f:
        logFile = f.readlines()
    label = [index] * len(logFile)
    return logFile, label

def shuffle_log_data(logData, label):
    data = list(zip(logData, label))
    random.shuffle(data)
    logData, label = zip(*data)
    
    return logData, label

def load_files_in_dir(directory): 
    files = []
    for (dirpath, dirnames, filenames) in walk(directory):
        for filename in filenames:
            if mimetypes.guess_type(filename)[0] == 'text/plain':
                files.append(join(dirpath, filename))
    return files
    
def load_log_files(directory):
    dirFiles = load_files_in_dir(directory)
    all_logs = []
    all_labels = []
    i = 0
    k = 0
    for file in dirFiles:
        logData, label = load_log_file(file, k)
        adapted_log_messages = adapt_log_messages(logData)
        all_logs.extend(adapted_log_messages)
        all_labels.extend(label)
        i += 1
        # 3 represenrs the raw files labelled 1-3
        if i % 3 == 0:
            k +=1
    
    logData, label = shuffle_log_data(all_logs, all_labels)
    return logData, label

def save_log_file_label(path, log_data, labels):
    if log_data:
        with open(path + "logs.txt", "w") as text:
            for log in log_data:
                if "\n" in log:
                    text.write(log)
                else:
                    text.write(log + '\n')
    
    if labels:
        with open(path + "labels.txt", "w") as text_file:
            for label in labels:
                text_file.write(str(label) + '\n')
                
def read_logs_and_labels(log_file, label_file):
    with open(log_file) as f:
        logFile = f.readlines()
    
    with open(label_file) as f:
        labelFile = f.readlines()
        
    return logFile, labelFile