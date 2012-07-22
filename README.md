### WhatMail by [@TheRealDod](http://twitter.com/TheRealDod)

This is a simple cgi contact form that has [recaptcha](http://pypi.python.org/pypi/recaptcha-client/)
and can handle utf-8, which is a crucial feature for me since not all my friends write to me in English :)

The GUI (big word for a form and a thankyou page) can be skinned with [mustache](http://mustache.github.com/mustache.5.html) templates. The default skin is [twitter bootstrap](http://twitter.github.com/bootstrap/) based, but anything goes, and skin pull-requests are welcome.

If your form is served via SSL, you can also configure it to encrypt the mail it sends with [gpgme](http://www.gnupg.org/related_software/gpgme/) (plain old ascii-armor. not mime). Be careful when you set this up: the illusion of security can easily make you [lose your head](http://simonsingh.net/The_Black_Chamber/maryqueenofscots.html). [**Peer review is welcome**](#rfc).

There's no email address validation and no assumption that such an address is entered at all (friends can leave a name, strangers may decide to leave a phone number instead).
Also note that the identity of the sender can't be verified (even when encryption is enabled, nothing is signed), but the again - your phone doesn't come with prank-call protection either :).
For what it's worth, the sender's ip number is included in the mail you receive.

### Installing

* do `git submodule update --init` (to get [recaptcha](http://pypi.python.org/pypi/recaptcha-client/)
  and [pystache](https://github.com/defunkt/pystache/)).
* Put all files (including .htaccess) in a web-accessible folder.
* Check your .htaccess settings by accessing testcgi.py from web: If you see
  python source, do *not* continue to the next step (creating whatconf.py). This file
  will contain passwords and keys, and you have to make sure it can't be accessible
  from web. If .htaccess doesn't do the trick, show it to your sysadmin and ask to config
  your folder at the apache according to what's written there.
* copy `whatconf_example.py` to `whatconf.py` and edit it. See comments inside the file.
* That's it. You can now access the folder via web (e.g. `/whatmail/`) and get a contact form.
  Send yourself a message to congratulate yourself.

### Skinning the GUI

* Copy the `skins/default/` folder to [say] `skins/mine/`.
* Edit the [mustache](http://mustache.github.com/mustache.5.html) templates there.
* You can also have static files (css, js, graphics) in the skin's folder.
  In templates, you can refer to that folder as `{{skin}}`
  (e.g. `<img src="{{skin}}/graphics/logo.png">`).
* Change `SKIN_FOLDER` at `whatconf.py` from `skins/default` to `skins/mine`.

Easy.

### Enabling gpg

**Note:** If you decide to enable gpg, make sure the cgi page is served via SSL
(otherwise, it's kinda [daft](http://simonsingh.net/The_Black_Chamber/maryqueenofscots.html)).
If there's an alternative http url that gets to the same cgi script, it is **important** to
supply an `SSL_REDIRECT_TO` at `whatconf.py` (see below).

First thing, you need to make sure you have [gpgme](http://www.gnupg.org/related_software/gpgme/)
and [pygpgme](http://pypi.python.org/pypi/pygpgme/) installed.  
Simply try `import gpgme` from python and see if it works.  
If it doesn't - installing them is beyond the scope of this README file, but it's doable :)

* Create a script-specific gpg homedir (say, `./.gnupg`). If it's inside a web-accessible folder,
  **make sure homedir's name starts with a "."** (and verify that you can't get to files there via web).

* Export the recepient's pubkey (i.e. yours). E.g. do (on your desktop)
  `gpg -a --export me@example.com > me.asc` and upload the temporary `me.asc` to the server.

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

  Even if web server user (e.g. `www-data`) is not trusted, there's no risk in giving it write
  permissions to `secring.pgp` etc. (never used anyway), but what about `random_seed`?
  Isn't it dangerous to let strangers have write permission there?
  OTOH _can_ it be read only? (I know it _can_. Not sure it's a good idea, though).

