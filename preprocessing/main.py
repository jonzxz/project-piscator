import os
from utils import format_all_mails
# Mail Utils
import mailparser
from EmailData import EmailData

# ML Utils
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib

def train_model() -> RandomForestClassifier:
    dataset = pd.read_csv('dsv4.csv', encoding = "ISO-8859-1")
    # dataset = pd.read_csv('train.csv', encoding = "ISO-8859-1")
    dataset.columns = ['X1','X2','X3','X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10', 'X11', 'X12','Y']
    dataset.head()

    forest = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=123456)
    X = dataset.values[:, 0:12]
    Y = dataset.values[:, 12]
    trainX, testX, trainY, testY = train_test_split(X, Y, test_size=0.3)
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

def test_model(model: RandomForestClassifier, test_data_dir: str):
    count = 0
    phish = 0
    for i in range(1, 133):
        try:
            mail = mailparser.parse_from_file(r'{}{}.eml'.format(test_data_dir, i))
            if 'ARC-Authentication-Results' in mail.headers or 'Authentication-Results' in mail.headers:
                try:
                    headers = mail.headers['ARC-Authentication-Results']
                except KeyError:
                    headers = mail.headers['Authentication-Results']
            else:
                headers = None
            test_mail = EmailData(mail.subject, mail.from_, mail.attachments, mail.body, headers)
            test_mail.generate_features()
            result = model.predict(test_mail.repr_in_arr())
            count+=1
            # change to -1 if testing for non phish
            if result == 1:
                phish+=1
            print("Mail {} -- Result: {}".format(i, result))
        except FileNotFoundError:
            pass

    print("Detected Mails: {} -- Total Mails: {}".format(phish, count))
    print("Accuracy: {}".format((phish/count)*100))

def test_model_single(model: RandomForestClassifier, file_path: str):
    mail = mailparser.parse_from_file(r'{}'.format(file_path))
    if 'ARC-Authentication-Results' in mail.headers or 'Authentication-Results' in mail.headers:
        try:
            headers = mail.headers['ARC-Authentication-Results']
        except KeyError:
            headers = mail.headers['Authentication-Results']
    else:
        headers = None
    test_mail = EmailData(mail.subject, mail.from_, mail.attachments, mail.body, headers)
    test_mail = EmailData(mail.subject, mail.from_, mail.attachments, mail.body, headers)
    test_mail.generate_features()
    result = model.predict(test_mail.repr_in_arr())
    print("Result: {}".format(result))

def test_model_modern_phish(model, test_data_dir, start, end):
    count = 0
    phish = 0
    for i in range(start, end+1):
        try:
            mail = mailparser.parse_from_file(r'{}{}.eml'.format(test_data_dir, i))
            if 'ARC-Authentication-Results' in mail.headers or 'Authentication-Results' in mail.headers:
                try:
                    headers = mail.headers['ARC-Authentication-Results']
                except KeyError:
                    headers = mail.headers['Authentication-Results']
            else:
                headers = None
            test_mail = EmailData(mail.subject, mail.from_, mail.attachments, mail.body, headers)
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
            if 'ARC-Authentication-Results' in mail.headers or 'Authentication-Results' in mail.headers:
                try:
                    headers = mail.headers['ARC-Authentication-Results']
                except KeyError:
                    headers = mail.headers['Authentication-Results']
            else:
                headers = None
            test_mail = EmailData(mail.subject, mail.from_, mail.attachments, mail.body, headers)
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
            if 'ARC-Authentication-Results' in mail.headers or 'Authentication-Results' in mail.headers:
                try:
                    headers = mail.headers['ARC-Authentication-Results']
                except KeyError:
                    headers = mail.headers['Authentication-Results']
            else:
                headers = None
            test_mail = EmailData(mail.subject, mail.from_, mail.attachments, mail.body, headers)
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
            if 'ARC-Authentication-Results' in mail.headers or 'Authentication-Results' in mail.headers:
                try:
                    headers = mail.headers['ARC-Authentication-Results']
                except KeyError:
                    headers = mail.headers['Authentication-Results']
            else:
                headers = None
            test_mail = EmailData(mail.subject, mail.from_, mail.attachments, mail.body, headers)
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
    MODERN_HAM_PATH = '../../Mailboxes/Yannis_Mailbox/'
    MODERN_PHISH_PATH = '../../Mailboxes/IndividualTestMails/Phish/'
    OLDEN_HAM_PATH = '../../Mailboxes/enron_mail_20150507/maildir/badeer-r/all_documents/'
    OLDEN_PHISH_PATH = '../../Mailboxes/PhishingCorpus_Jose_Nazario/public_phishing/phishing3/'
    SINGLE_TEST_FILE = '../../Mailboxes/IndividualTestMails/Ham/ham_1.eml'
    model = train_model()
    # test_model_olden_phish(model, OLDEN_PHISH_PATH, 1301, 1601)
    # test_model_olden_ham(model, OLDEN_HAM_PATH, 1, 300)
    # test_model(model, '../../Mailboxes/Yannis_Mailbox/', 1, 134)
    test_model_modern_phish(model, MODERN_PHISH_PATH, 31, 46)
    # test_model_modern_ham(model, MODERN_HAM_PATH, 1, 134)
    # test_model_single(model, SINGLE_TEST_FILE)
    # serialize_model(model)

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
