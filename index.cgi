#!/usr/local/bin/python2.6
# -*- coding: utf-8 -*-
from whatconf import *

MESSAGE_TEMPLATE="""%(iptext)s%(gmtime)s

A mix named "%(subject)s" was submitted by "%(author)s".

It is at %(message)s"""

FORM_PAGE_TEMPLATE="""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
  <title>Share / submit your mix</title>
  <meta http-equiv="Content-Type" content=
  "text/html; charset=utf-8">
</head>
<body>
<p>
  <b>Share your mix with friends</b><br>
  <a target="_blank" title="Twitter" href="http://twitter.com/home?status=Listen to my SynPhonia mix: %(ugcurl)s"><img border="0" alt="Twitter" width="16" height="16" style="margin: 0pt; vertical-align: middle" src="icon-twitter.png"></a>
  <a target="_blank" title="Facebook" href="http://www.facebook.com/share.php?u=%(ugcurl)s"><img border="0" alt="Facebook" width="16" height="16" style="margin: 0pt; vertical-align: middle" src="icon-facebook.png"></a>
  <a target="_blank" title="Friendfeed" href="http://www.friendfeed.com/share?title=Listen to my SynPhonia mix&amp;link=http://bit.ly/c3R9oO"><img border="0" alt="Friendfeed" width="16" height="16" style="margin: 0pt; vertical-align: middle" src="icon-friendfeed.png"></a>
  <input size="20" value="%(ugcurl)s" onclick="this.select()">
</p>
<hr>
<p>
  <b>Submit your mix to us</b>
  <form name="submit_form" id="submit_form" method="post"
  action="%(scriptname)s">
      <span style="color:#7f0000">%(errorhtml)s</span>
      <p>Name of mix: <input name="subject" id="subject" value="%(subject)s"></p>
      <p>Your nickname: <input name="author" id="author" value="%(author)s"></p>
      <input type="hidden" name="message" value="%(ugcurl)s">
      <input type="hidden" name="ref" value="%(referrer)s">
      <b>To prove you're human and not a spam robot,<br>
      you need to pass the captcha test.</b>
      %(captcha)s
      <input type="submit" value="Send us your mix">
      <input type="button" value="Close window" onclick="window.close()">
  </form>
</p>
</body>
</html>"""

RESPONSE_PAGE_TEMPLATE="""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
  <title>%(title)s</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
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
    msg.add_header('to',SMTP_TO)
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

    form = cgi.FieldStorage()
    ref=form.getvalue('ref',os.environ.get('HTTP_REFERER',''))
    if not ref.startswith(ALLOWED_REFERRER_PREFIX):
        print 'Content-type: text/plain\n\n' # temporary?!?
        print 'Error: Illegal referrer'
        return

    ugcurl=bitly.Api(BITLY_USERNAME,BITLY_API_KEY).shorten(ref)

    print 'Content-type: text/html; charset=utf-8\n\n'
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
        subject=form.getvalue('subject','').strip()
        if not subject:
            errors.append("You didn't give your mix a name.")
        author=form.getvalue('author','').strip()
        if not author:
            errors.append("You didn't write your own name.")
        captcha_response = captcha.submit(
            form.getvalue('recaptcha_challenge_field'),
            form.getvalue('recaptcha_response_field'),
            RECAPTCHA_PRIVATE_KEY,
            os.environ['REMOTE_ADDR'])
        if not captcha_response.is_valid:
            errors.append("You've failed the captcha test. Convince me again that you're not a robot.")
            captcha_error=captcha_response.error_code
        if errors:
            errorhtml='Errors:<ul>%s</ul>' % ('\n'.join(['<li>%s</li>' % e for e in errors]))
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
                title='Message sent'
                response='Thank you for your mix, %s.' % form.getvalue('author')
            except Exception,e:
                title='Message sending failed'
                response='<b>Error:</b> %s' % str(e)
            print RESPONSE_PAGE_TEMPLATE % {'title':title,'response':response,'ref':ref}


if __name__=='__main__':
    webit()
