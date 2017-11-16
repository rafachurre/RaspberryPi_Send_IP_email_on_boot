# RaspberryPi_Send_IP_email_on_boot
Sends email with the RPi IP when booting the Pi. This is useful when moving the pi from one network to other.

# Tutorial
https://elinux.org/RPi_Email_IP_On_Boot_Debian

***2017/11/16*** - The code in this tutorial leads into errors with indexes when executing in ARMBIAN. I edited the code to search the IP in all the lines instead of hardcoding the selected lines. This approach avoid outOfBounds errors and index() errors when seaching for 'src' word.


### What Does it Do?
This code will extract the ip address of your Pi and then send an email containing the ip to the specified email address. This is inspired by the need to access the Pi via SSH or other network protocols without a monitor and moving from network to network. This uses a Gmail SMTP server, and assumes you have a valid Gmail address. You may need to alter a bit for other servers (beyond the scope of this article).

### What Do You Need?
A working, and network enabled Raspberry Pi

### What Skill Level is Required?
Medium Level. You should be comfortable navigating a Linux system and be comfortable using sudo (if you want to use this script, odds are you are quite comfortable at the command prompt).

### Overview of this Guide
You need to: 1. Create a Python script and store it in a directory. 2. Make Python script executable. 3. Set the program to run at boot time.

# LET'S DO IT!
Create the Python Script
Copy and paste the following code into a text editor (I'm a Vim man myself).

```
__author__ = 'Cody Giles'
__license__ = "Creative Commons Attribution-ShareAlike 3.0 Unported License"
__version__ = "1.0"
__maintainer__ = "Cody Giles"
__status__ = "Production"

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
to = 'username@email.com' # Email to send to.
gmail_user = 'username@gmail.com' # Email to send from. (MUST BE GMAIL)
gmail_password = 'gmailpassword' # Gmail password.
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
split_line_a = ip_lines[1].split()
split_line_b = ip_lines[2].split()

# con_type variables for the message text. ex) 'ethernet', 'wifi', etc.
ip_type_a = connect_type(split_line_a)
ip_type_b = connect_type(split_line_b)

"""Because the text 'src' is always followed by an ip address,
we can use the 'index' function to find 'src' and add one to
get the index position of our ip.
"""
ipaddr_a = split_line_a[split_line_a.index('src')+1]
ipaddr_b = split_line_b[split_line_b.index('src')+1]

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
```


Save this script using a nice name like 'startup_mailer.py' and make note of its path (like /home/pi/Code/startup_mailer.py)

For good measure, make the script executable

> sudo chmod +x startup_mailer.py

# Edit /boot/boot.rc
Using your text editor once again, edit /boot/boot.rc (this assumes you have already renamed this file to boot.rc If not, see RPi_Advanced_Setup). For example:

> sudo nano /boot/boot.rc

Add the following at the end of the file, making changes to the path for your directory tree and save.

> python /home/pi/Code/startup_mailer.py

## Alternative if Using Rasbian
If you are using Rasbian you won't have a /boot/boot.rc file. Instead you can edit /etc/rc.local as follows:

> sudo nano /etc/rc.local

Add the 'python /home/pi/Code/startup_mailer.py' line, so the file now looks like this:

```
 # rc.local
 #
 # This script is executed at the end of each multiuser runlevel.
 # Make sure that the script will "exit 0" on success or any other
 # value on error.
 #
 # In order to enable or disable this script just change the execution
 # bits.
 #
 # By default this script does nothing.
 # Print the IP address if it doesn't work ad sleep 30 before all your code 
 _IP=$(hostname -I) || true
 if [ "$_IP" ]; then
   printf "My IP address is %s\n" "$_IP"
   python /home/pi/Code/startup_mailer.py        <<<------------------------------------------ ADD THIS LINE!!!
 fi
 exit 0
```

# FINISHED!
Reboot your Pi and you should receive an email with your ip address.

## Troubleshooting
+ If you don't get your email notification: connect your pi to a monitor, boot and wait until you reach the 'login' prompt, and check if it says "My IP Address is...". If it doesn't, you may add 'sleep 30'(no quotes) in the etc/rc.local just after the last comment(# Print the IP...).

+ If you don't get email when rebooting, you have to check the hostname you currently have. because the script calls for #raspberrypi. Just type in the command line # hostname. if you have an other hostname its simple just change you hostname #with your preferred editor. Also in etc/hosts on the bottom of the page.

> $ msg['Subject'] = 'IP For YOUR HOSTNAME on %s' % today.strftime('%b %d %Y')


# EDIT: 2017/11/16

```
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
```
