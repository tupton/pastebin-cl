# PASTEBIN WORKFLOW

You can use the pastebin.sh script in the OS X Services menu.

First, in order to use the workflow as-is, we must make sure the script is available. The workflow
assumes the pastebin script is in `/usr/local/bin/pastebin`. You can alias the script:

     $ ln -s ~/path/to/script/pastebin.sh /usr/local/bin/pastebin
         
Obviously, replace `path/to/script` (and/or `/usr/local/bin/`) with the appropriate paths.

Next, you need to place the workflow where the Services menu can see it. Move the workflow to
`~/Library/Services/`. You may have to open the workflow and resave it in order for the Services
menu to be aware of the new workflow.

While you have the workflow open, you can tweak it. Currently, the workflow passes `-c` in order to
paste the text being posted to pastebin to your clipboard first. This is useful if you are using a
clipboard manager like [Jumpcut][jc].

[jc]: http://jumpcut.sourceforge.net/

