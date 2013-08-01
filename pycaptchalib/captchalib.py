"""Usage:
        >>> q = captchalib.get_question()
        >>> [(k,q[k]) for k in q if k!='imgsrc'] # imgsrc is too long to watch: it's the whole image in base-64 as a "data:" uri
        [('imgheight', 96), ('token', '51fa535asgndRItwZHV0jxENTC0WFYR12iuCdpV4j3Pu8vBN8'), ('imgwidth', 256)]
        >>> file('test.html','w').write('<img src="{0}">'.format(q['imgsrc'])) # now we can watch test.html in a browser
        >>> captchalib.check_answer(q['token'],'noise') # right answer
        True
        >>> `captchalib.check_answer(q['token'],'noise')` # replay attempt
        'None'
        >>> captchalib.check_answer(q['token'],'wrong by definition') # wrong answer
        False
        >>> `captchalib.check_answer(q['token'],'trying something else')` # replay attempt
        'None'
When None is returned, app should fail (e.g. show the form agai), but not display a "captcha failed" message,
since this could either be a replay attack or a benign accident ('reload' or 'back' buttons)
"""
### This lib is 90% a shameless copy/paste from WinoCaptcha/winolib
### TODO(?) make this a pluggable thing
LIBDIR = '/' in __file__ and __file__.rsplit('/',1)[0] or '.'
MAX_CHALLENGES = 529 # Feel free to increase if you're popular or under a DoS attack :)
DBPATH = '/'.join([LIBDIR,'challenges.db'])

import shelve,random,re,os,time,StringIO
from Captcha.Visual.Tests import PseudoGimpy

_RE_NONALPHANUM=re.compile('[^a-zA-Z0-9]+')
def _gen_token(): # monotonic yet unpredictable
    return hex(int(time.time()))[2:]+_RE_NONALPHANUM.sub('',random._urandom(32).encode('base64'))

def _register_challenge(dbpath,answer):
    token = _gen_token()
    db = shelve.open(dbpath)
    db[token] = map(lambda s:s.lower(),answer) # be nice and case-insensitive
    db.sync()
    keys = sorted(db.keys())
    if len(keys)>MAX_CHALLENGES:
        for k in keys[:len(keys)-MAX_CHALLENGES]: # Trim old entries
            try:
                del db[k]
            except KeyError:
                pass
    db.close()
    return token

def _check_response(dbpath,token):
    db = shelve.open(dbpath)
    a = db.get(token)
    if a:
        try:
            del db[token]
        except KeyError:
            pass
    db.close()
    return a
    
def get_question(winograd_source='winograd.txt',dbpath=DBPATH):
    """Returns a  question, and a token that can be used to check the user's answer.
This token can't be reused (to avoid a replay attack)"""
    g = PseudoGimpy()
    i = g.render()
    w,h = i.getbbox()[2:]
    buff = StringIO.StringIO()
    i.save(buff,'png')
    return {
        'token':_register_challenge(dbpath,g.solutions),
        'imgsrc':'data:image/png;base64,'+buff.getvalue().encode('base64'),
        'imgwidth':w,'imgheight':h}

def check_answer(token,answer,dbpath=DBPATH):
    """Fetches the token's challenge from the db. If it exists, removes it from the db and verifies the user's answer.
Returns True/False if answer was right/wrong, None if token wasn't in the db.
The None result does not necessarily mean it's an attack. This could still be accidental (user hit reload or back button).
When None is returned, app should fail, but not display a "captcha error" message."""
    a = _check_response(dbpath,token)
    if a:
        return answer.lower() in a # True or False
    else: # Either attack or accidental (user hit reload or back button)
        return None # App should fail, but not show "captcha error"
