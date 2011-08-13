
from optparse import OptionParser
import random, smtplib, sys, time, urllib
import sqlite3, email, math, imaplib
from dateutil.parser import parse
from datetime import timedelta
import json

import re
inputarg = 10
if len(sys.argv) >= 2:
    inputarg = sys.argv[1]

def get_top_senders(num):
    conn = sqlite3.connect('../mail.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    try:
        email_list = ["'%yahoo%'", "'%gmail%'", "'%aol%'", "'%hotmail%'", "'%live.com%'"]
        emailStr = "and (email like " + " or email like ".join(email_list) + ")"
        execCode = 'select email, count(*) as c from msgs, contacts where msgs.fr = contacts.id %s group by email order by c desc limit %d;' % (emailStr, num)
        res = c.execute(execCode)
        res.fetchone()
        res = res.fetchall()
    except Exception, e:
        print >> sys.stderr, e
        res = None
    total = 0
    emails = []
    numbers = []
    for item in res:
        total += int(item[1])
        emails.append(item[0])
        numbers.append(item[1])
    for item in res:
        length = float(item[1]) / float(total) * 100
        print "%35s %9s %s" % (item[0], item[1], "*"*int(length))
    return emails, numbers



obj = dict()

myemails, mynumbers = get_top_senders(int(inputarg))

obj["x"] = myemails
obj["y"] = mynumbers

print json.dumps(obj)

