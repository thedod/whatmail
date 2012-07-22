#!/usr/bin/env python
# -*- coding: utf-8 -*-
from whatconf import *
import pystache
stache = pystache.Renderer(search_dirs=SKIN_FOLDER,file_encoding='utf-8',string_encoding='utf-8')

def is_ssl(env):
    return env.get('HTTPS','').lower()=='on' or env.get('HTTP_HTTPS','').lower()=='on'

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
    body=stache.render(stache.load_template('message'), {
        'author':author,
        'iptext':ip and ('IP number: %s, ' % ip) or '',
        'gmtime':asctime(gmtime()),
        'subject':subject,
        'message':message,
    }).encode('utf-8')
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
        print stache.render(stache.load_template('form'),{
            'scriptname':scriptname,
            'errorhtml':'',
            'title':PAGE_TITLE,
            'author':'',
            'subject':'',
            'message':'',
            'captchahtml':captcha.displayhtml(RECAPTCHA_PUBLIC_KEY,use_ssl=True),
            'is_encrypted': GPG_ENABLED,
        }).encode('utf-8')
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
            print stache.render(stache.load_template('form'),{
                'scriptname':scriptname,
                'errorhtml':errorhtml,
                'author':author,
                'subject':subject,
                'message':form.getvalue('message',''),
                'captcha':captcha.displayhtml(RECAPTCHA_PUBLIC_KEY,error=captcha_error),
            }).encode('utf-8')
        else:
            try:
                sendit(author=form.getvalue('author'), ip=os.environ['REMOTE_ADDR'],
                    subject=form.getvalue('subject'), message=form.getvalue('message','(empty message)'))
                title='Message sent'
                response='Thank you, %s, for your message.' % form.getvalue('author')
            except Exception,e:
                title='Message sending failed'
                response='<strong>Error:</strong> %s' % str(e)
            print stache.render(stache.load_template('response'),{
                'title':title,'responsehtml':response
            }).encode('utf-8')

if __name__=='__main__':
    webit()
