import os
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import accuracy_score



#making dictionary for the dataset
def make_dict():
    path = "emails/"
    files = os.listdir(path)

    emails = [path + email for email in files]

    words = []
    length = len(emails)

    for email in emails:
        f = open(email)
        blob = f.read()
        words += blob.split(" ") # we are splitting the individual words form the sentence.
        length = length - 1

    for i in range(len(words)):
        if not words[i].isalpha():
            words[i] = ""

    dictionary = Counter(words)
    del dictionary[""]  # we are deleting alphanumeric words which are noise and decreases the accuracy
    return dictionary.most_common(3000)


#converting the dictionary into a feature vector
def make_dataset(dictionary):
    direc = "emails/"
    files = os.listdir(direc)

    emails = [direc + email for email in files]

    feature_set = []
    labels = []
    length =len(emails)

    for email in emails:
        data = []
        f =open(email)
        words = f.read().split(' ')
        for entry in dictionary:
            data.append(words.count(entry[0]))
        feature_set.append(data)
        if "ham" in email:  #if we have word 'ham' in email then it is labeled as 0
            labels.append(0)
        if "spam" in email: #if we have word 'ham' in email then it is labeled as 1
            labels.append(1)
        print length
        length = length - 1
    return feature_set, labels
d = make_dict()

features, labels = make_dataset(d)



x_train, x_test, y_train, y_test = tts(features, labels, test_size=0.2)
clf = MultinomialNB()
clf.fit(x_train, y_train)
prediction = clf.predict(x_test)
print "accuracy is ",accuracy_score(y_test, prediction) #accuracy for NB Classifier

while True:
    features = []
    inp = raw_input(">").split()
    if inp[0] == "exit":
        break
    for word in d:
        features.append(inp.count(word[0]))
    res = clf.predict([features])
    print ["Ham", "Spam!"][res[0]]


