import MySQLdb
import time
import os
import signal
from subprocess import check_output, Popen

db = MySQLdb.connect(user='xss', password='AoL5anga', db='superblog')
c = db.cursor()
while True:
    c.execute('COMMIT')
    c.execute('SELECT id, url FROM blog_feedback WHERE not visited ORDER BY created_at ASC LIMIT 1')
    feedback = c.fetchone()

    # print 'Got feedback: %r' % (feedback,)
    if feedback is None:
        time.sleep(1)
        continue
    id, url = feedback

    c.execute('COMMIT')
    c.execute('UPDATE blog_feedback SET visited = 1 WHERE id = %s', (id,))
    c.execute('COMMIT')

    if not url.startswith('http://') or url.startswith('https://'):
        print 'Invalid scheme for URL %r' % url
        continue
    print 'Processing URL %r' % url
    p = Popen(["python2", "/bot/chrome.py", url],preexec_fn=os.setsid)
    pgid = os.getpgid(p.pid)

    try:
        p.communicate()
    except:
        print 'p.communicate failed'

    try:
        os.killpg(pgid, signal.SIGKILL)
    except:
        print 'os.killpg failed'

    print 'Done processing URL %r' % url
