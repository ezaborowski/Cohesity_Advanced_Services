import csv
import glob
from datetime import date
from multiprocessing import managers
from sqlite3 import Row
from tkinter.tix import COLUMN

import pandas as pd
 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# pip install manager
# pip install pandas 
# pip install jinja2

raw_input = input
#source = input('Please input the directory of the uncompressed secLogs folder (ex: /Users/john.doe/secLogs): ')
#html_source = input('Please input the share directory you want the HTML files to be saved to (ex: \\Users\john.doe\secLogs): ')

source = "/Users/erin.zaborowski/Documents/Source_Files/Professional_Services/PROJECTS/Memorial_Hermann/Memorial_Hermann_scripts"
html_source = "/Users/erin.zaborowski/Documents/Source_Files/Professional_Services/PROJECTS/Memorial_Hermann/Memorial_Hermann_scripts"

orig_email = "ezaborowski@cohesity.com"
dest_email = "ezaborowski@cohesity.com"

# get current date
dateString = date.today()

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Cohesity Protection Summary HTML Reports"
msg['From'] = orig_email
msg['To'] = dest_email

# load csv files
summary = glob.glob(source + '/ClientSummary_source*.csv')

for i in summary:

    # to read csv file 
    client_html = pd.read_csv(i)

    
    # update html data 
    df = pd.DataFrame(client_html)
    df.style
    print(df)
    #df.to_html(html_source + "/Client_Summary.htm")

    # def file():
    #     styled = df.style.apply(highlight_rows, axis = 0)
    #     f = open('Client_Summary.htm', 'w')
    #     html = (styled.render())
    #     f.write(html)
    #     f.close()

    def highlight_rows(df):        
        #if df.loc[df['Status'].isin('Error')]:
        if df[df["Status"] == 'Error']:
            return ['background-color: red'] * df.size
        elif df.query("Status == 'Error'"):
            return ['background-color: yellow'] * df.size

    # def highlight_greaterthan(s,column):
    #     is_max = pd.Series(data=False, index=s.index)
    #     is_max[column] = s.loc[column] >= 1
    #     return ['background-color: red' if is_max.any() else '' for v in is_max]

    # def highlight_greaterthan_1(s):
    #     if s.Status == "Error":
    #         return ['background-color: red']*16
    #     else:
    #         return ['background-color: green']*16


    # df.style.apply(highlight_greaterthan_1, axis=1)

    # def highlight_rows(row):
    #     value = df[['Status']]
    #     if value == 'Error':
    #         color = '#FFB3BA' # Red
    #     elif value == 'Warn':
    #         color = '#fad378' # Yellow

    #     #return ['background-color: {}'.format(color) for r in row]
    #     return df

    # # to save as html file
    # df.style.apply(highlight_rows, axis=None)
    df.style.apply(highlight_rows, axis = 0)
    df.to_html(html_source + "/Client_Summary.htm")

    
    print("\n")
    print("Client Summary CSV files saved into the following HTML file: " + html_source + "/Client_Summary.htm") 
    print("\n")
    

# load csv files
strike = glob.glob(source + '/StrikeSummary_source-*.csv')

for i in strike:

    # to read csv file 
    strike_html = pd.read_csv(i)

    # to save as html file
    strike_html = pd.DataFrame(strike_html)
    strike_html.fillna('', inplace=True)
    strike_html.to_html(html_source + "/Strike_Summary.htm")

    print("\n")
    print("Client Summary CSV files saved into the following HTML file: " + html_source + "/Strike_Summary.htm") 
    print("\n")
    

# Create the body of the message (a plain-text and an HTML version)
text = "Below are the links to the Cohesity Protection Summary HTML and the Cohesity Strike Summary HTML:\n" + html_source + "/Client_Summary.htm\n" + html_source + "/Strike_Summary.htm"
html = """\
<html>
  <head></head>
  <body>
    <p>Below are the links to the Cohesity Protection Summary HTML and the Cohesity Strike Summary HTML:<br>
       <a href=""" + html_source + "/Client_Summary.htm"""">link</a><br>
       <a href=""" + html_source + "/Strike_Summary.htm"""">link</a><br>
    </p>
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container
# According to RFC 2046, the last part of a multipart message, in this case the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

# Send the message via SMTP server
#smtp_server = smtplib.SMTP('smtp.example.com')
#smtp_server = smtplib.SMTP('localhost')
#smtp_server = smtplib.SMTP('smtp.gmail.com')

# connect to actual host on actual port
    # If you are providing host argument, then you need to specify a port, where SMTP server is listening. Usually this port would be 25.
    # smtp_server = smtp.SMTP(host, port)
    # smtp_server.starttls()
smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtp_server.login(orig_email, '')

# # sendmail function takes 3 arguments: sender's address, recipient's address, and message to send
# try:
#     smtp_server.sendmail(orig_email, dest_email, msg.as_string())
#     smtp_server.quit()
#     print("Successfully sent email")
# except smtplib.SMTPException:
#    print("Error: unable to send email")
# except smtplib.SMTPAuthenticationError:
#    print("Error: unable to send email")

