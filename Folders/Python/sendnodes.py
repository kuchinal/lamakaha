"""
sendnodes.py

Version 2

Tyler Lockard [lockardvfx@gmail.com] TylerLockard.com
13 September 2013

A tool designed to send selected nodes to an artist quickly and easily
using a predefined email account.


NOTE: You'll have to change the "fromaddr", "username" and "password"
      on lines 31-33 for this to work properly. For security
      sake, make sure it's a dummy account and not your personal
      email since we're storing the password as plain text here.
      If you're not using Gmail, you may also need to tweak the
      server in line 73.
"""

from smtplib import SMTP
from PySide import QtGui
import nuke
import nukescripts



def sendNodes():
    # ----------------------------------------------------------------------------
    # (NOTE: Change this to an email address you have created.)
    fromaddr = 'lamakaha@gmail.com'
    username = 'lamakaha@gmail.com'
    password = 'thedrone'
    # ----------------------------------------------------------------------------

    # Grab the selected nodes and copy to the clipboard.
    try:
        nuke.selectedNodes()
        nuke.nodeCopy(nukescripts.cut_paste_file())
        clipboard = QtGui.QApplication.clipboard()
        clipboard = clipboard.text()
    except:
        nuke.message("You have to select something first. Try clicking and dragging")
        return

    # Grab some input from the user, exit if they pressed cancel
    p = nuke.Panel('Send nodes via email')
    p.addSingleLineInput('To:', 'lamakaha@gmail.com')
    p.addSingleLineInput('Subject:', 'My copied node setup')
    p.addNotepad('Body:', clipboard)
    p.addButton('Cancel')
    p.addButton('Send')
    if p.show() == 0:
        return

    # Exit if we only have the default/example email address
    toaddrs  = p.value('To:')
    if toaddrs == 'example@gmail.com':
        nuke.message("Please provide an email address other than the default example.")
        return

    # Exit if we don't have a message body
    body = p.value('Body:')
    if body == '':
        nuke.message("Please provide a message body.")
        return

    # Format the body to include the subject lines
    body = 'Subject: %s\n\n%s' % (p.value('Subject:'), body)

    # Everything checks out, let's try to send it!
    try:
        server = SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, body)
        server.quit()
        nuke.message('Your nodes have been sent to "%s"!' % toaddrs)
    except:
        nuke.message("Error occured. Couldn't send nodes.")
        nuke.tprint("Error occured. Couldn't send nodes.")
        nuke.tprint(sys.exc_type)
        nuke.tprint(sys.exc_value)

