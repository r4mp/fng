"""fng.

Usage:
    fng.py -l <username> [--host=<hostname>]
    fng.py (-h|--help)
    fng.py --version

Options:
    -l          Show user information.
    -h --help   Show this screen.
    --version   Show version.

"""
from docopt import docopt
from datetime import datetime
from datetime import timedelta
import os

class Passwd(object):

    def __init__(self, username):
        self.username = username

    def parse(self):
        f = open('/etc/passwd', 'r')
        for user in f:
            (username, encrypwd, uid, gid, gecos, homedir, usershell) = user.split(':')
            if username == self.username:
                return {'username' : username, 'encrypwd' : encrypwd, 'uid' : uid, 'gid' : gid, 'gecos' : gecos, 'homedir' : homedir, 'usershell' : usershell}

        return {'username' : '', 'encrypwd' : '', 'uid' : '', 'gid' : '', 'gecos' : '', 'homedir' : '', 'usershell' : ''}


class Group(object):

    def __init__(self, username):
        self.username = username
    
    def parse(self):
        g = []

        if self.username == '':
            return g

        f = open('/etc/group', 'r')
        for group in f:
            (groupname, encrypwd, gid, grouplist) = group.split(':')
            users = grouplist.strip().split(',')
            if self.username in users:
                g.append(gid + '(' + groupname + ')')

        return g

class Shadow(object):
    def __init__(self, username):
        self.username = username

    def parse(self):
        if os.geteuid() != 0: # TODO: check diff between geteuid and getuid
                              # TODO: if ... or paramater ssh --> sudo
            return []

        f = open('/etc/shadow', 'r')
        for user in f:
            shadow = user.split(':')
            if self.username == shadow[0]:
                return shadow                 
  
        return []

class User(object):
    
    def __init__(self, username):
        self.username = username
        self.realname = ''
        self.office_number = ''
        self.office_phone_number = ''
        self.home_phone_number = ''
        self.groups = ''
        self.homedir = ''
        self.usershell = ''
        self.last_password_change = ''
        self.password_expires = ''
        self.password_inactive = ''
        self.account_expires = ''
        self.min_days_between_password_change = ''
        self.max_days_between_password_change = ''
        self.days_of_warning_before_password_expires = ''

        self.get()

    def get(self):
        passwd = Passwd(self.username)
        pr = passwd.parse()

        self.username = pr['username']
 
        finger_information =  pr['gecos'].strip().split(',')

        lfi = len(finger_information)

        if lfi > 0:
            self.realname = finger_information[0]

        if lfi > 1:        
            self.office_number = finger_information[1]

        if lfi > 2:
            self.office_phone_number = finger_information[2]
            
        if lfi > 3:
            self.home_phone_number = finger_information[3]

        del lfi

        self.homedir = pr['homedir']
        self.usershell = pr['usershell']

        group = Group(self.username)

        self.groups = ', '.join(group.parse())

        shadow = Shadow(self.username)        
        sr = shadow.parse()

        lsr = len(sr)

        if lsr > 2:
            date_1 = datetime.strptime('01/01/1970', "%m/%d/%Y")
            self.last_password_change = (date_1 + timedelta(days=int(sr[2]))).strftime("%b %d, %Y")
        
        #if lsr > 
        #    self.password_expires = sr[1]
        #    
        #if lsr >
        #    self.password_inactive = ''
        # 
        #    self.account_expires = ''
        
        if lsr > 3:
            self.min_days_between_password_change = sr[3]
        
        if lsr > 4:
            self.max_days_between_password_change = sr[4]
        
        if lsr > 5:
            self.days_of_warning_before_password_expires = sr[5]

        del lsr

    def show(self):
    
        u = ("Username                                            : " + self.username + "\n"
             "Real name                                           : " + self.realname + "\n"
             "Office number                                       : " + self.office_number + "\n"
             "Office phone number                                 : " + self.office_phone_number + "\n"
             "Home phone number                                   : " + self.home_phone_number + "\n"
             ""
             "Groups                                              : " + self.groups + "\n"
             "Homedir                                             : " + self.homedir + "\n"    
             "Usershell                                           : " + self.usershell
            )

        s = (
             "Last password change                                : " + self.last_password_change + "\n"
             "Password expires                                    : " + self.password_expires + "\n" 
             "Password inactive                                   : " + self.password_inactive + "\n" 
             "Account expires                                     : " + self.account_expires + "\n" 
             "Minimum number of days between password change      : " + self.min_days_between_password_change + "\n" 
             "Maximum number of days between password change      : " + self.max_days_between_password_change + "\n" 
             "Number of days of warning before password expires   : " + self.days_of_warning_before_password_expires 
            )

        print(u)
        
        if os.geteuid() == 0: # TODO: check diff between geteuid and getuid
                              # TODO: if ... or paramater ssh --> sudo
            print(s)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='fng 0.1')
    #print(arguments)

    user = User(arguments['<username>'])
    user.show()
