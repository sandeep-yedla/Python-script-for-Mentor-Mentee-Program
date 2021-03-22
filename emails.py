'''
 * Running the script send emails to paired mentors and mentees(500/Day Max)
 * Created by ISA 2019-20
 * User: Sidheswar Venkatachalapathi
 * Date: 1/4/2020
 * Time: 3:20 AM
'''

import pandas as pd
import time
import sys
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import param

# Method to send emails
def send_emails(index, pairing, email_success, email_failed):
    # if email already sent, skip
    if pairing.loc[index, 'Email Sent'] == True:
        return pairing, email_success, email_failed
    else:
        # extract infomation from the data frame
        mentee_email = pairing.loc[index, 'Mentee Email']
        mentee_name = pairing.loc[index, 'Mentee Name']
        mentor_email = pairing.loc[index, 'Mentor Email']
        mentor_name = pairing.loc[index, 'Mentor Name']
        to_addr = [mentee_email, mentor_email]
        html = (param["html"]["greeting"]+
                mentee_name+
                param["html"]["introduction"]+
                mentor_name+
                param["html"]["address_mentee"]+
                mentor_name+
                param["html"]["address_mentor"])

        # Create the email object
        msg = MIMEMultipart()
        msg['From'] = param["from_addr"]
        msg['To'] = ", ".join(to_addr)
        msg['Subject'] = param["subject"]
        msg.attach(MIMEText(html, 'html'))

        # Initiate email server and login with the credentials
        smtp_server = smtplib.SMTP(param["host"], 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(param["from_addr"],param["password"])

        # Compile email: From, To, Email body
        text = msg.as_string()
        try:
            # Send email and update Email Sent Column to True
            smtp_server.sendmail(param["from_addr"], to_addr, text)
            pairing.loc[index, 'Email Sent'] = True
            print("Email sent! :)")
            email_success = email_success + 1
        except:
            # Catch cases where Email failed to send
            print("Email failed to send! :(")
            email_failed = email_failed + 1
        return pairing, email_success, email_failed
        smtp_server.quit()

start_time = time.time()

# Read the Pairing CSV file
pairing = pd.read_csv("Pairing.csv", index_col=0)
print(pairing.head())

# Iterate through every row and call send_emails() method
email_success = 0
email_failed = 0
for index, row in pairing.iterrows():
    pairing, email_success, email_failed = send_emails(index, pairing, email_success, email_failed)

# Save the updated dataframe into a new file
pairing.to_csv("Pairing2.csv", encoding="utf-8")
print ("\n" + str(email_failed) +" email(s) failed to send!")
print("\n" + str(email_success) +" email(s) sent in {:.2f}".format(time.time() - start_time) + " seconds\n")
