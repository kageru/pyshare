# Add credentials for your own users here.
# Since I'll only have very few users (probably just me), using a proper DB is overkill
# The password hash is generated by
# hashlib.sha3_256(bytes((password + salt).encode('utf8'))).hexdigest()

users = {
    'user1': ['c7d9c9621e417ea09141edbac126cd1f3ab1b2b94b2ad3b155a1e26a88b216c0', 'user1salt'],
}

# And btw, the password is just 'password'.
# I'm just saying this because there will be that one guy who actually thinks
# "Oh, I could totally brute-force this password now"
