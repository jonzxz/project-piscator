# with open ('../../5.eml', 'r', encoding = "ISO-8859-1") as email:
#     data = email.read()
#     print(data)
from EmailData import EmailData
import re


import mailparser

# for i in range(0, 10, 1):
#     mail = mailparser.parse_from_file('../../PhishingCorpus_Jose_Nazario/public_phishing/phishing0/{}.eml'.format(i))
#     # print(mail.subject)
#     # print(mail.attachments)
#     # print(mail.from_)
#     # print(mail.body)
#
#
#     # a = mail.body
#     # a = ' '.join([line.strip() for line in a.strip().splitlines() if line.strip()])
#     test_mail_item = EmailData(mail.subject, mail.from_, mail.attachments, mail.body)
#
#     # print(a)
#     # b = re.findall(r'https:', a)
#     test_mail_item.generate_features()
#
#     print(test_mail_item.get_domain())
#     print(test_mail_item.get_feature_domain_age())



mail = mailparser.parse_from_file('../../{}.eml'.format(5))
test_mail_item = EmailData(mail.subject, mail.from_, mail.attachments, mail.body)
test_mail_item.generate_features()

print(test_mail_item.get_feature_domain_age())

# print(test_mail_item.get_domain()[0])
# cont = (test_mail_item.get_content())
# b = re.findall(r'^(http://|www|https://).*', cont)
# print(b)
#

# a = test_mail_item.get_content()
# print(test_mail_item.get_domain())
# print(test_mail_item.get_feature_domain_age())
# # b = re.findall('((http://www.|https://www.|http://|www.|https://).+?(?=\/))', a)
# c = set(['.'.join((b[0]).split(sep='.')[-2:]) for b in re.findall('((http://www.|https://www.|http://|www.|https://).+?(?=\/))', a)])
#


# main_domain = ['.'.join(dom.split(sep='.')[-2:]) for dom in test_mail_item.get_domain()]
# domains_in_mail = set(['.'.join((b[0]).split(sep='.')[-2:]) for b in \
# re.findall('((http://www.|https://www.|http://|www.|https://).+?(?=\/))' \
# , test_mail_item.get_content())])
#
# main_domain = ['ebay.com', 'ebay.coma']
# domains_in_mail = ['1ebay.com', '2ebay.com']
# for domain in domains_in_mail:
#         if len(main_domain) == 1:
#                 if main_domain[0] not in domain:
#                         print('toh')
#         else:
#                 for main_d in main_domain:
#                         print("Comparing {} against {}".format(main_d, domain))
#                         if main_d not in domain:
#                                 print('tohhhh')
