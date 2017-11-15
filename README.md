# pyshare
A simple python script that aims to replace the most basic functionalities (TL Note: the ones I used) of ShareX.
This wouldn't be necessary if ShareX had just been developed as a cross-platform project, but I digress.  
Needless to say, this is being developed for and tested on Linux. If you're on Windows, just use ShareX.\
~~Only (s)ftp uploads for now~~ I added simple curl commands (like used by 0x0), as well as a small server that can receive them.
I should add that the focus will be on a self-hosted server. If you don't care about that, just `curl` 0x0.st or something.
#### What works:
- Taking area screenshots
- Uploading screenshots to (s)ftp
- Generating a link from that and putting it into the clipboard
#### What's planned
- Local file upload
- Mirroring url contents on the remote server

### Dependencies
`pysftp` which can be installed via pip:
```
$ pip install pysftp
```
`escrotum` and `notify-send` which should be available in your favorite package manager 
(or pre-installed, depending on your distribution and desktop environment).

### Usage
Change all the relevant variables in `config.py` and execute
```
$ python3 pyshare
```
to take a screenshot and upload it.
Depending on your window manager, you can bind this to a hotkey. To cancel the capture, simply right-click. 
The script will then, uh, terminate (which is fancy speak for crash because it really doesn't matter).

You can also use the script to upload local files, mirror websites, or share your clipboard. Simply execute
```
$ python3 pyshare -m text
```
This is automatically  choose an action based on the contents of your clipboard. Links will be downloaded and mirrored, local paths will be uploaded, and other strings will be uploaded as text files to the remote host.  

Afterwards, the link is automatically copied to clipboard.
