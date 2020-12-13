# with open ('../../5.eml', 'r', encoding = "ISO-8859-1") as email:
#     data = email.read()
#     print(data)

import mailparser
mail = mailparser.parse_from_file('../../5.eml')
print(mail.subject)
