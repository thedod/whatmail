#!/usr/bin/env python
# -*- coding: utf-8 -*-
from whatconf_defaults import *
from whatconf import *
import pystache
stache = pystache.Renderer(
    search_dirs=SKIN_FOLDER,file_encoding='utf-8',string_encoding='utf-8',file_extension='html')

def is_ssl(env):
    return env.get('HTTPS','').lower()=='on' or env.get('HTTP_HTTPS','').lower()=='on'

def sendit(host = SMTP_HOST, port=SMTP_PORT,
           keyfile = SMTP_KEYFILE, certfile = SMTP_CERTFILE,
           username = SMTP_USERNAME, password = SMTP_PASSWORD,
           author = "nobody",
           ip = None,
           subject = "no subject",
           message = "no message"):
    """Sends email."""
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
    if GPG_ENABLED:
        import gpgme
        from StringIO import StringIO
        c=gpgme.Context()
        c.set_engine_info(c.protocol,None,GPG_HOMEDIR)
        c.armor=True
        keys=[c.get_key(a) for a in GPG_ENCRYPT_TO]
        cipher=StringIO()
        c.encrypt(keys,gpgme.ENCRYPT_ALWAYS_TRUST,StringIO(body),cipher)
        body=cipher.getvalue()
    msg=MIMEText(body,'plain','utf-8')
    msg.add_header('from',SMTP_FROM)
    for addr in SMTP_TOS:
        msg.add_header('to',addr)
    msg.add_header('subject',Header(SUBJECT_PREFIX+subject,'utf-8').encode())
    send(msg, host, port, keyfile, certfile, username, password)

def webit():
    import os,cgi
    from exceptions import Exception
    if RECAPTCHA_PUBLIC_KEY:
        from recaptcha.client import captcha
    try:
        scriptname=os.environ['SCRIPT_NAME']
    except: 
        raise Exception,'Program should run as a cgi'
    if DEBUG_TO_WEB:
        import cgitb; cgitb.enable()
    is_encrypted = False
    if is_ssl(os.environ):
        is_encrypted = GPG_ENABLED
    elif REDIRECT_TO_SSL:
        print 'Location: %s\n' % REDIRECT_TO_SSL
        return
    print 'Content-type: text/html; charset=utf-8\n'
    form = cgi.FieldStorage()
    if os.environ['REQUEST_METHOD']=='GET':
        print stache.render(stache.load_template('form'),{
            'skin':SKIN_FOLDER,
            'scriptname':scriptname,
            'errorhtml':'',
            'title':PAGE_TITLE,
            'subtitle':is_encrypted and SECURE_PAGE_SUBTITLE or PAGE_SUBTITLE,
            'author':'',
            'subject':'',
            'message':'',
            'captchahtml':RECAPTCHA_PUBLIC_KEY and captcha.displayhtml(RECAPTCHA_PUBLIC_KEY,use_ssl=True) or None,
            'is_encrypted': is_encrypted,
        }).encode('utf-8')
    else: # POST
        errors=[]
        author=form.getvalue('author','').strip()
        if not author:
            errors.append(MSG_EMPTY_FROM)
        subject=form.getvalue('subject','').strip()
        if not subject:
            errors.append(MSG_EMPTY_SUBJECT)
        if RECAPTCHA_PUBLIC_KEY:
            captcha_error=''
            captcha_response = captcha.submit(
                form.getvalue('recaptcha_challenge_field'),
                form.getvalue('recaptcha_response_field'),
                RECAPTCHA_PRIVATE_KEY,
                os.environ['REMOTE_ADDR'])
            if not captcha_response.is_valid:
                errors.append(MSG_CAPTCHA_FAILED)
                captcha_error=captcha_response.error_code
        if errors:
            errorhtml='<ul class="error-list">%s</ul>' % ('\n'.join(['<li>%s</li>' % e for e in errors]))
            print stache.render(stache.load_template('form'),{
                'skin':SKIN_FOLDER,
                'scriptname':scriptname,
                'title':PAGE_TITLE,
                'errorhtml':errorhtml,
                'author':author,
                'subject':subject,
                'message':form.getvalue('message',''),
                'captchahtml':
                    RECAPTCHA_PUBLIC_KEY and captcha.displayhtml(RECAPTCHA_PUBLIC_KEY,use_ssl=True,error=captcha_error) or None,
                'is_encrypted': GPG_ENABLED,
            }).encode('utf-8')
        else:
            try:
                sendit(author=form.getvalue('author'), ip=os.environ['REMOTE_ADDR'],
                    subject=form.getvalue('subject'), message=form.getvalue('message','(empty message)'))
                print stache.render(stache.load_template('success'),{
                    'skin':SKIN_FOLDER,
                    'title':MSG_SUCCESS_TITLE,
                    'sender':form.getvalue('author'),
                    'subject':form.getvalue('subject')
                }).encode('utf-8')
            except Exception,e:
                print stache.render(stache.load_template('fail'),{
                    'skin':SKIN_FOLDER,
                    'title':MSG_FAIL_TITLE,
                    'error': DEBUG_TO_WEB and str(e) or str(type(e))
                }).encode('utf-8')

if __name__=='__main__':
    webit()
