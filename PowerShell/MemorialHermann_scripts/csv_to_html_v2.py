import csv
import glob
from datetime import date

import pandas as pd
 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

raw_input = input
source = input('Please input the directory of the uncompressed secLogs folder (ex: /Users/john.doe/secLogs): ')

#source = "/Users/erin.zaborowski/Documents/Source_Files/Professional_Services/PROJECTS/Memorial_Hermann/Memorial_Hermann_scripts"

# get current date
dateString = date.today()
print(dateString)

# load csv files
summary = glob.glob(source + '/ClientSummary_source*.csv')

for i in summary:
    print(i)

    # to read csv file 
    csv_file = pd.read_csv(i)

    # to save as html file
    csv_file.to_html(source + "/Client_Summary.htm")
    print("Client Summary CSV files saved into HTML file.") 
    

    # # assign it to a
    # html_file = csv_file.to_html()

# load csv files
strike = glob.glob(source + '/StrikeSummary_source-*.csv')

for i in strike:
    print(i)

    # to read csv file 
    csv_file = pd.read_csv(i)

    # to save as html file
    csv_file.to_html(source + "/Strike_Summary.htm")
    print("Strike Summary CSV files saved into HTML file.") 
    

    # # assign it to a
    # html_file = csv_file.to_html()

# import pandas as pd
# import numpy as np

# # np.random.seed(24)
# # df = pd.DataFrame({'A': np.linspace(1, 10, 10)})

# # df = pd.concat([df, pd.DataFrame(np.random.randn(10, 4), columns=list('BCDE'))],
# #                axis=1)
# # df.iloc[0, 2] = np.nan

# def format_headers(s, threshold, column):
#     is_max = pd.Series(data=False, index=s.index)
#     is_max[column] = s.loc[column] >= threshold
#     return ['background-color: yellow' if is_max.any() else '' for v in is_max]

# s2.applymap_index(lambda v: "background-color: #94CCFA;" "color:black;", axis=0)
# s.set_table_styles([cell_hover, index_names, headers])

# df.style.apply(highlight_greaterthan, threshold=1.0, column=['C', 'B'], axis=1)

#     # html = """
#     # <!DOCTYPE html>
#     # <html lang="en">
#     # <head>
#     #     <meta charset="UTF-8">
#     #     <meta http-equiv="X-UA-Compatible" content="IE=edge">
#     #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     #     <title>Document</title>
#     # </head>
#     # <body>
#     #     <table id="data">
#     # """
#     # html_end = """
#     # </table>
#     # </body>
#     # </html>
#     # """
#     # color_code = {
#     #     "JobRun Status": "lightblue",
#     #     "kSuccess": "lightgreen",
#     #     "kWarning" : "yellow",
    #     "kError" : "red"
    # }

    # for i in report:

    #     # read a csv file
    #     with open(csv_file, newline='') as csvfile:
    #         data = csv.reader(csvfile, delimiter=',')
    #         i = 0
            
    #         for row in data:
    #             new_row = f'    <tr id="{i}" style="background-color: {color_code[row[6]]}">' + ''.join(['<td>' + i + '</td>' for i in row]) + '</tr>\n'
    #             i += 1
    #             html += new_row
                
    #     html += html_end
    #     with open(i.html, 'w') as f:
    #         f.write(html)