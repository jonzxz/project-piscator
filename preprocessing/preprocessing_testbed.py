# with open ('../../5.eml', 'r', encoding = "ISO-8859-1") as email:
#     data = email.read()
#     print(data)
from EmailData import EmailData
import re


import mailparser
# mail = mailparser.parse_from_file('../../PhishingCorpus_Jose_Nazario/public_phishing/phishing0/{}.eml'.format)
# test_mail_item = EmailData(mail.subject, mail.from_, mail.attachments, mail.body)
# test_mail_item.generate_features()
# print("Mail Num 34: -- {}".format(test_mail_item))

"""
TRAIN DATA USED SO FAR
PHISHING
phishing0
phishing1

NONPHISHING
allen-p
arnold-j
"""
for i in range(201, 438):
    try:
        mail = mailparser.parse_from_file('../../PhishingCorpus_Jose_Nazario/public_phishing/phishing1/{}.eml'.format(i))
        # mail = mailparser.parse_from_file('../../enron_mail_20150507/maildir/allen-p/all_documents/{}..eml'.format(i))
        # mail = mailparser.parse_from_file('../../enron_mail_20150507/maildir/arnold-j/all_documents/{}..eml'.format(i))
        test_mail_item = EmailData(mail.subject, mail.from_, mail.attachments, mail.body)
        test_mail_item.generate_features()
        print("{}".format(test_mail_item))
    except FileNotFoundError:
        pass
