import os
import mailparser


import pandas as pd

urlList = [".com", ".in", ".org"]
mathSymList = "+-/*%^."


def randomForest():
    from sklearn.ensemble import RandomForestClassifier
    dataset = pd.read_csv('dataset.csv', encoding = "ISO-8859-1")
    dataset.columns = ['X1','X2','X3','X4','Y']
    dataset.head()

    from sklearn.model_selection import train_test_split
    forest = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=123456)
    X = dataset.values[:, 0:4]
    Y = dataset.values[:, 4]
    trainX, testX, trainY, testY = train_test_split(X, Y, test_size=0.3)
    #Training
    forest.fit(trainX, trainY)
    print('Accuracy: \n', forest.score(testX, testY))
    #Prediction
    pred = forest.predict(testX)

    #Test a random email
    mail = mailparser.parse_from_file(r'C:\Users\ahmad\PycharmProjects\randomForest\phish_2.eml')

    if len(mail.attachments) <= 0:
        attachments = 1
    else:
        attachments = -1

    testemail = [checkSubject(mail.subject), checkSubject(mail.from_), attachments, checkSubject(mail.body)]
    print(testemail)
    result = forest.predict([testemail])
    print(result)

    #test another random email
    mail = mailparser.parse_from_file(r'C:\Users\ahmad\PycharmProjects\randomForest\real_1.eml')

    if len(mail.attachments) <= 0:
        attachments = 1
    else:
        attachments = -1

    testemail = [checkSubject(mail.subject), checkSubject(mail.from_), attachments, checkSubject(mail.body)]
    print(testemail)
    result = forest.predict([testemail])

    print(result)


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
