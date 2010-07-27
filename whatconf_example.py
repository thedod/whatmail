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

# You get these two at http://bit.ly/a/your_api_key
BITLY_USERNAME='*******'
BITLY_API_KEY='*******'

# To avoid cross-site scripting and honest mistakes
# Only allow referrers to come from a specific site (or folder)
# Should end with a / (don't allow example.org.evil.com or /users/me2)
ALLOWED_REFERRER_PREFIX='http://example.org/users/me/'
