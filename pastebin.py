#! /usr/bin/env python

import sys
import os
import urllib2
import optparse
import time

PASTEBIN_API = "http://pastebin.com/api_public.php"

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

    parser = optparse.OptionParser("Paste text to pastebin.com")

    parser.add_option('-c', '--copy', default=False, action='store_true',
            help="copy the text that is posted to pastebin.com before copying the pastebin.com URL")
    parser.add_option('-f', '--file', default=False, action='store',
            help="read from FILE instead of stdin")

    return parser

def paste_to_pastebin(lines):
    """
    Post the given text to pastebin and return the response from the api
    """

    to_paste = "paste_code=" + lines
    request = urllib2.Request(url=PASTEBIN_API, data=to_paste)
    response = urllib2.urlopen(request)
    pastebin = response.read()
    return pastebin

def main(argv):
    """
    Parse the command lines options and paste the given text to pastebin.com
    """

    parser = create_opt_parser()
    opts, args = parser.parse_args(argv)

    if opts.file != False:
        file = open(args.file, 'r')
    else:
        file = sys.stdin

    lines = "".join(file.readlines())

    if opts.copy == True:
        copy_text(lines)

    pastebin_response = paste_to_pastebin(lines)
    copy_text(pastebin_response)

if __name__ == '__main__':
    main(sys.argv[1:])

