#! /usr/bin/env python

import sys
import os
import urllib
import urllib2
import optparse
import time
from subprocess import Popen, PIPE

VERSION = """%prog 0.6 by Thomas Upton

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

    PASTEBIN_USER_KEY_CACHE = '.pastebin_user_key_cache'

    pastebin_api = "https://pastebin.com/api/api_post.php"
    pastebin_user_api = "https://pastebin.com/api/api_login.php"
    pastebin_dev_key = "564b1c623712f731a96c7820dff4ab9f"

    def __init__(self, paste_code, paste_name=None, paste_private=False,
            paste_expire_date=PASTEBIN_EXPIRE_NEVER, paste_format=None, username=None,
            password=None):

        self.set_paste_code(paste_code)
        self.set_paste_name(paste_name)
        self.set_paste_private(paste_private)
        self.set_paste_expire_date(paste_expire_date)
        self.set_paste_format(paste_format)
        self.set_username(username)
        self.set_password(password)

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

    def set_paste_private(self, paste_private):
        paste_private = paste_private == True
        self._paste_private = paste_private

    def set_paste_expire_date(self, paste_expire_date):
        if not paste_expire_date in self.PASTEBIN_EXPIRE:
            paste_expire_date = self.PASTEBIN_EXPIRE_NEVER
        self._paste_expire_date = paste_expire_date

    def set_paste_format(self, paste_format):
        self._paste_format = paste_format

    def set_username(self, username):
        self._username = username

    def set_password(self, password):
        self._password = password

    def get_paste_code(self):
        return self._paste_code

    def get_paste_name(self):
        return self._paste_name

    def get_paste_private(self):
        paste_private = "0"
        if self._paste_private is True:
            paste_private = "1"

        return paste_private

    def get_paste_expire_date(self):
        return self._paste_expire_date

    def get_paste_format(self):
        return self._paste_format

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def _build_request(self):

        request_url = self.pastebin_api

        user_key = self._get_user_key()

        request_data = self._build_param_string(user_key)

        return urllib2.Request(url=request_url, data=request_data)

    def _build_param_string(self, user_key):

        params = dict()

        if not self.get_paste_code():
            raise Exception, "No paste_code was given"

        params['api_option'] = 'paste'
        params['api_dev_key'] = self.pastebin_dev_key
        params['api_paste_code'] = self.get_paste_code()

        if self.get_paste_name() is not None:
            params['api_paste_name'] = self.get_paste_name()

        if self.get_paste_private() != "0":
            params['api_paste_private'] = self.get_paste_private()

        params['api_paste_expire_date'] = self.get_paste_expire_date()

        if self.get_paste_format() is not None:
            params['api_paste_format'] = self.get_paste_format()

        if user_key is not None:
            params['api_user_key'] = user_key

        return self._encode_params(params)

    def _build_user_param_string(self):

        params = dict()

        params['api_user_name'] = self.get_username()
        params['api_user_password'] = self.get_password()
        params['api_dev_key'] = self.pastebin_dev_key

        return self._encode_params(params)

    def _encode_params(self, params):
        encoded = urllib.urlencode([(k, v) for (k, v) in params.iteritems()])
        return encoded

    def _get_user_key(self):
        username = self.get_username()
        password = self.get_password()

        user_key = None
        if username is not None and password is not None:
            user_key = self._get_user_key_from_cache(username)

            if user_key is None:
                user_request_url = self.pastebin_user_api
                user_request_data = self._build_user_param_string()
                user_request = urllib2.Request(url=user_request_url, data=user_request_data)
                user_response = urllib2.urlopen(user_request)
                user_key = user_response.read()
                self._put_user_key_in_cache(username, user_key)

        return user_key

    def _get_user_key_from_cache(self, username):
        user_key = None

        try:
            cache = open(self.PASTEBIN_USER_KEY_CACHE, 'r')
        except IOError:
            cache = open(self.PASTEBIN_USER_KEY_CACHE, 'w')
            cache.close()
            cache = open(self.PASTEBIN_USER_KEY_CACHE, 'r')

        for line in cache:
            parts = line.split()
            if len(parts) == 2 and parts[0] == username:
                user_key = parts[1]
        
        cache.close()
        return user_key

    def _put_user_key_in_cache(self, username, user_key):
        cache = open(self.PASTEBIN_USER_KEY_CACHE, 'a')
        cache.write(' '.join([username, user_key]))
        cache.write('\n')
        cache.close()

def copy_text(text):
    """
    Copy text to the system clipboard
    """

    cb_name = get_clipboard_name()

    if cb_name is not None:
        clipboard = Popen(cb_name, shell=True, stdin=PIPE).stdin
        clipboard.write(text)
        clipboard.close()

def get_clipboard_name():
    """Get the name of the system clipboard"""

    cb_list = ['pbcopy', 'xclip', 'putclip']

    cb_name = None
    for cb in cb_list:
        if cli_exists(cb):
            cb_name = cb
            break

    return cb_name

def cli_exists(command):
    """Determine whether or not a command line command exists"""
    exists = False

    test = 'type %s >> /dev/null 2>&1' % command
    process = Popen(test, shell=True, stdout=PIPE)
    process.stdout.close()
    if not process.wait():
        exists = True

    return exists

def create_opt_parser():
    """
    Creates an option parser using optparse
    """

    parser = optparse.OptionParser(usage="""usage: pastebin.py [-h] [-v] [-cp] [-f FILE] [--paste-name PASTE_NAME]
                       [--paste-expire-date PASTE_EXPIRE_DATE]
                       [--paste-format PASTE_FORMAT]
                       [--username USERNAME]
                       [--password PASSWORD]""", epilog="Paste text to pastebin.com.",
            version=VERSION)

    parser.add_option('-c', '--copy-text', default=False, action='store_true',
            help="copy the text that is posted to pastebin.com before copying the pastebin.com URL")
    parser.add_option('-f', '--file', default=False, action='store',
            help="read from FILE instead of stdin")
    parser.add_option('-p', '--print-response', default=False, action='store_true',
            help="print the response from the pastebin API instead of copying it to the clipboard")

    # pastebin API options
    pastebin_api_group = optparse.OptionGroup(parser, "Pastebin API Options",
        "These options are passed to the pastebin API request.")
    pastebin_api_group.add_option('--paste-name', default=None, action='store',
            help="the name to give to the pasted text")
    pastebin_api_group.add_option('--paste-private', default=False, action='store_true',
            help="whether to make the paste private")
    pastebin_api_group.add_option('--paste-expire-date', default=None, action='store',
            help="when to expire the paste; valid values are N, 10M, 1H, 1D, and 1M")
    pastebin_api_group.add_option('--paste-format', default=None, action='store',
            help="the format used for syntax highlighting; see http://pastebin.com/api.php for valid values")
    pastebin_api_group.add_option('--username', default=None, action='store',
            help="your pastebin.com username")
    pastebin_api_group.add_option('--password', default=None, action='store',
            help="your pastebin.com password")
    parser.add_option_group(pastebin_api_group)

    return parser

def growl_notify(pastebin_response):
    """Use Growl via Applescript to create a notification with pastebin's response."""

    if not cli_exists('osascript'):
        return

    growl_app = 'Growl'

    growl_helper_applescript = 'tell application "System Events" to (name of processes) contains "GrowlHelperApp"'
    osascript = Popen("osascript -e '" + growl_helper_applescript + "'", shell=True, stdout=PIPE)
    stdout,stderr = osascript.communicate()

    if stdout.strip() == "true":
        growl_app = 'GrowlHelperApp'

    applescript = """ tell application "%(growl_app)s"
set allNotificationsList to {"Pastebin Notification"}
set enabledNotificationsList to {"Pastebin Notification"}
register as application "Pastebin Commandline" all notifications allNotificationsList default notifications enabledNotificationsList icon of application "Script Editor"
notify with name "Pastebin Notification" title "Pastebin" description "%(pastebin_response)s" application name "Pastebin Commandline"
end tell """ % {'growl_app': growl_app, 'pastebin_response': pastebin_response}

    osascript = Popen("osascript -e '%s'" % applescript, shell=True)
    osascript.communicate() 

def paste_to_pastebin(lines, opts):
    """
    Post the given text to pastebin and return the response from the api
    """

    pastebin = Pastebin(paste_code=lines, paste_name=opts.paste_name,
            paste_private=opts.paste_private, paste_expire_date=opts.paste_expire_date,
            paste_format=opts.paste_format, username=opts.username, password=opts.password)
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

    if opts.copy_text:
        copy_text(lines)

    pastebin_response = paste_to_pastebin(lines, opts)

    growl_notify(pastebin_response)

    if opts.print_response:
        print pastebin_response
    else:
        copy_text(pastebin_response)

if __name__ == '__main__':
    main(sys.argv[1:])

