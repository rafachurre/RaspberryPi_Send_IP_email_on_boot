__author__ = 'Cody Giles'
__license__ = "Creative Commons Attribution-ShareAlike 3.0 Unported License"
__version__ = "1.0"
__maintainer__ = "Cody Giles"
__status__ = "Production"
__edit_2017_11_16__ = "Rafael Lopez"

import subprocess
import smtplib
from email.mime.text import MIMEText
import datetime

def connect_type(word_list):
    """ This function takes a list of words, then, depeding which key word, returns the corresponding
    internet connection type as a string. ie) 'ethernet'.
    """
    if 'wlan0' in word_list or 'wlan1' in word_list:
        con_type = 'wifi'
    elif 'eth0' in word_list:
        con_type = 'ethernet'
    else:
        con_type = 'current'

    return con_type

# Change to your own account information
# Account Information
to = 'email@email.com' # Email to send to.
gmail_user = 'from_email@gmail.com' # Email to send from. (MUST BE GMAIL)
gmail_password = 'gmailPassword' # Gmail password.
smtpserver = smtplib.SMTP('smtp.gmail.com', 587) # Server to use.

smtpserver.ehlo()  # Says 'hello' to the server
smtpserver.starttls()  # Start TLS encryption
smtpserver.ehlo()
smtpserver.login(gmail_user, gmail_password)  # Log in to server
today = datetime.date.today()  # Get current time/date

arg='ip route list'  # Linux command to retrieve ip addresses.
# Runs 'arg' in a 'hidden terminal'.
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate()  # Get data from 'p terminal'.

# Split IP text block into three, and divide the two containing IPs into words.
ip_lines = data[0].splitlines()
print ip_lines

#######
# EDIT code to avoid errors. Search where is the 'src' to find the IP
#######

ip_messages = []
for line in ip_lines:
  split_line = line.split()
  if 'src' in split_line:
    ip_type = connect_type(split_line)
    ipaddr = split_line[split_line.index('src')+1]
    my_ip = '\nYour %s ip is %s' % (ip_type, ipaddr)
    ip_messages.append(my_ip)

email_body = ''.join(ip_messages)

# Creates the text, subject, 'from', and 'to' of the message.
msg = MIMEText(email_body)
msg['Subject'] = 'IPs For RaspberryPi on %s' % today.strftime('%b %d %Y')
msg['From'] = gmail_user
msg['To'] = to
# Sends the message
smtpserver.sendmail(gmail_user, [to], msg.as_string())
# Closes the smtp server.
smtpserver.quit()

#######
# END EDIT Code
#######

######
# ORIGINAL code
######

""" commented code

split_line_a = ip_lines[1].split()
split_line_b = ip_lines[2].split()

# con_type variables for the message text. ex) 'ethernet', 'wifi', etc.
ip_type_a = connect_type(split_line_a)
ip_type_b = connect_type(split_line_b)


END commented code """

"""Because the text 'src' is always followed by an ip address,
we can use the 'index' function to find 'src' and add one to
get the index position of our ip.
"""

""" commented code

# correction from the original code
if 'src' in split_line_a:
  ipaddr_a = split_line_a[split_line_a.index('src')+1]
else:
  ipaddr_a = "IP not available"

if 'src' in split_line_b:
  ipaddr_b = split_line_b[split_line_b.index('src')+1]
else:
  ipaddr_b = "IP not available"

#Original lines
#ipaddr_a = split_line_a[split_line_a.index('src')+1]
#ipaddr_b = split_line_b[split_line_b.index('src')+1]

# Creates a sentence for each ip address.
my_ip_a = 'Your %s ip is %s' % (ip_type_a, ipaddr_a)
my_ip_b = 'Your %s ip is %s' % (ip_type_b, ipaddr_b)

# Creates the text, subject, 'from', and 'to' of the message.
msg = MIMEText(my_ip_a + "\n" + my_ip_b)
msg['Subject'] = 'IPs For RaspberryPi on %s' % today.strftime('%b %d %Y')
msg['From'] = gmail_user
msg['To'] = to
# Sends the message
smtpserver.sendmail(gmail_user, [to], msg.as_string())
# Closes the smtp server.
smtpserver.quit()


END commented code """