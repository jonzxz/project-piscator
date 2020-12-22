import re, datetime, whois
from utils import clean_up_raw_body, flatten_from_tuples, identify_domains

class EmailData:
    def __init__(self, subject, from_, attachments, content):
        self.__feature_https_tokens = 0
        self.__feature_domain_age = 0
        self.__feature_matching_domain = 0
        self.__feature_keyword_count = 0
        self.__feature_presence_html_header = 0
        self.__feature_ip_url = 0
        self.__feature_presence_js = 0
        self.__feature_presence_form_tag = 0
        self.__feature_subdomain_links = 0

        self.__subject = subject
        self.__content = clean_up_raw_body(content)
        self.__from = flatten_from_tuples(from_)
        self.__attachments = attachments
        # Returns a list of domains
        self.__domain = identify_domains(self.get_from())

    ## -- Jon START --
    def process_https_tokens(self):
        num_http = len(re.findall(r'http:', self.get_content()))
        num_https = len(re.findall(r'https:', self.get_content()))
        # Need to determine 1 or -1 based on num https counted
        # eg. 1 HTTP 3 HTTPS, 1 or -1??? there isn't a clear determining of what
        # does processing the https token do and what's the threshold if any
        self.set_feature_https_token(num_https)


    # One issue with processing domain age is that the From: header can be spoofed to be a valid one
    # There will be chances where encoding will fail in future processing if it contains things like
    # service@intI-ÒaypaÓ.com
    def process_domain_age(self):
        # Iterate through a list of domain (likely only one) to perform whois and
        # return a creation date. Some entries for some reason are nested in a [1][1] list
        # so isinstance checks if 1st element is a list and takes it out into a flat list

        # Returns a list of creation dates for domains
        domain_age = ([whois.whois(dom).creation_date for dom in self.get_domain()])

        # -- Test domains - gmail is valid for both conditions
        # domain_age = [whois.whois(dom).creation_date for dom in ['gmail.com']]
        # domain_age = [whois.whois(dom).creation_date for dom in ['skyfi.com']]

        # eg. [[datetime.datetime(1995, 8, 13, 4, 0), datetime.datetime(1995, 8, 13, 0, 0)]]
        # transforms into flat list
        if isinstance(domain_age[0], list):
            domain_age = domain_age[0]

        # eg. [datetime.datetime(1995, 8, 13, 4, 0), datetime.datetime(1995, 8, 13, 0, 0)]
        # returns 1995/8/13:0400
        # max returns the "youngest" (latest) creation date

        # If domain returns a single datetime then [0] domain_age to get the only element
        if not len(domain_age) == 1:
            domain_age = max(domain_age)
        else:
            domain_age = domain_age[0]

        # Compares difference in days from current time to domain_age in days
        diff_days = (datetime.datetime.now() - domain_age).days

        # If domain age more than 30 days return 1 (not phish) else -1 (phish)
        self.set_feature_domain_age(1 if diff_days <= 30 else -1)

    def process_matching_domain(self):
        # self.__feature_matching_domain =
        pass

    def process_keyword_count(self):
        # self.__feature_keyword_count =
        pass
    ## -- Jon END --

    ## -- Zuhree START --
    def process_html_header(self):
        # Regex check for html header
        checkhtmlheader = re.compile(r'(<html>)')

        # Checks if the string is empty
        if not self.get_content().strip():
            return 0

        # Checks the message with the regex and extracts it out
        header = re.search(checkhtmlheader, self.get_content())
        # If matches with the regex
        if header:
            return 1
        else:
            return -1

    def process_ip_url(self):
        # Regex check for ip address
        checkipregex = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')

        # Checks if the string is empty
        if not self.get_content().strip():
            return 0

        # Checks the message with the regex and extracts it out
        ips = re.findall(checkipregex, self.get_content())

        # For each ip found, checks if it matches the regex
        for ip in ips:
            print(ip)
            # Checks the ip with a black list ip checker
            # ip_checker = pydnsbl.DNSBLIpChecker()
            # result = ip_checker.check(ip)
            # if result.blacklisted:
            return 1
            # continue

        return -1

    def process_presence_js(self):
        # Regex check for javascript
        checkjavascript = re.compile(r'(javascript|Javascript|JavaScript|<script>)')

        # Checks if the string is empty
        if not self.get_content().strip():
            return 0

        # Checks the message with the regex and extracts it out
        checkJS = re.search(checkjavascript, self.get_content())
        # If matches with the regex
        if checkJS:
            return 1
        else:
            return -1

    def process_presence_form_tag(self):
        # Regex check for form
        checkformtag = re.compile(r'<(?:form|Form)')

        # Checks if the string is empty
        if not self.get_content().strip():
            return 0

        # Checks the message with the regex and extracts it out
        checkForm = re.search(checkformtag, self.get_content())
        # If matches with the regex
        if checkForm:
            return 1
        else:
            return -1

    def process_subdomain_links(self):
        # Regex check for sub domain
        subdomainregex = re.compile(r'([a-z0-9|-]+\.)*[a-z0-9|-]+\.[a-z]+')

        # Checks if the string is empty
        if not self.get_content().strip():
            return 0

        # Checks the message with the regex and extracts it out
        links = re.findall(subdomainregex, self.get_content())

        # Check each link if the domain has more than 3 dots
        for link in links:
            if link.count('.') > 3:
                return 1
            else:
                continue

        return -1
    ## -- Zuhree END --

    def generate_features(self):
        self.process_https_tokens()
        self.process_domain_age()
        self.process_matching_domain()
        self.process_keyword_count()
        self.process_html_header()
        self.process_ip_url()
        self.process_presence_js()
        self.process_presence_js()
        self.process_presence_form_tag()
        self.process_subdomain_links()

    def get_subject(self):
        return self.__subject

    def get_content(self):
        return self.__content

    def get_from(self):
        return self.__from

    def get_attachments(self):
        return self.__attachments

    def get_domain(self):
        return self.__domain

    def __repr__(self):
        return "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}".format(self.__feature_https_tokens, \
            self.__feature_domain_age, \
            self.__feature_matching_domain, \
            self.__feature_keyword_count, \
            self.__feature_presence_html_header, \
            self.__feature_ip_url, \
            self.__feature_presence_js, \
            self.__feature_presence_form_tag, \
            self.__feature_subdomain_links)

    def set_feature_https_token(self, num):
        self.__feature_https_tokens = num

    def get_feature_https_token(self):
        return self.__feature_https_tokens

    def set_feature_domain_age(self, num):
        self.__feature_domain_age = num

    def get_feature_domain_age(self):
        return self.__feature_domain_age
