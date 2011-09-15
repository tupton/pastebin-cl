# PASTEBIN-CL

Use [pastebin][pb] from the commandline. See [the blog post][bp] for information on how this script came
to be and to leave any comments or questions.

[pb]: http://pastebin.com/
[bp]: http://www.thomasupton.com/blog/2010/12/pastebin-from-the-commandline/


## USAGE

    Usage: pastebin.py [-h] [-v] [-cp] [-f FILE] [--paste-name PASTE_NAME]
                           [--paste-expire-date PASTE_EXPIRE_DATE]
                           [--paste-format PASTE_FORMAT]
                           [--username USERNAME]
                           [--password PASSWORD]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -c, --copy-text       copy the text that is posted to pastebin.com before
                            copying the pastebin.com URL
      -f FILE, --file=FILE  read from FILE instead of stdin
      -p, --print-response  print the response from the pastebin API instead of
                            copying it to the clipboard

      Pastebin API Options:
        These options are passed to the pastebin API request.

        --paste-name=PASTE_NAME
                            the name to give to the pasted text
        --paste-private     whether to make the paste private
        --paste-expire-date=PASTE_EXPIRE_DATE
                            when to expire the paste; valid values are N, 10M, 1H,
                            1D, and 1M
        --paste-format=PASTE_FORMAT
                            the format used for syntax highlighting; see
                            http://pastebin.com/api.php for valid values
        --username=USERNAME
                            your pastebin.com username
        --password=PASSWORD
                            your pastebin.com password

I find it useful to put the script where it is readily available, like so:

    $ ln -s ~/path/to/script/pastebin.py /usr/local/bin/pastebin

Obviously, replace `path/to/script` (and/or `/usr/local/bin/`) with the appropriate paths. If you use the `username` and `password` options, a cache file called `.pastebin_user_key_cache` will be created in the same directory that the script is running in.

Use `-c` to copy the contents of what is being posted first. This is useful if you are using a clipboard manager that can handle multiple items, such as [Jumpcut][jc].

[jc]: http://jumpcut.sourceforge.net/

## OS X Service

Under `automator/`, there is an OS X Automator workflow. This can aid in using the pastebin script from the OS X Services menu. Put this workflow into `~/Library/Services` (create that directory if it does not already exist.) Then open the *Keyboard Shortcut* preferences and make sure "Paste to pastebin.com" is checked under the **Services** item. See the `WORKFLOW.md` help file under `automator/` for more instructions.
