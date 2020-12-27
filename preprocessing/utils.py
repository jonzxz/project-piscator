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
