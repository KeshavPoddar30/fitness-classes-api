import pandas as pd
from datetime import datetime
import settings
import smtplib
from email.message import EmailMessage


def getDf():
    try:
        file_path = settings.db_file_path
        df = pd.read_excel(file_path, dtype={'Client_Name': str, 'Client_Email': str})
        return df
    except Exception as e:
        print("Error in getDf") 
        print(e)
        return None
    
def checkSlot(activity_id):
    try:
        df = getDf()
        res = False
        indx = -1
        today = pd.to_datetime(datetime.today().date())
        df['DateTime'] = pd.to_datetime(df['DateTime'], format="%d-%m-%Y  %H:%M:%S")
        df_2 = df[df['DateTime'] >= today]

        for index,row in df_2.iterrows():
            if(index == 0 or row['Activity_Id']!=activity_id):
                continue
            else:
                if(row['Booked']==False):
                    res = True
                    indx = index
                    break

        msg = {"isAvailable":res,"Index":indx,"error":False}               
        return msg

    except Exception as e:
        print(e)
        print("Error in checkSlot function")
        return {"error":True}
    
def bookSlot(indx,name,email):
    try:
        df = getDf()
        df.at[indx, 'Client_Name'] = name
        df.at[indx, 'Client_Email'] = email
        df.at[indx, 'Booked'] = True
        time = df.iloc[indx]['DateTime'].strftime('%H:%M')
        date = df.iloc[indx]['DateTime'].strftime('%Y-%m-%d')
        res = updateDf(df,time,email,date)
        if(res['error']==False):
            return {"message":"Booking Done","error":False}
        else:
            return {"error":True}    
    except Exception as e:
        print(e)
        print("Error in bookSlot function")
        return {"error":True}
    
def updateDf(df,time,email,date):
    try:
        df.to_excel(settings.db_file_path,index=False)
        res = sendEmail(email,time,date)
        if(res['error']==False):
            return {"message":"Updated Successfully","error":False}
        else:
            return {"error":True}    
    except Exception as e:
        print(e)
        print("Error in updateDf function")
        return {"error":True}
    
def sendEmail(email,time,date):
    try:
        server = smtplib.SMTP(settings.email_domain, settings.email_port)
        server.starttls()
        server.login(settings.sender_email, settings.appPassword)
        msg = EmailMessage()
        msg['Subject'] = "Slot Confirmation In Our Fitness Studio"
        msg['From'] = settings.sender_email
        msg['To'] = email
        body = f"Your slot has successfully been booked on {date} at {time}"
        msg.set_content(body)
        server.send_message(msg)
        server.quit()
        return {"message":"Mail Sent Successfully","error":False}

    except Exception as e:
        print(e)
        print("Error in sendEmail function")
        return {"error":True}
    
def getAllBookings(email):
    try:
        df = getDf()
        lst = []
        
        for index,row in df.iterrows():
            if(index==0):
                continue
            if pd.isna(row.get('Client_Email')):
                continue
            if (str(row['Client_Email']) == email):
                booking = {
                    "Activity_Id": row['Activity_Id'],
                    "Activity_Name": row['Activity_Name'],
                    "Instructor": row['Instructor'],
                    "Date": row['DateTime'].strftime('%Y-%m-%d'),
                    "Time": row['DateTime'].strftime('%H:%M'),
                    "Duration": row['Duration']
                }
                lst.append(booking)

        if(len(lst)>0):
            return {"data":lst,"isPresent":True,"error":False}
        else:
            return {"isPresent":False,"error":False}

    except Exception as e:
        print(e)
        print("Error in getAllBookings function")
        return {"error":True}
