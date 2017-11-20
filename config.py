# Can be 'curl' or 'sftp'
uploader = 'sftp'

# (S)FTP credentials, only if you want to use SFTP for uploads
# Set all to None that you don’t need
sftp_address = 'your_domain.com'
sftp_port = 22
username = None
password = None
private_key = None
private_key_pass = None

# This should contain a complete curl command with a {} to insert the filename.
# Example: 'curl -F"file=@{}" https://0x0.st'
curl_command = None

# This is where the screenshots are saved locally
local_directory = '/home/kageru/pyshare/'

# Directory on the ftp server where you want the screenshots to be sent
remote_directory = '/usr/share/nginx/html/pyshare/'
# Template for the link that the script will generate. {} is the filename
url_template = 'https://your_domain.com/pyshare/{}'
remote_port = 5000

# In case you want a certain prefix for all files. Can also be an empty string
prefix = ''
# Number of random characters in the filename
length = 5
