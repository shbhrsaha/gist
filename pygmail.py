import re
import imaplib, smtplib

import email
from email.message import *

from datetime import *

import quopri # for MIME encoding/decoding

class pygmail:
    
    def __init__(self):
        self.IMAP_SERVER='imap.gmail.com'
        self.IMAP_PORT=993
        self.M = None
        self.response = None
        self.mailboxes = []
        
        self.user_email = None
    
    # =============== AUTHENTICATION =============== #
    
    def login(self, username, password):
        
        self.user_email = username
        
        # Start IMAP Session
        self.M = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
        rc, self.response = self.M.login(username, password)
        return rc
    
    def logout(self):
        self.M.logout()
    
    # =============== MESSAGES =============== #
    
    # get all unread messages in this mailbox
    # returns list of Python Email Message objects
    def fetchUnreadMessages(self, folder="Inbox"):
        
        messages = []
        
        self.M.select(folder, readonly=True)

        result, data = self.M.uid('search', None, 'UNSEEN')
        uid_list = data[0].split()
        
        for i in range(len(uid_list)):
            email_uid = uid_list[i]
            res, dat = self.M.uid('fetch', email_uid, '(RFC822)')
            raw_email = dat[0][1]
            msg = email.message_from_string(raw_email)
            messages.append(msg)

        messages.reverse() # to put most recent first
        
        return messages