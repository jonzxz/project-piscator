import re
import joblib
from sklearn.ensemble import RandomForestClassifier

# Cleans up a messed up HTML / tabbed raw content into space delimited content
def clean_up_raw_body(raw_text):
    return ' '.join([line.strip() for line in raw_text.strip().splitlines() \
     if line.strip()])

# Flattens a list of tuples for (Sender, SenderDomain) into [Sender, SenderDomain]
# By right there SHOULD only be a single pair but kept in list just in case!
# Even indexes are Sender and odd indexs are SenderDomains
def flatten_from_tuples(list_tupl):
    # print("Retrieved: {}".format(list_tupl))
    return [item for tup in list_tupl for item in tup]

# Retrieves a list of [Sender, SenderDomain] and returns domain names only
# eg. ['Person', 'Person@Company.com']
# Returns [Company.com]
# By right there should only be one entry but kept in list just in case
# set list to remove duplicates
def identify_domains(list_of_sender_domain_pairs):
    if isinstance(list_of_sender_domain_pairs, list):
        return list(set([item.split(sep='@')[1] for item in list_of_sender_domain_pairs if '@' in item]))
    return list_of_sender_domain_pairs.split(sep='@')[-1]

# Reads all .eml files and rewrites it by prepending a tab for non-header starts
# this is so that the .eml files are modified such that the headers are properly parseable
# Example usage: format_all_mails('../../Mailboxes/IndividualTestMails/Phish/ORG/', 1, 45)
# All header values AND LINES CONTAINING +0000 are skipped the prepending.
# if lines with +0000 are tabbed the email body breaks
def format_all_mails(FILE_PATH, start, end):
    spl = []
    for i in range(start, end+1):
        try:
            with open ('{}{}.eml'.format(FILE_PATH, i), 'r', encoding='utf-8') as pf:
                data = pf.read()
                spl = data.split(sep='\n')
                for idx, line in enumerate(spl):
                    result = re.search(r'(^(Received|Authentication-Results|DKIM-Signature|X-Facebook|Date|To|Subject|Reply-to|Return-Path|From|Errors-To|Feedback-ID|Content-|OriginalChecksum|Message-|X-.*:|--))', line)
                    if not result:
                        spl[idx] = '\t{}'.format(spl[idx])
                    # print(result)

            with open('{}../{}.eml'.format(FILE_PATH, i), 'w', encoding='utf-8') as nf:
                for line in spl:
                        nf.write(line + "\n")
                nf.close()
        except FileNotFoundError:
            pass

def load_model(MODEL_NAME) -> RandomForestClassifier:
    return joblib.load(MODEL_NAME)
