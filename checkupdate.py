#!/usr/bin/python

import urllib
import smtplib
import shelve
import logging

dbpath = '/home/ypcat/cgi-bin/notify.db'
logpath = '/home/ypcat/cgi-bin/checkupdate.log'
sender = 'ypcat@eumacro.csie.org'

db = shelve.open(dbpath, writeback=True)
logging.basicConfig(filename=logpath, level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%c')

for name, site in db['sites'].items():
    r = urllib.urlopen(site['url'])
    if 'etag' not in site or not site['etag']:
        site['etag'] = r.headers['etag']
        logging.info('init %s with etag %s' % (name, site['etag']))
    elif site['etag'] != r.headers['etag']:
        site['etag'] = r.headers['etag']
        smtplib.SMTP('localhost').sendmail(sender, site['subscribers'].keys(), 'Subject: %s updated\n\nvisit %s' % (name, site['url']))
        logging.info('%s updated with etag %s' % (name, site['etag']))
        logging.info('sent notification to %s' % ', '.join(site['subscribers'].keys()))
    else:
        logging.info('%s unmodified' % name)

db.close()

