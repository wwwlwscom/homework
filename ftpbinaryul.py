#!/usr/bin/env python


from ftp import FTP

import sys, getpass, os.path

host, username, localfile, remotepath = sys.argv[1:]
password = getpass.getpass("Enter password for %s on %s: " % (username, host))

f = FTP(host)
f.login(username, password)
f.cwd(remotepath)
fd = open(localfile, 'rb')
f.storbinary('STOR %s' % os.path.basename(localfile), fd)
fd.close()

f.quit()
