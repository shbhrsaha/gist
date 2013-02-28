import cmd, getpass, webbrowser

from pygmail import *

class Gist(cmd.Cmd):
    
    def do_login(self, line):
        
        emails = ['example@gmail.com', 'example2@gmail.com']
        
        self.accounts = []
    
        print "Authenticating accounts..."
        
        for email in emails:
            g = pygmail()
            password = getpass.getpass("Password for "+email.upper()+": ")
            g.login(email,password)
            self.accounts.append(g)
        
        print "Done"
    
    
    def do_go(self, line):
    
        print ""
        print ""
        
        for g in self.accounts:
    
            print "UNREAD MESSAGES FOR " + g.user_email.upper()
            print "="*124
            
            messages = g.fetchUnreadMessages()

            for msg in messages:
                
                msgFromArray = email.utils.parseaddr(msg['From'])
                
                if msgFromArray[0] != "":
                    msgFrom = msgFromArray[0]
                else:
                    msgFrom = msgFromArray[1]
                
                msgSubject = msg['Subject']
                
                msgDate = ""
                
                date_str = msg['Date']
                date_tuple = email.utils.parsedate_tz(date_str)
                if date_tuple:
                    date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                if date:
                    msgDate = date.strftime("%A %B %d")
                
                print msgFrom.ljust(30) + msgSubject.ljust(75) + msgDate

            print ""
            print ""

    def do_open(self, number):
        
        url = "https://mail.google.com/mail/u/"+number+"/#inbox"
        webbrowser.open_new(url)

    def do_quit(self, line):
        return True
    
    def postloop(self):
        print

if __name__ == '__main__':

    print ""
    print ""
    print "="*124
    print "WELCOME TO GIST!"
    print "GIST is the fastest way to check multiple Gmail inboxes for unread messages."
    print "Type 'login' to authenticate your accounts,"
    print "'go' to list unread messages,"
    print "'open #' to open the account that has the # index in your web browser,"
    print "and 'quit' to exit GIST."
    print ""
    print "Keep your Terminal window open all day for best effect."
    print "="*124
    print ""
    print ""
    
    gist = Gist()
    gist.prompt = "GIST > "
    gist.do_login("Hi")
    gist.do_go("Hi")
    gist.cmdloop()