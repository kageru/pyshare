# === General ===
# Can be 'curl' or 'sftp'
uploader = 'curl'
# Enable or disable thumbnail previews in the notification (only for image uploads, broken on some distros)
enable_thumbnails = False

# === SFTP-related ===
# (S)FTP credentials, only if you want to use SFTP for uploads
# Set all to None that you don’t need
sftp_address = 'your_domain.com'
sftp_port = 22
username = None
password = None
private_key = None
private_key_pass = None
# Directory on the ftp server where you want the screenshots to be sent
remote_directory = '/usr/share/nginx/html/pyshare/'
# Template for the link that the script will generate. {} is the filename
url_template = 'https://your_domain.com/pyshare/{}'

# === curl-related ===
# This should contain a complete curl command with a {} to insert the filename.
curl_command = 'curl -F"file=@{}" https://0x0.st'

# === Local storage ===
# This is where the screenshots are saved locally
local_directory = '/home/kageru/pyshare/'
# If set to false, images will be deleted after uploading them
keep_local_copies = True

# In case you want a certain prefix for all files. Can also be an empty string
# The filename will be used for local storage as well as the files stored on the SFTP host
prefix = ''
# Number of random characters in the filename
length = 5

# Additional folder nesting to include the current year/date/month.
# Leading/Trailing slashes can be omitted. The syntax follows Python’s strftime as documented here:
# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
# Leave empty to disable nesting.
# Example: '%y/%m' to store files in $local_directory/18/03/file.png (for March 2018)
local_directory_nesting = ''
# Set this to True to also use the date-based folder structure on the remote server
preserve_folders_on_remote = True

