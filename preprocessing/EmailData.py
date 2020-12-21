import re

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
        self.__content = content
        self.__from = from_
        self.__attachments = attachments

    ## -- Jon START --
    def process_https_tokens(self):
        # self.feature_https_tokens =
        num_http = len(re.findall(r'http:', self.get_content()))
        num_https = len(re.findall(r'https:', self.get_content()))
        self.set_feature_https_token(num_https)

    def process_domain_age(self):
        # self.__feature_domain_age =
        pass

    def process_matching_domain(self):
        # self.__feature_matching_domain =
        pass

    def process_keyword_count(self):
        # self.__feature_keyword_count =
        pass
    ## -- Jon END --

    ## -- Zuhree START --
    def process_html_header(self):
        # self.__feature_presence_html_header =
        pass

    def process_ip_url(self):
        # self.__feature_ip_url =
        pass

    def process_presence_js(self):
        # self.__feature_presence_js =
        pass

    def process_presence_form_tag(self):
        # self.__feature_presence_form_tag =
        pass

    def process_subdomain_links(self):
        # self.__feature_subdomain_links =
        pass
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
