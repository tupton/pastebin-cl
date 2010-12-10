#! /usr/local/bin/python2.7

import sys
import os
import urllib2
import argparse

PASTEBIN_API = "http://pastebin.com/api_public.php"

def copy_text(text):
    """
    Copy text to the OS X system clipboard
    """
    command = "echo \"" + text + "\" | pbcopy"
    os.system(command)

def create_arg_parser():
    """
    Creates an argument parser.
    """
    parser = argparse.ArgumentParser(description="Paste text to pastebin.com")
    parser.add_argument('-c', '--copy', default=False , action='store_true',
            help="Copy the text that's posted to pastebin.com before copying the pastebin URL")
    parser.add_argument('-f', '--file', default=False , action='store',
            help="Read from %(dest)s instead of STDIN")

    return parser

def paste_to_pastebin(lines):
    """
    Post the given text to pastebin and return the response from the api
    """
    to_paste = "paste_code=" + lines
    request = urllib2.Request(url=PASTEBIN_API,
                          data=to_paste)
    response = urllib2.urlopen(request)
    pastebin = response.read()
    return pastebin

def main(argv):
    """
    Parse the command lines options and paste the given text to pastebin.com
    """

    parser = create_arg_parser()
    args = parser.parse_args(argv)

    if args.file != False:
        file = open(args.file, 'r')
    else:
        file = sys.stdin

    lines = "".join(file.readlines())

    if args.copy == True:
        copy_text(lines)

    pastebin_response = paste_to_pastebin(lines)
    copy_text(pastebin_response)

if __name__ == '__main__':
    main(sys.argv[1:])

