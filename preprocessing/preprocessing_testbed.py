# with open ('../../5.eml', 'r', encoding = "ISO-8859-1") as email:
#     data = email.read()
#     print(data)
from EmailData import EmailData
import re
from utils import clean_up_raw_body

import mailparser
mail = mailparser.parse_from_file('../../5.eml')
# print(mail.subject)
# print(mail.attachments)
# print(mail.from_)
# print(mail.body)


# a = mail.body
# a = ' '.join([line.strip() for line in a.strip().splitlines() if line.strip()])
test_mail_item = EmailData(mail.subject, mail.from_, mail.attachments, clean_up_raw_body(mail.body))

# print(a)
# b = re.findall(r'https:', a)
test_mail_item.generate_features()
print(test_mail_item.get_feature_https_token())
