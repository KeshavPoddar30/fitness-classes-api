import pandas as pd
from datetime import datetime
from flask import jsonify

file_path = r"C:\Users\Keshav Poddar\Desktop\Job_Project\Fitness_Studio\db.xlsx"

def open_file(file_path):
    try:
        file_df = pd.read_excel(file_path)
        return file_df

    except Exception as e:
        print("Error in open_file function")
        print(e)

def upcoming_fitness_classes(file_df):
    try:
        today = datetime.today().date()
        file_df['Date'] = pd.to_datetime(file_df['Date'], format='%d-%m-%Y')
        filtered_df = file_df[file_df['Date'].dt.date >= today]
        lst = []
        for index,row in filtered_df.iterrows():
            resp = {}
            resp['Id'] = row['Activity_Id']
            resp['Name'] = row['Activity_Name']
            resp['Instructor'] = row['Instructor']
            resp['Date'] = row['Date']
            resp['Slot'] = row['Time']
            resp['Duration'] = row['Duration']
            resp['Booking_Status'] = row['Booked']
            lst.append(resp)
        return jsonify({"result":lst,"error":False}),200
    except Exception as e:
        msg = "Error in upcoming_fitness_classes API"
        print(msg)
        return jsonify({"message":msg,"error":True}),500

df = open_file(file_path)
upcoming_fitness_classes(df)

