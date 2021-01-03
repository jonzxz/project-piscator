import os
# from preprocessing.utils import format_all_mails
from utils import format_all_mails
# Mail Utils
import mailparser
# from preprocessing.EmailData import EmailData
from EmailData import EmailData

# ML Utils
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib

def train_model() -> RandomForestClassifier:
    dataset = pd.read_csv('dsv6.csv', encoding = "ISO-8859-1")
    # dataset = pd.read_csv('train.csv', encoding = "ISO-8859-1")
    dataset.columns = ['X1','X2','X3','X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10', 'X11', 'X12', 'X13', 'X14', 'X15','Y']
    dataset.head()

    forest = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=123456)
    X = dataset.values[:, 0:15]
    Y = dataset.values[:, 15]
    trainX, testX, trainY, testY = train_test_split(X, Y, train_size=0.8, test_size=0.2)
    #Training
    forest.fit(trainX, trainY)
    print('Accuracy: \n', forest.score(testX, testY))
    #Prediction
    pred = forest.predict(testX)

    return forest

def serialize_model(model: RandomForestClassifier):
    joblib.dump(model, 'PhishingForest')

def load_model() -> RandomForestClassifier:
    return joblib.load('PhishingForest')

def test_model_single(model: RandomForestClassifier, file_path: str):
    mail = mailparser.parse_from_file(r'{}'.format(file_path))
    test_mail = EmailData(mail.subject, mail.from_, mail.attachments, mail.body, mail.headers)
    test_mail.generate_features()
    result = model.predict(test_mail.repr_in_arr())
    print("Result: {}".format(result))

def test_model_modern_phish(model, test_data_dir, start, end):
    count = 0
    phish = 0
    for i in range(start, end+1):
        try:
            mail = mailparser.parse_from_file(r'{}{}.eml'.format(test_data_dir, i))
            test_mail = EmailData(mail.subject, mail.from_, mail.attachments, mail.body, mail.headers)
            test_mail.generate_features()
            result = model.predict(test_mail.repr_in_arr())
            count+=1
            if result == 1:
                phish+=1
            print("Result: {}".format(result))
        except FileNotFoundError:
            pass
    print("Detected Mails: {} -- Total Mails: {}".format(phish, count))
    print("Accuracy: {}".format((phish/count)*100))

def test_model_modern_ham(model, test_data_dir, start, end):
    count = 0
    ham = 0
    for i in range(start, end+1):
        try:
            mail = mailparser.parse_from_file(r'{}{}.eml'.format(test_data_dir, i))
            test_mail = EmailData(mail.subject, mail.from_, mail.attachments, mail.body, mail.headers)
            test_mail.generate_features()
            result = model.predict(test_mail.repr_in_arr())
            count+=1
            if result == -1:
                ham+=1
            print("Result: {}".format(result))
        except FileNotFoundError:
            pass
    print("Ham: {} -- Total Mails: {}".format(ham, count))
    print("Accuracy: {}".format((ham/count)*100))

def test_model_olden_ham(model, test_data_dir, start, end):
    count = 0
    ham = 0
    for i in range(start, end+1):
        try:
            mail = mailparser.parse_from_file(r'{}{}.eml'.format(test_data_dir, i))
            test_mail = EmailData(mail.subject, mail.from_, mail.attachments, mail.body, mail.headers)
            test_mail.generate_features()
            result = model.predict(test_mail.repr_in_arr())
            count+=1
            if result == -1:
                ham+=1
            print("Result: {}".format(result))
        except FileNotFoundError:
            pass
    print("Ham: {} -- Total Mails: {}".format(ham, count))
    print("Accuracy: {}".format((ham/count)*100))

def test_model_olden_phish(model, test_data_dir, start, end):
    count = 0
    phish = 0
    for i in range(start, end+1):
        try:
            mail = mailparser.parse_from_file(r'{}{}.eml'.format(test_data_dir, i))
            test_mail = EmailData(mail.subject, mail.from_, mail.attachments, mail.body, mail.headers)
            test_mail.generate_features()
            result = model.predict(test_mail.repr_in_arr())
            count+=1
            if result == 1:
                phish+=1
            print("Result: {}".format(result))
        except FileNotFoundError:
            pass
    print("Detected Mails: {} -- Total Mails: {}".format(phish, count))
    print("Accuracy: {}".format((phish/count)*100))

def main():
    MODERN_HAM_PATH = '../../Mailboxes/Hams/ModernHam2/'
    MODERN_PHISH_PATH = '../../Mailboxes/Phish/ModernPhish2/'
    OLDEN_HAM_PATH = '../../Mailboxes/enron_mail_20150507/maildir/badeer-r/all_documents/'
    OLDEN_PHISH_PATH = '../../Mailboxes/PhishingCorpus_Jose_Nazario/public_phishing/phishing3/'
    SINGLE_TEST_FILE = '../../Mailboxes/Hams/Jonathan_Mailbox/1.eml'
    model = train_model()
    # test_model_olden_phish(model, OLDEN_PHISH_PATH, 1301, 1601)
    # test_model_olden_ham(model, OLDEN_HAM_PATH, 1, 300)
    # test_model(model, '../../Mailboxes/Yannis_Mailbox/', 1, 134)
    # test_model_modern_phish(model, MODERN_PHISH_PATH, 1, 56)
    # test_model_modern_ham(model, MODERN_HAM_PATH, 1, 222)
    # test_model_single(model, SINGLE_TEST_FILE)
    serialize_model(model)

main()

import mailparser

def get_mail_files():
    for i in range(1, 46):
        try:
            # mail = mailparser.parse_from_file('../../Mailboxes/PhishingCorpus_Jose_Nazario/public_phishing/phishing3/{}.eml'.format(i))
            mail = mailparser.parse_from_file('../../Mailboxes/IndividualTestMails/Phish/{}.eml'.format(i))
            # mail = mailparser.parse_from_file('../../Mailboxes/IndividualTestMails/Ham/{}.eml'.format(i))
            # mail = mailparser.parse_from_file('../../Mailboxes/Jonathan_Mailbox/{}.eml'.format(i))

            if 'ARC-Authentication-Results' in mail.headers or 'Authentication-Results' in mail.headers:
                try:
                    headers = mail.headers['ARC-Authentication-Results']
                except KeyError:
                    headers = mail.headers['Authentication-Results']
            else:
                headers = None

            test_mail_item = EmailData( \
            mail.subject, \
            mail.from_, \
            mail.attachments, \
            mail.body, \
            headers
            )

            test_mail_item.generate_features()
        except FileNotFoundError:
            pass

# format_all_mails('../../Mailboxes/IndividualTestMails/Phish/ORG/', 1, 45)
