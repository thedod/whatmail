### The TipWire branch ([see demo](https://swatwt.com/tipwire/))

While Whatmail is a general-purpose contact form script (and gpgme encryption only comes as an option),
TipWire is a special-purpose form intended for communication between a `source` (a casual user) and a `desk`
(a person or a team with enough skills to read gpg mail, and enough resources to run an [etherpad](http://etherpad.org/) server behind SSL).

Note that you should configure the etherpad server in an
"[unorthodox](https://github.com/thedod/whatmail/blob/tipwire/useful-for-etherpad-settings.txt)"
manner for privacy and other reasons.

The [wiki page](https://github.com/thedod/whatmail/wiki/tipwire) is where I [try to] describe the system.
This is also where I document relevant [feedback](https://github.com/thedod/whatmail/wiki/tipwire#criticism-so-far)
I get via the [demo form](https://swatwt.com/tipwire/) or otherwise.

----------------------------

Below you'll find the original README from the master branch of the WhatMail contact form script

----------------------------

### WhatMail by [@TheRealDod](http://twitter.com/TheRealDod)

This is a simple cgi contact form that 
can handle utf-8, which is a crucial feature for me since not all my friends write to me in English :)

It also has a [text captcha](https://github.com/thedod/WinoCaptcha). It's enabled by default but you can 
configure whatmail to either disable it or use Google's [recaptcha](http://pypi.python.org/pypi/recaptcha-client/) instead.
Note that using recaptcha would enable Google to track people who use your form, so this option is mainly here for legacy reasons.

The GUI (big word for a form and a thankyou page) can be skinned with [mustache](http://mustache.github.com/mustache.5.html) templates. The default skin is [twitter bootstrap](http://twitter.github.com/bootstrap/) based, but anything goes, and skin pull-requests are welcome.

If your form is served via SSL, you can also configure it to encrypt the mail it sends with [gpgme](http://www.gnupg.org/related_software/gpgme/) (plain old ascii-armor. not mime). Be careful when you set this up: the illusion of security can easily make you [lose your head](http://simonsingh.net/The_Black_Chamber/maryqueenofscots.html). **Peer review is welcome**.

There's no email address validation and no assumption that such an address is entered at all (friends can leave a name, strangers may decide to leave a phone number instead).
Also note that the identity of the sender can't be verified (even when encryption is enabled, nothing is signed), but the again - your phone doesn't come with prank-call protection either :).
For what it's worth, the sender's ip number is included in the mail you receive.

### Installing

* Run `git submodule update --init` to fetch dependencies.
* Put all files (including .htaccess) in a web-accessible folder.
* Check your .htaccess settings by accessing testcgi.py from web: If you see
  python source, do *not* continue to the next step (creating whatconf.py). This file
  will contain passwords and keys, and you have to make sure it can't be accessible
  from web. If .htaccess doesn't do the trick, show it to your sysadmin and ask to config
  your folder at the apache according to what's written there.
* Optionally, get [recapcha keys](https://www.google.com/recaptcha/admin) for the form's domain.
* copy `whatconf_defaults.py` to `whatconf.py` and edit it. See comments inside the file.
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
* **Note:** You should make sure your gpg homedir and the files in it are only readable by you
  (chmod 700 for the folder and 600 for the files). This can also work on a shared host,
  if the hosting provider has configured cgi scripts to run under _your own_ uid (e.g. at Webfaction).  

  If you're on a shared host where cgi scripts of all users run under _the same_ uid
  (e.g. Apache's `www-data`), **don't** try to chmod the homedir so that www-data has
  rights at the gpg homedir. Better use an unecrypted form, so that your users know
  where they stand :)

### Thanks

Thanks to the authors of all the stuff glued here together:

  * [gnupg](http://www.gnupg.org/), [gpgme](http://www.gnupg.org/related_software/gpgme/)
    and [pygpgme](http://pypi.python.org/pypi/pygpgme/)
  * [mustache](http://mustache.github.com/) and [pystache](https://github.com/defunkt/pystache)
  * [WinoCaptcha](https://github.com/yerich/WinoCaptcha/)
  * [recaptcha](http://pypi.python.org/pypi/recaptcha-client/)
  * [mysender](https://github.com/denever/mysender/)

Special thanks to _Mack_ for peer review.
