import mysql.connector
import csv
import os
from os import listdir
from os.path import isfile, join
from datetime import datetime

def report():
    mydb = mysql.connector.connect(
            host="148.66.138.159",
            user = "harshita",
            passwd = "harshita",
            database = "harshita"
            )

    mycursor = mydb.cursor()
    now = datetime.now()
    now = now.strftime("%Y-%m-%d")
    mycursor.execute("SELECT users.name,attendance.createdDate as entryDate FROM attendance inner join users on users.id = attendance.user_id where date(attendance.createdDate)  = '"+now+"'")
    records = mycursor.fetchall()
    rows_affected = mycursor.rowcount
    if(rows_affected>0):
        with open('//home//pi//Desktop//IBS_Attendance_Project//report//report.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='', quoting=csv.QUOTE_NONE)
            spamwriter.writerow(["Name","Time"])
            for i in records:
                spamwriter.writerow([i[0],i[1].strftime("%d-%m-%Y %H:%M:%S")])
        
        #for i in records:
         #   print("Name : "++" Time : "+i[1].strftime("%Y-%m-%d-%I-%M"))
    else:
        print("No Records Found")


