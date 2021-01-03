from EmailData import EmailData
import re

import mailparser

for i in range(1, 57):
    try:
        # mail = mailparser.parse_from_file('../../Mailboxes/PhishingCorpus_Jose_Nazario/public_phishing/phishing3/{}.eml'.format(i))
        # mail = mailparser.parse_from_file('../../Mailboxes/PhishingCorpus_Jose_Nazario/public_phishing/phishing3/{}.eml'.format(i))
        mail = mailparser.parse_from_file('../../Mailboxes/Phish/ModernPhish2/{}.eml'.format(i))
        # mail = mailparser.parse_from_file('../../Mailboxes/Hams/Yannis_Mailbox/{}.eml'.format(i))
        # mail = mailparser.parse_from_file('../../Mailboxes/enron_mail_20150507/maildir/allen-p/all_documents/{}..eml'.format(i))
        # mail = mailparser.parse_from_file('../../Mailboxes/enron_mail_20150507/maildir/arnold-j/all_documents/{}..eml'.format(i))


        test_mail_item = EmailData( \
        mail.subject, \
        mail.from_, \
        mail.attachments, \
        mail.body, \
        mail.headers
        )
        test_mail_item.generate_features()
        print("{}".format(test_mail_item))
    except FileNotFoundError:
        pass
