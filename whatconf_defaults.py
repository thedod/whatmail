# -*- coding: utf-8 -*-
DEBUG_TO_WEB=False # set to True when debugging
PAGE_TITLE='Request a TipWire chat'
PAGE_SUBTITLE='Warning: insecure instance!' # html is allowed here
SECURE_PAGE_SUBTITLE='[<strong>Warning: experimental</strong>] Initiate a secure chat with us' # subtitle when both gpg and ssl are on. html allowed.
SMTP_FROM='myself@gmail.com' # An email address that you're allowed to send from
SMTP_TOS=['me@home.org','gang@work.com'] # list of recepients
SMTP_HOST='smtp.gmail.com' # This is for gmail, depends on your mail provider
SMTP_PORT=587 # usually 587
SMTP_KEYFILE=None # If you know what it is, you know what to put there
SMTP_CERTFILE=None # Ditto
SMTP_USERNAME=SMTP_FROM # for gmail (and usually), SMTP_FROM is what you need
SMTP_PASSWORD='*******'
SUBJECT_PREFIX='[TipWire] ' # subject line prefix. good for mail filters
PAD_ID_PREFIX='https://piratenpad.de/p'
PAD_ID_MINCHARS=32

### Use winograd text captcha
# set to false if you want no captcha (or recaptcha)
USE_WINOCAPTCHA=True

### You get these two at https://www.google.com/recaptcha/admin
# RECAPTCHA_PUBLIC_KEY='****************'
# RECAPTCHA_PRIVATE_KEY='***************'
### But you don't have to use recaptcha (what they don't know, won't hurt you :) )
RECAPTCHA_PUBLIC_KEY=None
RECAPTCHA_PRIVATE_KEY=None

# Folder containing mustache templates
SKIN_FOLDER='skins/default'
## ובעברית...
#!!!!! Not TipWire-ready yet
#SKIN_FOLDER='skins/hebrew'

# Messages
MSG_SHORT_PAD_ID = "Pad-id should be at least {0} characters long.".format(PAD_ID_MINCHARS)
MSG_BAD_SLUG = 'Pad-id should only contain letters, digits, "-", and "_".'
MSG_PAD_ID_MISMATCH = "You should enter the same pad-id in both fields."
MSG_CAPTCHA_FAILED="You've failed the captcha test. Convince me again that you're not a robot."
MSG_CAPTCHA_TRY_AGAIN="Try to get it right this time :)"
MSG_SUCCESS_TITLE="Chat request sent"
MSG_FAIL_TITLE="Mesage sending failed"

## ובעברית...
#MSG_EMPTY_FROM="לא הכנסת פרטי יצירת קשר"
#MSG_CAPTCHA_FAILED="לא הצלחת להוכיח שאת/ה לא רובוט :)"
#MSG_CAPTCHA_TRY_AGAIN="עכשיו ברצינות ;)"
#MSG_SUCCESS_TITLE="ההודעה נשלחה"
#MSG_FAIL_TITLE="תקלה בשליחת ההודעה"

### gnupg (see README for details)
GPG_ENABLED=False # Enable if you have gpgme and know how to conf this
# This should work for most sane people:
GPG_ENCRYPT_TO=SMTP_TOS
# If you want to get tricky, this would also work:
# GPG_ENCRYPT_TO=['0x......','someone@else.com']

# GPG_HOMEDIR should be a whatmail-specific gpg dir.
# import all GPG_ENCRYPT_TO pubkeys there. E.g. like this:
# gpg --homedir '/path/to/.gnupg' --import < mypub.asc
# Make sure that the user running the web server (e.g. www-data) has sufficient
# permissions at GPG_HOMEDIR (if you get "Error: (7, 16383, u'End of file')" it's
# either permissions, or you forgot to import a GPG_ENCRYPT_TO pubkey).
GPG_HOMEDIR='/path/to/.gnupg'

# REDIRECT_TO_SSL should be an https:// url or you'll loop
# REDIRECT_TO_SSL='https://secure.example.com/path/to/whatmail/'
REDIRECT_TO_SSL=''
