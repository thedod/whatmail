### WhatMail by [@TheRealDod](http://twitter.com/TheRealDod)

This is a simple cgi contact form that has recaptcha and can handle utf-8.

I always need one, and I always end up writing it again. Never again [I hope].

Uses Recaptcha [client library](http://pypi.python.org/pypi/recaptcha-client) and Denevers [mysender](http://github.com/denever/mysender/) SMTP wrapper (both included).

There's no email address validation and no assumption that such an address is entered at all.
It's not added as a Reply-to header so that I won't reveal my email address by accident.
My friends can leave a name, strangers can leave a phone number, I'm easy :)

Optionally, you can gpg-encrypt the mail (plain old ascii-armor. not mime).
This would require [pygpgme](http://pypi.python.org/pypi/pygpgme/) and some concentration :)

### Installing

* Put all files (including .htaccess) in a web-accessible folder.

* Check your .htaccess settings by accessing testcgi.py from web: If you see
  python source, do *not* continue to the next step (creating whatconf.py). This file
  will contain passwords and keys, and you have to make sure it can't be accessible
  from web. If .htaccess doesn't do the trick, show it to your sysadmin and ask to config
  your folder at the apache according to what's written there.

* copy `whatconf_example.py` to `whatconf.py` and edit it. See comments inside the file.

* That's it. You can now access the folder via web (e.g. `/whatmail/`) and get a contact form.
  Send yourself a message to congratulate yourself.

### Enabling gpg

**Note:** If you decide to enable gpg, make sure the cgi page is served via SSL
(otherwise, it's kinda [daft](http://simonsingh.net/The_Black_Chamber/maryqueenofscots.html)).
If there's an alternative http url that gets to the same cgi script, it is **important** to
supply an `SSL_REDIRECT_TO` at `whatconf.py` (see below).

First thing, you need to make sure you have [gpgme](http://www.gnupg.org/related_software/gpgme/)
and [pygpgme](http://pypi.python.org/pypi/pygpgme/) installed.  
Simply try `import gpgme` from python and see if it works.  
If it doesn't - installing them is beyond the scope of this README file, but it's doable :)

* Create a script-specific gpg homedir. `./.gnupg` is a good idea since it's .gitignored :)
* Export the recepient's pubkey (i.e. yours). E.g. do (on your desktop)
  `gpg -a --export me@example.com > me.asc` and copy the temporary `me.asc` to the server.
* Import the pubkey to the gpg homedir with `gpg --homedir ./.gnupg --import < me.asc`
* Repeat with other pubkeys (if you want to encrypt to multiple recepients).
* Edit `GPG_*` parameters at `whatconf.py` (`GPG_HOMEDIR` should be a full path starting with `/`).
* It is recommended to write your script's SSL url as `SSL_REDIRECT_TO`.
  You **are** using SSL. Right? :)
* If the user running the web server isn't you (e.g. `www-data`), you'll need to setup permissions
  for the gpg homedir (this is why it should be script-specific, especially on shared machines).

  **After** you import the pubkey[s], make sure the web-server user has read/write permission to
  the gpg homedir and all files there [created by the import], **except** for `pubring.pgp`
  where it should only have **read** permissions.

### <a name="rfc"></a>Request for comments:

  Even if web server user (e.g. `www-data`) is not trusted, we can still give it write permissions
  to `secring.pgp` etc. (will be ignored anyway), but what about `random_seed`?
  Isn't it dangerous to let strangers have write permission there?
  OTOH _can_ it be read only? (I know it _can_. Not sure it's a good idea, though).

