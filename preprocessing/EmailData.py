import re, datetime, whois
from utils import clean_up_raw_body, flatten_from_tuples, identify_domains
from whois.parser import PywhoisError

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
        self.__from = flatten_from_tuples(from_) if isinstance(from_, list) else from_
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
        self.set_feature_https_token(num_http-num_https)

    # One issue with processing domain age is that the From: header can be spoofed to be a valid one
    # There will be chances where encoding will fail in future processing if it contains things like
    # service@intI-ÒaypaÓ.com
    def process_domain_age(self):
        # Iterate through a list of domain (likely only one) to perform whois and
        # return a creation date. Some entries for some reason are nested in a [1][1] list
        # so isinstance checks if 1st element is a list and takes it out into a flat list

        try:
            # Returns a either a list of datetime, a datetime or string
            domain_age = ([whois.whois(dom).creation_date for dom in self.get_domain()]) \
            if isinstance(self.get_domain(), list) else whois.whois(self.get_domain()).creation_date

            # print("Domain Age: {} -- Type: {}".format(domain_age, type(domain_age)))
            # Some TLDs don't work with python-whois because it's not in the data of the lib
            # eg. .com.sg - so just return a 0 in this case
            if domain_age.count(0) < 1 and domain_age[0] is None:
                self.set_feature_domain_age(0)
                return

            # -- Test domains - gmail is valid for both conditions
            # domain_age = [whois.whois(dom).creation_date for dom in ['gmail.com']]
            # domain_age = [whois.whois(dom).creation_date for dom in ['skyfi.com']]

            # eg. [[datetime.datetime(1995, 8, 13, 4, 0), datetime.datetime(1995, 8, 13, 0, 0)]]
            # transforms into flat list
            if isinstance(domain_age, list) and isinstance(domain_age[0], list):
                domain_age = domain_age[0]

            # Sometimes whois returns .creation_date as a str instead of datetime
            # Attempts to convert string datetime to datetime object
            # %b if month is represented as Jan/Feb/Mar
            if isinstance(domain_age, str):
                try:
                    domain_age = datetime.datetime.strptime(domain_age, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    domain_age = datetime.datetime.strptime(domain_age, '%d-%b-%Y %H:%M:%S')

            # eg. [datetime.datetime(1995, 8, 13, 4, 0), datetime.datetime(1995, 8, 13, 0, 0)]
            # returns 1995/8/13:0400
            # max returns the "youngest" (latest) creation date
            # If max throws error because of difference in datetime format then
            # take first element in list

            # If domain returns a single datetime then [0] domain_age to get the only element
            try:
                if isinstance(domain_age, list) and not len(domain_age) == 1:
                        domain_age = max(domain_age)
                else:
                    domain_age = domain_age[0]
            except TypeError:
                try:
                    if isinstance(domain_age, datetime.datetime):
                        domain_age = domain_age
                    else:
                        domain_age = domain_age[0]
                except TypeError:
                    self.set_feature_domain_age(0)
                    return

            # Compares difference in days from current time to domain_age in days
            diff_days = (datetime.datetime.now() - domain_age).days

            # If domain age more than 30 days return 1 (not phish) else -1 (phish)
            self.set_feature_domain_age(1 if diff_days <= 30 else -1)
        except PywhoisError:
            self.set_feature_domain_age(1)

    # main_domain iterates through self.__domain which is set as a list
    # splits each element and returns the last 2 elements because some domains are like
    # test.ebay.com, the split and join returns 'ebay.com'
    # it is done in this way so that even if it's just 'ebay.com' it will return the same thing

    # domains_in_mail does a regex catch to get all <site>.<TLD> with the same split idea as above
    # from the content body of email. Returns a set so that duplicates are removed
    # Regex searches for all http:// or https:// or https://www. so on and returns the
    # website.com or website.net or whatever found
    # If the length of main_domain is actually 1 (which in most cases it should be)
    # then it checks if the main_domain is in each element of domains_in_mail
    # If it is not then count is incremented
    # If length of main_domain is more than 1 then it'll enter a nested loop to tally
    # For this function IP addresses will not be split correctly resulting in half-IP
    # which itself is sufficient to test for matching domains, since in the first place
    # a legitimate sender will be DNS resolved instead of raw IP.

    ## UPDATE FOR MAILBOX CHECKS
    # There's a chance self.get_domain() returns a string instead of list
    # So it returns directly as it is. This affects the counts for domain checks
    # Modified such that if main_domains in list then it will traverse as per preprocessing
    # Otherwise it'll just be a single check
    # **THIS MIGHT END UP FAIRLY INACCURATE DUE TO DOMAIN=google.com and in_mail contains GOOGLEAPIS.COM**

    ## UPDATE V2
    # Modified function to return a -1 as long as a SINGLE MATCH for self.get_domain()
    # vs. any domain in email
    # otherwise returns a phish (1)
    def process_matching_domain(self):
        main_domains = ['.'.join(dom.split(sep='.')[-2:]) for dom in self.get_domain()] \
        if isinstance(self.get_domain(), list) else self.get_domain()
        domains_in_mail = set(['.'.join((b[0]).split(sep='.')[-2:]) for b in \
        re.findall('((http://www.|https://www.|http://|www.|https://).+?(?=\/))' \
        , self.get_content())])

        count = 0
        if isinstance(main_domains, list):
            if len(main_domains) == 1:
                main_domains = main_domains[0]
                for domain in domains_in_mail:
                    if main_domains == domain:
                        self.set_feature_matching_domain(-1)
                        return
            else:
                for main_d in main_domains:
                    for domain in domains_in_mail:
                        if main_d == domain:
                            self.set_feature_matching_domain(-1)
                            return
        else:
            for domain in domains_in_mail:
                if main_domains == domain:
                    self.set_feature_matching_domain(-1)
                    return

        self.set_feature_matching_domain(1)
        # if isinstance(main_domains, list):
        #     if len(main_domains) == 1:
        #         main_domains= main_domains[0]
        #         for domain in domains_in_mail:
        #             # print("Comparing {} against {}".format(main_domains, domain))
        #             if main_domains not in domain:
        #                 count+=1
        #     else:
        #         for main_d in main_domains:
        #             # print("Comparing {} against {}".format(main_d, domain))
        #             for domain in domains_in_mail:
        #                 if main_d not in domain:
        #                     count+=1
        # else:
        #     for domain in domains_in_mail:
        #         if main_domains not in domain:
        #             count+=1

        # Threshold is set to > 1
        # If more than 1 domain does not match the sender domain then it is
        # given a score of phish (-1)
        # self.set_feature_matching_domain(1 if count > 1 else -1)

    def process_keyword_count(self):
        keywordList = ["suspend", "verify", "username", "password", "update", \
         "confirm", "user", "customer", "client", "restrict", "hold", "verify", \
         "account", "login", "SSN", "Social Security", "NRIC", "label", "invoice", \
         "post", "document", "postal", "calculations", "copy", "fedex", "statement", \
         "financial", "dhl", "usps", "notification", "delivery", "ticket", "paypal", "bank" ]
        count = 0
        # Checks if the string is empty
        if not self.get_content().strip():
            return 0

        for i in keywordList:
            if i.lower() in self.get_content().lower():
                count += 1

        self.set_feature_keyword_count(1 if count > 8 else -1)
    ## -- Jon END --

    ## -- Zuhree START --
    def process_html_header(self):
        # Regex check for html header
        checkhtmlheader = re.compile(r'(<html>)')

        # Checks if the string is empty
        if not self.get_content().strip():
            self.set_feature_presence_html_header(0)
            return

        # Checks the message with the regex and extracts it out
        header = re.search(checkhtmlheader, self.get_content())
        # If matches with the regex
        self.set_feature_presence_html_header(1 if header else -1)

    def process_ip_url(self):
        # Regex check for ip address
        checkipregex = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')

        # Checks if the string is empty
        if not self.get_content().strip():
            self.set_feature_ip_url(0)
            return

        # Checks the message with the regex and extracts it out
        ips = re.findall(checkipregex, self.get_content())

        # For each ip found, checks if it matches the regex
        for ip in ips:
            # print(ip)
            # Checks the ip with a black list ip checker
            # ip_checker = pydnsbl.DNSBLIpChecker()
            # result = ip_checker.check(ip)
            # if result.blacklisted:
            self.set_feature_ip_url(1)
            return
            # continue

        self.set_feature_ip_url(-1)

    def process_presence_js(self):
        # Regex check for javascript
        checkjavascript = re.compile(r'(javascript|Javascript|JavaScript|<script>|<script src)')

        # Checks if the string is empty
        if not self.get_content().strip():
            self.set_feature_presence_js(0)
            return

        # Checks the message with the regex and extracts it out
        checkJS = re.search(checkjavascript, self.get_content())
        # If matches with the regex

        self.set_feature_presence_js(1 if checkJS else -1)

    def process_presence_form_tag(self):
        # Regex check for form
        checkformtag = re.compile(r'<(?:form|Form)')

        # Checks if the string is empty
        if not self.get_content().strip():
            self.set_feature_presence_form_tag(0)
            return

        # Checks the message with the regex and extracts it out
        checkForm = re.search(checkformtag, self.get_content())
        # If matches with the regex
        self.set_feature_presence_form_tag(1 if checkForm else -1)

    def process_subdomain_links(self):
        # Regex check for sub domain
        subdomainregex = re.compile(r'([a-z0-9|-]+\.)*[a-z0-9|-]+\.[a-z]+')

        # Checks if the string is empty
        if not self.get_content().strip():
            self.set_feature_subdomain_links(0)
            return

        # Checks the message with the regex and extracts it out
        links = re.findall(subdomainregex, self.get_content())

        # Check each link if the domain has more than 3 dots
        for link in links:
            if link.count('.') > 3:
                self.set_feature_subdomain_links(1)
                return

        self.set_feature_subdomain_links(-1)
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
        return "{0},{1},{2},{3},{4},{5},{6},{7},{8}".format(self.__feature_https_tokens, \
            self.__feature_domain_age, \
            self.__feature_matching_domain, \
            self.__feature_keyword_count, \
            self.__feature_presence_html_header, \
            self.__feature_ip_url, \
            self.__feature_presence_js, \
            self.__feature_presence_form_tag, \
            self.__feature_subdomain_links)


    def repr_in_arr(self):
        return [[self.__feature_https_tokens, \
            self.__feature_domain_age, \
            self.__feature_matching_domain, \
            self.__feature_keyword_count, \
            self.__feature_presence_html_header, \
            self.__feature_ip_url, \
            self.__feature_presence_js, \
            self.__feature_presence_form_tag, \
            self.__feature_subdomain_links]]

    def set_feature_https_token(self, num):
        self.__feature_https_tokens = num

    def get_feature_https_token(self):
        return self.__feature_https_tokens

    def set_feature_domain_age(self, num):
        self.__feature_domain_age = num

    def get_feature_domain_age(self):
        return self.__feature_domain_age

    def set_feature_matching_domain(self, num):
        self.__feature_matching_domain = num

    def get_feature_matching_domain(self):
        return self.__feature_matching_domain

    def set_feature_presence_html_header(self, num):
        self.__feature_presence_html_header = num

    def get_feature_presence_html_header(self):
        return self.__presence_html_header

    def set_feature_ip_url(self, num):
        self.__feature_ip_url = num

    def get_feature_ip_url(self):
        return self.__feature_ip_url

    def set_feature_presence_js(self, num):
        self.__feature_presence_js = num

    def get_feature_presence_js(self):
        return self.__feature_presence_js

    def set_feature_presence_form_tag(self, num):
        self.__feature_presence_form_tag = num

    def get_feature_presence_form_tag(self):
        return self.__feature_presence_form_tag

    def set_feature_subdomain_links(self, num):
        self.__feature_subdomain_links = num

    def get_feature_subdomain_links(self):
        return self.__feature_subdomain_links

    def set_feature_keyword_count(self, num):
        self.__feature_keyword_count = num

    def get_feature_subdomain_links(self):
        return self.__feature_keyword_count
