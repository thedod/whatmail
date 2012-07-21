#!/usr/bin/env python
# -*- coding: utf-8 -*-
from whatconf import *

MESSAGE_TEMPLATE="""%(iptext)s%(gmtime)s
Message from %(author)s

Subject: %(subject)s

%(message)s"""

FORM_PAGE_TEMPLATE="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <title>%(title)s</title>
  <meta http-equiv="Content-Type" content=
  "text/html; charset=utf-8">
  <link rel="stylesheet" href="stylee.css" type="text/css" />
</head>
<body>
  <form class="feedback-form" name="feedback_form" id="feedback_form" method="post"
        action="%(scriptname)s">
    <div class="captcha">
      <strong>To prove you're not a spam robot,<br/>
      you need to pass the captcha test.</strong>
      %(captcha)s
    </div>
    <h3>%(title)s</h3>
    <p>Stuff in <strong>bold</strong> is mandatory. International text כמו עברית is OK.</p>
      %(errorhtml)s
      <div class="field-wrapper">
          <div class="field-label"><strong>Name and/or email:</strong></div>
          <input class="field" size="20" name="author" id="author" value="%(author)s">
      </div>
      <div class="field-wrapper">
          <div class="field-label"><strong>subject:</strong></div>
          <input class="field" size="30" name="subject" id="subject" value="%(subject)s">
      </div>
      <div class="field-wrapper">
        <td colspan="2">
          <p>Message%(maybegpgtext)s:<br/>
          <textarea class="field" cols="90" rows="8" name="message" id=
          "message">%(message)s</textarea></p>
          <p><input type="submit" value="Send"></p>
      </div>
  </form>
  <a target="_blank" href="https://github.com/thedod/whatmail/"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png" alt="Fork me on GitHub"></a>
</body>
</html>"""

RESPONSE_PAGE_TEMPLATE="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <title>%(title)s</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <link rel="stylesheet" href="stylee.css" type="text/css" />
</head>
<body>
  <h2>%(title)s</h2>
  %(response)s
</body>
</html>"""

def is_ssl(env):
    return env.get('HTTPS').lower()=='on' or env.get('HTTP_HTTPS').lower()=='on'

def sendit(host = SMTP_HOST, port=SMTP_PORT,
           keyfile = SMTP_KEYFILE, certfile = SMTP_CERTFILE,
           username = SMTP_USERNAME, password = SMTP_PASSWORD,
           author = "A guy who knows a guy",
           ip = None,
           subject = "Testing multilingual subject line כלומר זה רב שפתי בדבר הזה",
           message = "This is in English,\r\nוזה בעברית"):
    """Sends email."""
    if GPG_ENABLED:
        import gpgme
        from StringIO import StringIO
        c=gpgme.Context()
        c.set_engine_info(c.protocol,None,GPG_HOMEDIR)
        c.armor=True
        keys=[c.get_key(a) for a in GPG_ENCRYPT_TO]
        cipher=StringIO()
        c.encrypt(keys,gpgme.ENCRYPT_ALWAYS_TRUST,StringIO(message),cipher)
        message=cipher.getvalue()
    from email.header import Header
    from email.mime.text import MIMEText
    from mysender import send
    from time import asctime,gmtime
    body=MESSAGE_TEMPLATE % {
        'author':author,
        'iptext':ip and ('IP number: %s, ' % ip) or '',
        'gmtime':asctime(gmtime()),
        'subject':subject,
        'message':message,
    }
    msg=MIMEText(body,'plain','utf-8')
    msg.add_header('from',SMTP_FROM)
    for addr in SMTP_TOS:
        msg.add_header('to',addr)
    msg.add_header('subject',Header(SUBJECT_PREFIX+subject,'utf-8').encode())
    send(msg, host, port, keyfile, certfile, username, password)

def webit():
    import os,cgi
    from exceptions import Exception
    from recaptcha.client import captcha
    try:
        scriptname=os.environ['SCRIPT_NAME']
    except: 
        raise Exception,'Program should run as a cgi'
    if DEBUG_TO_WEB:
        import cgitb; cgitb.enable()
    if REDIRECT_TO_SSL and not is_ssl(os.environ):
        print 'Location: %s\n' % REDIRECT_TO_SSL
        return
    print 'Content-type: text/html; charset=utf-8\n'
    form = cgi.FieldStorage()
    if os.environ['REQUEST_METHOD']=='GET':
        print FORM_PAGE_TEMPLATE % {
            'scriptname':scriptname,
            'errorhtml':'',
            'title':PAGE_TITLE,
            'author':'',
            'subject':'',
            'message':'',
            'maybegpgtext':
                GPG_ENABLED and ' (do <strong>not</strong> write secrets or passwords anywhere else)' or '',
            'captcha':captcha.displayhtml(RECAPTCHA_PUBLIC_KEY),
      }
    else: # POST
        errors=[]
        captcha_error=''
        author=form.getvalue('author','').strip()
        if not author:
            errors.append("Empty name/email. I need to know how to get back to you.")
        subject=form.getvalue('subject','').strip()
        if not subject:
            errors.append("Empty subject line. Tell me what it's about.")
        captcha_response = captcha.submit(
            form.getvalue('recaptcha_challenge_field'),
            form.getvalue('recaptcha_response_field'),
            RECAPTCHA_PRIVATE_KEY,
            os.environ['REMOTE_ADDR'])
        if not captcha_response.is_valid:
            errors.append("You've failed the captcha test. Convince me again that you're not a robot.")
            captcha_error=captcha_response.error_code
        if errors:
            errorhtml='<ul class="error-list">%s</ul>' % ('\n'.join(['<li>%s</li>' % e for e in errors]))
            print FORM_PAGE_TEMPLATE % {
                'scriptname':scriptname,
                'errorhtml':errorhtml,
                'author':author,
                'subject':subject,
                'message':form.getvalue('message',''),
                'captcha':captcha.displayhtml(RECAPTCHA_PUBLIC_KEY,error=captcha_error),
            }
        else:
            try:
                sendit(author=form.getvalue('author'), ip=os.environ['REMOTE_ADDR'],
                    subject=form.getvalue('subject'), message=form.getvalue('message','(empty message)'))
                title='Message sent'
                response='Thank you, %s, for your message.' % form.getvalue('author')
            except Exception,e:
                title='Message sending failed'
                response='<strong>Error:</strong> %s' % str(e)
            print RESPONSE_PAGE_TEMPLATE % {'title':title,'response':response}


if __name__=='__main__':
    webit()
