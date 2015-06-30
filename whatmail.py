#!/usr/bin/env python2
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
    def captcha_html(error_text=None):
        if USE_WINOCAPTCHA:
            from WinoCaptcha import winolib
            return stache.render(stache.load_template('winocaptcha'),winolib.get_question(),error_text=error_text)
        elif USE_PYCAPTCHA:
            from pycaptchalib import captchalib
            return stache.render(stache.load_template('pycaptcha'),captchalib.get_question(),error_text=error_text)
        else:
            return None
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
            'message':'',
            'captchahtml':captcha_html(),
            'is_encrypted': is_encrypted,
        }).encode('utf-8')
    else: # POST
        errors=[]
        author=form.getvalue('author','').strip()
        if not author:
            errors.append(MSG_EMPTY_FROM)
        captcha_error=None
        if USE_WINOCAPTCHA:
            from WinoCaptcha import winolib
            captcha_result = winolib.check_answer(form.getvalue('wino_token','').strip(),form.getvalue('wino_answer','').strip())
            if captcha_result is None: # Either attack or honest mistake (reload, back button)
                errors.append(None) # Fail, but don't show error message
            elif not captcha_result: # Good question, wrong answer :)
                errors.append(MSG_CAPTCHA_FAILED)
                captcha_error=MSG_CAPTCHA_TRY_AGAIN
        elif USE_PYCAPTCHA:
            from pycaptchalib import captchalib
            captcha_result = captchalib.check_answer(form.getvalue('captcha_token','').strip(),form.getvalue('captcha_answer','').strip())
            if captcha_result is None: # Either attack or honest mistake (reload, back button)
                errors.append(None) # Fail, but don't show error message
            elif not captcha_result: # Good question, wrong answer :)
                errors.append(MSG_CAPTCHA_FAILED)
                captcha_error=MSG_CAPTCHA_TRY_AGAIN
        if errors:
            errors = filter(None,errors) # skip empty messages (see winolb.check_answer above)
            errorhtml = errors and '<ul class="error-list">%s</ul>' % ('\n'.join(['<li>%s</li>' % e for e in errors])) or ''
            print stache.render(stache.load_template('form'),{
                'skin':SKIN_FOLDER,
                'scriptname':scriptname,
                'title':PAGE_TITLE,
                'errorhtml':errorhtml,
                'author':author,
                'message':form.getvalue('message',''),
                'captchahtml':captcha_html(error_text=captcha_error),
                'is_encrypted': GPG_ENABLED,
            }).encode('utf-8')
        else:
            try:
                try: # create subject lines one can distinguish between ;)
                    from WinoCaptcha import winolib
                    subject = winolib.get_question()['question'].split('.',1)[0]
                except:
                    subject = 'Form submission'
                sendit(author=form.getvalue('author'), ip=os.environ['REMOTE_ADDR'],
                    subject=subject, message=form.getvalue('message','(empty message)'))
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
