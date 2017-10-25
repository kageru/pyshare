# Can be 'curl' or 'sftp'
uploader = 'curl'

# (S)FTP credentials, only if you want to use SFTP for uploads
sftp_address = 'your_domain.com'
username = 'your_ftp_user'
password = 'your_ftp_password'

# curl parameters, if you're using pyshare_receivere
curl_target = 'your_domain.com:5000'
curl_user = 'user1'
curl_password = 'password'

# This should contain a complete curl command with a {} to insert the filename.
# Setting this to anything but None will result in the other curl parameters to be ignored
# Example: 'curl -F"file=@{}" https://0x0.st'
custom_curl_command = None

# This is where the screenshots are saved locally
local_directory = '/home/kageru/pyshare/'

# Directory on the ftp server where you want the screenshots to be sent to
remote_directory = '/usr/share/nginx/html/pyshare/'
# Template for the link that the script will generate. {} is the filename
url_template = 'https://your_domain.com/pyshare/{}'
remote_port = 5000

# In case you want a certain prefix for all files. Can also be an empty string
prefix = ''
# Number of random characters in the filename
length = 5
