import re, datetime, whois
from utils import clean_up_raw_body, flatten_from_tuples, identify_domains
import dns.resolver

class EmailData:
    def __init__(self, subject, from_, attachments, content, auth_results):
        self.__feature_https_tokens = 0
        self.__feature_matching_domain = 0
        self.__feature_keyword_count = 0
        self.__feature_presence_html_header = 0
        self.__feature_ip_url = 0
        self.__feature_presence_js = 0
        self.__feature_presence_form_tag = 0
        self.__feature_subdomain_links = 0
        self.__feature_dkim_status = 0
        self.__feature_spf_status = 0
        self.__feature_dmarc_status = 0
        self.__feature_mx_record = 0

        self.__subject = subject
        self.__content = clean_up_raw_body(content)
        self.__from = flatten_from_tuples(from_) if isinstance(from_, list) else from_
        self.__attachments = attachments
        self.__auth_results = clean_up_raw_body(auth_results).split(sep=' ') if auth_results else None
        # Returns a list of domains
        self.__domain = identify_domains(self.get_from())

    ## -- Jon START --
    # number of http / total count. if more than 25% of links are http return a 1
    # if no http return -1
    def process_https_tokens(self):
        num_http = len(re.findall(r'http:', self.get_content()))
        if num_http == 0:
            self.set_feature_https_token(-1)
            return

        num_https = len(re.findall(r'https:', self.get_content()))
        self.set_feature_https_token(1 if num_http/(num_https+num_http) >= 0.25 else -1)

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

    # Keyword count above 20% of length of keyword list
    def process_keyword_count(self):
        keywordList = ["suspend", "verify", "username", "password", "update", \
         "confirm", "user", "customer", "client", "restrict", "hold", "verify", \
         "account", "login", "SSN", "Social Security", "NRIC", "label", "invoice", \
         "post", "document", "postal", "calculations", "copy", "fedex", "statement", \
         "financial", "dhl", "usps", "notification", "delivery", "ticket", "paypal", "bank", \
         "survey", "transfer", "bank", "compensation", "bitcoin", "payment", "investment", \
          "suspended", "verified", "activate"
          ]
        count = 0
        # Checks if the string is empty
        if not self.get_content().strip():
            return 0

        for i in keywordList:
            if i.lower() in self.get_content().lower():
                count += 1

        self.set_feature_keyword_count(1 if count/len(keywordList) >= 0.20 else -1)
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
        checkformtag = re.compile(r'<(?:form|Form)|forms.google')

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
            if link.count('.') > 2:
                self.set_feature_subdomain_links(1)
                return

        self.set_feature_subdomain_links(-1)
    ## -- Zuhree END --

    def process_dkim_status(self):
        if not self.get_auth_results():
            self.set_feature_dkim_status(0)
            return

        dkim_status = [item for item in self.get_auth_results() if 'dkim' in item]
        if dkim_status:
            dkim_status = dkim_status[0].split(sep='=')[1]

        if dkim_status == 'none':
            self.set_feature_dkim_status(1)
        elif dkim_status == 'pass':
            self.set_feature_dkim_status(-1)
        else:
            self.set_feature_dkim_status(0)
        return

    def process_dmarc_status(self):

        if not self.get_auth_results():
            self.set_feature_dkim_status(0)
            return

        dmarc_status = [item for item in self.get_auth_results() if 'dmarc' in item]
        if dmarc_status:
            dmarc_status = dmarc_status[0].split(sep='=')[1]

        if dmarc_status == 'pass':
            self.set_feature_dmarc_status(-1)
        elif dmarc_status == 'bestguesspass' or dmarc_status == 'none' or dmarc_status == 'permerror':
            self.set_feature_dmarc_status(1)
        else:
            self.set_feature_dmarc_status(0)
        return

    def process_spf_status(self):

        if not self.get_auth_results():
            self.set_feature_dkim_status(0)
            return

        spf_status = [item for item in self.get_auth_results() if 'spf' in item]
        if spf_status:
            spf_status = spf_status[0].split(sep='=')[1]

        if spf_status == 'pass':
            self.set_feature_spf_status(-1)
        elif spf_status == 'none' or spf_status == 'fail':
            self.set_feature_spf_status(1)
        else:
            self.set_feature_spf_status(0)
        return

    def process_mx_record(self):
        try:
            if len(self.get_domain()) == 1:
                result = dns.resolver.query(self.get_domain()[0], 'MX')
            else:
                results = [dns.resolver.query(domain, 'MX') for domain in self.get_domain()]
            self.set_feature_mx_record(-1)
        except dns.resolver.NoAnswer:
            # No response, legit domains can also hit this
            self.set_feature_mx_record(1)
        except dns.resolver.NXDOMAIN:
            # No DNS Query name exist
            self.set_feature_mx_record(1)
        except UnicodeError:
            # contains NON ASCII characters
            self.set_feature_mx_record(1)
        except dns.resolver.NoNameservers:
            # No name servers detected
            self.set_feature_mx_record(1)
        except dns.exception.Timeout:
            # Timeouts
            self.set_feature_mx_record(1)
        except dns.name.LabelTooLong:
            # Exist because of processing error in domain identification
            self.set_feature_mx_record(0)

    def generate_features(self):
        self.process_https_tokens()
        self.process_matching_domain()
        self.process_keyword_count()
        self.process_html_header()
        self.process_ip_url()
        self.process_presence_js()
        self.process_presence_form_tag()
        self.process_subdomain_links()
        self.process_dkim_status()
        self.process_dmarc_status()
        self.process_spf_status()
        self.process_mx_record()

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

    def get_auth_results(self):
        return self.__auth_results

    def __repr__(self):
        return "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}".format( \
            self.__feature_https_tokens, \
            self.__feature_matching_domain, \
            self.__feature_keyword_count, \
            self.__feature_presence_html_header, \
            self.__feature_ip_url, \
            self.__feature_presence_js, \
            self.__feature_presence_form_tag, \
            self.__feature_subdomain_links, \
            self.__feature_dkim_status, \
            self.__feature_spf_status, \
            self.__feature_dmarc_status, \
            self.__feature_mx_record
            )


    def repr_in_arr(self):
        return [[self.__feature_https_tokens, \
            self.__feature_matching_domain, \
            self.__feature_keyword_count, \
            self.__feature_presence_html_header, \
            self.__feature_ip_url, \
            self.__feature_presence_js, \
            self.__feature_presence_form_tag, \
            self.__feature_subdomain_links, \
            self.__feature_dkim_status, \
            self.__feature_spf_status, \
            self.__feature_dmarc_status, \
            self.__feature_mx_record]]

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

    def set_feature_dkim_status(self, num):
        self.__feature_dkim_status = num

    def get_feature_dkim_status(self):
        return self.__feature_dkim_status

    def set_feature_dmarc_status(self, num):
        self.__feature_dmarc_status = num

    def get_feature_dmarc_status(self):
        return self.__feature_dmarc_status

    def set_feature_spf_status(self, num):
        self.__feature_spf_status = num

    def get_feature_spf_status(self):
        return self.__feature_spf_status

    def set_feature_mx_record(self, num):
        self.__feature_mx_record = num

    def get_feature_mx_record(self):
        return self.__feature_mx_record
