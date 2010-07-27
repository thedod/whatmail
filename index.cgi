#!/usr/local/bin/python2.6
# -*- coding: utf-8 -*-
from whatconf import *

MESSAGE_TEMPLATE="""%(iptext)s%(gmtime)s

A mix named "%(subject)s" was submitted by "%(author)s".

It is at %(message)s"""

FORM_PAGE_TEMPLATE="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <title>Share / submit your mix</title>
  <meta http-equiv="Content-Type" content=
  "text/html; charset=utf-8">
  <link rel="stylesheet" href="stylee.css" type="text/css" />
</head>
<body>
<div>
  <strong>Share your mix with friends</strong><br/>
  <a target="_blank" title="Twitter" href="http://twitter.com/home?status=Listen to my SynPhonia mix: %(ugcurl)s"><img border="0" alt="Twitter" width="16" height="16" class="share-icon" src="icon-twitter.png"/></a>
  <a target="_blank" title="Facebook" href="http://www.facebook.com/share.php?u=%(ugcurl)s"><img border="0" alt="Facebook" width="16" height="16" class="share-icon" src="icon-facebook.png"/></a>
  <a target="_blank" title="Friendfeed" href="http://www.friendfeed.com/share?title=Listen to my SynPhonia mix&amp;link=http://bit.ly/c3R9oO"><img border="0" alt="Friendfeed" width="16" height="16" class="share-icon" src="icon-friendfeed.png"/></a>
  <input size="20" value="%(ugcurl)s" readonly="readonly" onclick="this.select()">
</div>
<hr>
<div>
  <form name="ugc_submission_form" id="ugc_submission_form" method="POST"
  action="%(scriptname)s">
      <strong>Submit your mix to us</strong><br/>
      %(errorhtml)s
      <em>Your [nick]name:</em> <input name="author" id="author" value="%(author)s"><br/>
      <em>A name for your mix:</em> <input name="subject" id="subject" value="%(subject)s"><br/>
      <input type="hidden" name="message" value="%(ugcurl)s">
      <input type="hidden" name="ref" value="%(referrer)s">
      <em>To prove you're human and not a spam robot,<br/>
      you need to pass the captcha test:</em>
      %(captcha)s
      <input type="submit" value="Send us your mix">
      <input type="button" value="Close window" onclick="window.close()">
  </form>
</div>
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
  <p>%(response)s</p>
  <input type="button" value="Close window" onclick="window.close()">
</body>
</html>"""

def sendit(host = SMTP_HOST, port=SMTP_PORT,
           keyfile = SMTP_KEYFILE, certfile = SMTP_CERTFILE,
           username = SMTP_USERNAME, password = SMTP_PASSWORD,
           author = "A guy who knows a guy",
           ip = None,
           subject = "Testing multilingual subject line כלומר זה רב שפתי בדבר הזה",
           message = "This is in English,\r\nוזה בעברית"):
    """Sends email."""
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
    try:
        scriptname=os.environ['SCRIPT_NAME']
    except: 
        raise Exception,'Program should run as a cgi'
    if DEBUG_TO_WEB:
        import cgitb; cgitb.enable()

    from recaptcha.client import captcha
    from bitly import bitly

    print 'Content-type: text/html; charset=utf-8\n\n'
    form = cgi.FieldStorage()
    ref=form.getvalue('ref',os.environ.get('HTTP_REFERER',''))
    if not ref.startswith(ALLOWED_REFERRER_PREFIX):
        print RESPONSE_PAGE_TEMPLATE % {
            'title':'How did you get here?','response':'Your browser must have lost its way :)'}
        return

    ugcurl=bitly.Api(BITLY_USERNAME,BITLY_API_KEY).shorten(ref)

    if os.environ['REQUEST_METHOD']=='GET':
        print FORM_PAGE_TEMPLATE % {
            'scriptname':scriptname,
            'ugcurl':ugcurl,
            'referrer':ref,
            'errorhtml':'',
            'author':'',
            'subject':'',
            'captcha':captcha.displayhtml(RECAPTCHA_PUBLIC_KEY),
      }
    else: # POST
        errors=[]
        captcha_error=''
        author=form.getvalue('author','').strip()
        if not author:
            errors.append("You didn't write your own name.")
        subject=form.getvalue('subject','').strip()
        if not subject:
            errors.append("You didn't give your mix a name.")
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
                'ugcurl':ugcurl,
                'referrer':ref,
                'author':author,
                'subject':subject,
                'message':form.getvalue('message',''),
                'captcha':captcha.displayhtml(RECAPTCHA_PUBLIC_KEY,error=captcha_error),
            }
        else:
            try:
                sendit(author=form.getvalue('author'), ip=os.environ['REMOTE_ADDR'],
                    subject=form.getvalue('subject'), message=form.getvalue('message','(empty message)'))
                title='Your mix was submitted'
                response='Thank you for your mix, %s.' % form.getvalue('author')
            except Exception,e:
                title='Message sending failed'
                response='<em>Error:</em> %s' % str(e)
            print RESPONSE_PAGE_TEMPLATE % {'title':title,'response':response,'ref':ref}


if __name__=='__main__':
    webit()
