DEBUG_TO_WEB=False # set to True when debugging
SMTP_FROM='myself@gmail.com' # An email address that you're allowed to send from
SMTP_TOS=['me@home.org','gang@work.com'] # list of recepients
SMTP_HOST='smtp.gmail.com' # This is for gmail, depends on your mail provider
SMTP_PORT=587 # usually 587
SMTP_KEYFILE=None # If you know what it is, you know what to put there
SMTP_CERTFILE=None # Ditto
SMTP_USERNAME=SMTP_FROM # for gmail (and usually), SMTP_FROM is what you need
SMTP_PASSWORD='*******'
SUBJECT_PREFIX='[whatmail] ' # subject line prefix. good for mail filters

# You get these two at http://recaptcha.net/api/getkey
RECAPTCHA_PUBLIC_KEY='****************'
RECAPTCHA_PRIVATE_KEY='***************'

### gnupg (you need https://launchpad.net/pygpgme or apt-get python-gpgme)
GPG_ENABLED=False # Enable if you have gpgme and know how to conf this
GPG_ENCRYPT_TO=['0x......'] # your key(s) here

# GPG_HOMEDIR should be a whatmail-specific gpg dir.
# import all GPG_ENCRYPT_TO pubkeys there. E.g. like this:
# gpg -a --export 'me@example.com' | gpg --homedir '/path/to/.gnupg' --import
# If you're getting 'enf of file' errors, check whether the user running the
# Make sure that the user running the web server (e.g. www-data) has sufficient
# permissions at GPG_HOMEDIR (if you get a bogus "end of file" error, it's either
# permissions, or you forgot to import an pubkey).
GPG_HOMEDIR='/path/to/.gnupg'
