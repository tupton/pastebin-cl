# PASTEBIN-CL

Use [pastebin][pb] from the commandline.

[pb]: http://pastebin.com/


## USAGE

    pastebin [-ch] [-f filename]

        -c  Copy the text that is pasted to the pastebin before copying the pastebin.com url.

        -f  Read from FILENAME instead of from STDIN

        -h  Print this help message

I find it useful to put the script where it is readily available, like so:

    $ ln -s ~/path/to/script/pastebin.sh /usr/local/bin/pastebin
    
Obviously, replace `path/to/script` (and/or `/usr/local/bin/`) with the appropriate paths.

Use `-c` to copy the contents of what is being posted first. This is useful if you are using a clipboard manager that can handle multiple items, such as [Jumpcut][jc].

[jc]: http://jumpcut.sourceforge.net/

## OS X Service

Under `automator/`, there is an OS X Automator workflow. This can aid in using the pastebin script from the OS X Services menu. Put this workflow into `~/Library/Services` (create that directory if it does not already exist.) Then open the *Keyboard Shortcut* preferences and make sure "Paste to pastebin.com" is checked under the **Services** item. See the `WORKFLOW.md` help file under `automator/` for more instructions.