#! /usr/bin/env python
# -*- Python -*-
# Source: https://github.com/denever/mysender/
###########################################################################
#                   MySender - A simple SMTP client                       #
#                        --------------------                             #
#  copyright         (C) 2006, 2007, 2008  Giuseppe "denever" Martino     #
#  email                : martinogiuseppe@gmail.com                       #
###########################################################################
###########################################################################
#                                                                         #
#   This program is free software; you can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License as published by  #
#   the Free Software Foundation; either version 2 of the License, or     #
#   (at your option) any later version.                                   #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with this program; if not, write to the Free Software            #
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA#
#                                                                         #
###########################################################################

import sys
import smtplib
import email
import os
import ConfigParser

from string import join, split, rstrip
from email.MIMEText import MIMEText
from email.Utils import getaddresses

def send(msg, smtpurl, port, keyfile, certfile, username, password):
	srcaddr = getaddresses(msg.get_all('From',[]))
	tos = msg.get_all('to',[])
	ccs = msg.get_all('cc',[])
	bccs = msg.get_all('bcc',[])
	resent_tos = msg.get_all('resent-to',[])
	resent_ccs = msg.get_all('resent-cc',[])
	toaddrlist = getaddresses(tos + ccs + bccs + resent_tos + resent_ccs)

	destaddr = []
	for (name, addr) in toaddrlist:
		if not (addr in destaddr):
			destaddr.append(addr)
	del msg['Bcc']

	client = smtplib.SMTP()
	client.set_debuglevel(2)
	client.connect(smtpurl, port)
	client.ehlo()

	if keyfile and certfile:
		client.starttls(keyfile, certfile)
	else:
		client.starttls()

	client.ehlo()

	if username and password:
		client.login(username, password)
		
	client.sendmail(srcaddr[0][1], destaddr, rstrip(msg.as_string()))
	client.quit()

	#out = open('/home/denever/mail/logs/sender.log', "a")
	#log = "\nId: "+msg['message-id']
	#log += "\tTo:"+join(destaddr)
	#log += "\tDate: "+msg['date']
	#log += "\tSub: "+msg['subject']
	#log += "\nUsing: " + smtpurl 
	#out.write(log)
	#out.close()

def main():
	fileconf = os.path.expanduser('~/.mysender.conf')
	conf = ConfigParser.ConfigParser()
	conf.readfp(open(fileconf))

	msg = email.message_from_file(sys.stdin)
	srcaddr = getaddresses(msg.get_all('From',[]))

	(user, account) = split(srcaddr[0][1],'@')
	
	host = conf.get(account, 'host')
	port = conf.getint(account, 'port')
	
	keyfile = str()
	if conf.has_option(account, 'keyfile'):
		keyfile = conf.get(account, 'keyfile')

	certfile = str()
	if conf.has_option(account, 'certfile'):
		certfile = conf.get(account, 'certfile')

	username = str()
	if conf.has_option(account, 'username'):
		username = conf.get(account, 'username')
		
	password = str()
	if conf.has_option(account, 'password'):
		password = conf.get(account, 'password')

	send(msg, host, port, keyfile, certfile, username, password)

if __name__ == '__main__':
    sys.exit(main())


