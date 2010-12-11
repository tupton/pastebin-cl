#! /usr/bin/env python

import sys
import os
import urllib2
import optparse
import time

VERSION = """%prog 0.1b by Thomas Upton

Use `%prog -h` for help and a list of options.
"""

class Pastebin(object):
    """A wrapper for the pastebin API"""

    PASTEBIN_EXPIRE_NEVER       = "N"
    PASTEBIN_EXPIRE_TEN_MINUTES = "10M"
    PASTEBIN_EXPIRE_ONE_HOUR    = "1H"
    PASTEBIN_EXPIRE_ONE_DAY     = "1D"
    PASTEBIN_EXPIRE_ONE_MONTH   = "1M"

    PASTEBIN_EXPIRE = [PASTEBIN_EXPIRE_NEVER, PASTEBIN_EXPIRE_TEN_MINUTES, PASTEBIN_EXPIRE_ONE_HOUR,
            PASTEBIN_EXPIRE_ONE_DAY, PASTEBIN_EXPIRE_ONE_MONTH]

    pastebin_api = "http://pastebin.com/api_public.php"

    def __init__(self, paste_code, paste_name=None, paste_email=None, paste_subdomain=None,
            paste_private=False, paste_expire_date=PASTEBIN_EXPIRE_NEVER, paste_format=None):

        self.set_paste_code(paste_code)
        self.set_paste_name(paste_name)
        self.set_paste_email(paste_email)
        self.set_paste_subdomain(paste_subdomain)
        self.set_paste_private(paste_private)
        self.set_paste_expire_date(paste_expire_date)
        self.set_paste_format(paste_format)

    def paste(self):
        """Submit the paste request to pastebin"""

        request = self._build_request()
        response = urllib2.urlopen(request)
        response = response.read()
        return response
        
    def set_paste_code(self, paste_code):
        self._paste_code = paste_code

    def set_paste_name(self, paste_name):
        self._paste_name = paste_name

    def set_paste_email(self, paste_email):
        self._paste_email = paste_email

    def set_paste_subdomain(self, paste_subdomain):
        self._paste_subdomain = paste_subdomain

    def set_paste_private(self, paste_private):
        paste_private = paste_private == True
        self._paste_private = paste_private

    def set_paste_expire_date(self, paste_expire_date):
        if not paste_expire_date in self.PASTEBIN_EXPIRE:
            paste_expire_date = self.PASTEBIN_EXPIRE_NEVER
        self._paste_expire_date = paste_expire_date

    def set_paste_format(self, paste_format):
        self._paste_format = paste_format

    def get_paste_code(self):
        return self._paste_code

    def get_paste_name(self):
        return self._paste_name

    def get_paste_email(self):
        return self._paste_email

    def get_paste_subdomain(self):
        return self._paste_subdomain

    def get_paste_private(self):
        paste_private = "0"
        if self._paste_private == True:
            paste_private = "1"

        return paste_private

    def get_paste_expire_date(self):
        return self._paste_expire_date

    def get_paste_format(self):
        return self._paste_format

    def _build_request(self):

        request_url = self.pastebin_api
        request_data = self._build_param_string()

        return urllib2.Request(url=request_url, data=request_data)

    def _build_param_string(self):

        params = dict()

        if not self.get_paste_code():
            raise Exception, "No paste_code was given"

        params['paste_code'] = self.get_paste_code()

        if self.get_paste_name() is not None:
            params['paste_name'] = self.get_paste_name()

        if self.get_paste_subdomain() is not None:
            params['paste_subdomain'] = self.get_paste_subdomain()

        if self.get_paste_private() != "0":
            params['paste_private'] = self.get_paste_private()

        params['paste_expire_date'] = self.get_paste_expire_date()

        if self.get_paste_format() is not None:
            params['paste_format'] = self.get_paste_format()

        return "&".join([k + "=" + str(v) for (k, v) in params.iteritems()])

def copy_text(text):
    """
    Copy text to the OS X system clipboard
    """

    out = os.popen('pbcopy', 'w')
    out.write(text)
    out.close()

def create_opt_parser():
    """
    Creates an option parser using optparse
    """

    parser = optparse.OptionParser(usage="%prog [-hc] [-f file]", epilog="Paste text to pastebin.com.",
            version=VERSION)

    parser.add_option('-c', '--copy', default=False, action='store_true',
            help="copy the text that is posted to pastebin.com before copying the pastebin.com URL")
    parser.add_option('-f', '--file', default=False, action='store',
            help="read from FILE instead of stdin")

    return parser

def paste_to_pastebin(lines):
    """
    Post the given text to pastebin and return the response from the api
    """

    pastebin = Pastebin(paste_code=lines)
    response = pastebin.paste()
    return response

def main(argv):
    """
    Parse the command lines options and paste the given text to pastebin.com
    """

    parser = create_opt_parser()
    opts, args = parser.parse_args(argv)

    if opts.file != False:
        file = open(opts.file, 'r')
    else:
        file = sys.stdin

    lines = "".join(file.readlines())

    if opts.copy == True:
        copy_text(lines)

    pastebin_response = paste_to_pastebin(lines)
    copy_text(pastebin_response)

if __name__ == '__main__':
    main(sys.argv[1:])

