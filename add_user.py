# This is probably false advertising because it doesn't actually add a user for you.
# It only generates a string that you can copy-paste into users.py

from pyshare_receiver import salthash
import sys


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('''
    Usage:
        $ python add_user.py <username> <password>
        ''')
        sys.exit(0)
    else:
        print()