import os

# Mail Utils
import mailparser
from EmailData import EmailData

# ML Utils
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split

def randomForest():
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

    count = 0
    phish = 0
    for i in range(1, 50):
        try:
            # mail = mailparser.parse_from_file(r'../../PhishingCorpus_Jose_Nazario/public_phishing/phishing3/{}.eml'.format(i))
            mail = mailparser.parse_from_file(r'../../enron_mail_20150507/maildir/arora-h/all_documents/{}..eml'.format(i))
            test_mail = EmailData(mail.subject, mail.from_, mail.attachments, mail.body)
            test_mail.generate_features()
            # print(test_mail)
            result = forest.predict(test_mail.repr_in_arr())
            count+=1
            if result == 1:
                phish+=1
            print("Mail {} -- Result: {}".format(i, result))
        except FileNotFoundError:
            pass

    print("Accuracy: {}".format((phish/count)*100))

def checkPhishingEmails():
    directory = r'C:\Users\ahmad\PycharmProjects\randomForest\phishing'
    listofPhishingEmails = []
    for filename in os.listdir(directory):
        if filename.endswith(".eml"):
            filepath = os.path.join(directory,filename)
            mail = mailparser.parse_from_file(filepath)
            listofPhishingEmails.append(mail)
        else:
            continue

    listOfEmails = []

    for i in listofPhishingEmails:
        if len(i.attachments) <= 0:
            attachments = 1
        else:
            attachments = -1

        email = [checkSubject(i.subject), checkSubject(i.from_), attachments, checkSubject(i.body), '1']
        listOfEmails.append(email)

    return listOfEmails


def checkSubject(msg):
    for i in urlList:
        if i in msg:
            return -1
    return 1

def checkFrom():
    return
def checkAttachments():
    return
def checkContent():
    return
def checkNonPhishingEmails():
    directory = r'C:\Users\ahmad\PycharmProjects\randomForest\non-phishing'
    listofNonPhishingEmails = []
    for filename in os.listdir(directory):
        if filename.endswith(".eml"):
            filepath = os.path.join(directory,filename)
            mail = mailparser.parse_from_file(filepath)
            listofNonPhishingEmails.append(mail)
        else:
            continue

    listOfEmails = []

    for i in listofNonPhishingEmails:
        if len(i.attachments) <= 0:
            attachments = 1
        else:
            attachments = -1

        email = [checkSubject(i.subject), checkSubject(i.from_), attachments, checkSubject(i.body), '0']
        listOfEmails.append(email)

    return listOfEmails


def writeToCSV(phishinglist,nonPhishingList):
    import csv
    with open('testcsv.csv', 'w', newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['subject','from','attachments','content','result'])

        for i in phishinglist:
            thewriter.writerow(i)

        for i in nonPhishingList:
            thewriter.writerow(i)



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    randomForest()
    #writeToCSV(checkPhishingEmails(),checkNonPhishingEmails())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
