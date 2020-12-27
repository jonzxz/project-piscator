# with open ('../../5.eml', 'r', encoding = "ISO-8859-1") as email:
#     data = email.read()
#     print(data)
from EmailData import EmailData
import re


import mailparser

for i in range(1, 30):
    try:
        # mail = mailparser.parse_from_file('../../Mailboxes/PhishingCorpus_Jose_Nazario/public_phishing/phishing3/{}.eml'.format(i))
        # mail = mailparser.parse_from_file('../../Mailboxes/PhishingCorpus_Jose_Nazario/public_phishing/phishing3/{}.eml'.format(i))
        # mail = mailparser.parse_from_file('../../Mailboxes/Isaac_Mailbox/{}.eml'.format(i))
        # mail = mailparser.parse_from_file('../../Mailboxes/IndividualTestMails/Phish/{}.eml'.format(i))
        # mail = mailparser.parse_from_file('../../Mailboxes/enron_mail_20150507/maildir/allen-p/all_documents/{}..eml'.format(i))
        # mail = mailparser.parse_from_file('../../Mailboxes/enron_mail_20150507/maildir/arnold-j/all_documents/{}..eml'.format(i))


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
        print("{}".format(test_mail_item))
    except FileNotFoundError:
        pass
