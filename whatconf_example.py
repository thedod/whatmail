DEBUG_TO_WEB=False # set to True when debugging
SMTP_FROM='myself@gmail.com' # An email address that you're allowed to send from
SMTP_TO=SMTP_FROM # same address, unless you want to send the form somewhere else
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

# You get these two at http://bit.ly/a/your_api_key
BITLY_USER='*******'
BITLY_PASSWORD='*******'
