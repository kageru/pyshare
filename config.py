# (S)FTP credentials
sftp_address = 'your_domain.com'
username = 'your_ftp_user'
password = 'your_ftp_password'

# This is where the screenshots are saved locally
local_directory = '/home/kageru/pyshare/'
# Directory on the ftp server where you want the screenshots to be sent to
remote_directory = '/usr/share/nginx/html/pyshare/'
# Template for the link that the script will generate. {} is the filename
url_template = 'https://your_domain.com/pyshare/{}'
# In case you want a certain prefix for all files. Can also be an empty string
prefix = ''
# Number of random characters in the filename
length = 5
