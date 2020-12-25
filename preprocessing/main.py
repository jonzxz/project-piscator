import os

# Mail Utils
import mailparser
from EmailData import EmailData

# ML Utils
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib

def train_model() -> RandomForestClassifier:
    dataset = pd.read_csv('train.csv', encoding = "ISO-8859-1")
    dataset.columns = ['X1','X2','X3','X4', 'X5', 'X6', 'X7', 'X8', 'X9','Y']
    dataset.head()

    forest = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=123456)
    X = dataset.values[:, 0:9]
    Y = dataset.values[:, 9]
    trainX, testX, trainY, testY = train_test_split(X, Y, test_size=0.3)
    #Training
    forest.fit(trainX, trainY)
    print('Accuracy: \n', forest.score(testX, testY))
    #Prediction
    pred = forest.predict(testX)

    return forest

def serialize_model(model):
    joblib.dump(model, 'PhishingForest')

def load_model() -> RandomForestClassifier:
    return joblib.load('PhishingForest')

def test_model(model: RandomForestClassifier):
    count = 0
    phish = 0
    for i in range(1, 50):
        try:
            # mail = mailparser.parse_from_file(r'../../PhishingCorpus_Jose_Nazario/public_phishing/phishing3/{}.eml'.format(i))
            mail = mailparser.parse_from_file(r'../../enron_mail_20150507/maildir/arora-h/all_documents/{}..eml'.format(i))
            test_mail = EmailData(mail.subject, mail.from_, mail.attachments, mail.body)
            test_mail.generate_features()
            # print(test_mail)
            result = model.predict(test_mail.repr_in_arr())
            count+=1
            # change to -1 if testing for non phish
            if result == 1:
                phish+=1
            print("Mail {} -- Result: {}".format(i, result))
        except FileNotFoundError:
            pass

    print("Accuracy: {}".format((phish/count)*100))

def main():
    model = train_model()
    # test_model(model)
    serialize_model(model)

main()
