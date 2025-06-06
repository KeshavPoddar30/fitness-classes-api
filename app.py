from flask import Flask,jsonify,request
from flasgger import Swagger,swag_from
import settings
import pandas as pd
from datetime import datetime
from utility import getDf,checkSlot,bookSlot,getAllBookings
from pytz import timezone as pytz_timezone
import pytz

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/allActivities")
@swag_from("docs/allActivities.yaml")
def home():
    lst = settings.activities_list
    return jsonify({"activities":lst,"error":False}),200


# @app.route("/classes")
# @swag_from("docs/classes.yaml")
# def classes():
#     try:
#         today = pd.to_datetime(datetime.today().date())
#         file_df = getDf()
#         file_df['DateTime'] = pd.to_datetime(file_df['DateTime'], format="%d-%m-%Y  %H:%M:%S")
#         filtered_df = file_df[file_df['DateTime'] >= today]
#         lst = []
#         for index,row in filtered_df.iterrows():
#             resp = {}
#             resp['Id'] = row['Activity_Id']
#             resp['Name'] = row['Activity_Name']
#             resp['Instructor'] = row['Instructor']
#             resp['Date'] = row['DateTime'].strftime('%Y-%m-%d')
#             resp['Time'] = row['DateTime'].strftime('%H:%M')
#             resp['Duration'] = row['Duration']
#             resp['Booking_Status'] = row['Booked']
#             lst.append(resp)
#         return jsonify({"result":lst,"error":False}),200
#     except Exception as e:
#         print(e)
#         msg = "Error in upcoming_fitness_classes API"
#         print(msg)
#         return jsonify({"message":msg,"error":True}),500

@app.route("/classes")
@swag_from("docs/classes.yaml")
def classes():
    try:
        # Get user's timezone or default to UTC
        user_tz_str = request.args.get("timezone", "UTC")
        try:
            user_tz = pytz_timezone(user_tz_str)
        except Exception:
            user_tz = pytz.UTC

        ist = pytz_timezone("Asia/Kolkata")
        today = pd.to_datetime(datetime.today().date())

        file_df = getDf()
        file_df['DateTime'] = pd.to_datetime(file_df['DateTime'], format="%d-%m-%Y  %H:%M:%S")

        # Attach IST timezone to datetime column
        file_df['DateTime'] = file_df['DateTime'].dt.tz_localize(ist)

        # Filter classes >= today in IST
        ist_today_start = ist.localize(datetime.combine(today, datetime.min.time()))
        filtered_df = file_df[file_df['DateTime'] >= ist_today_start]

        lst = []
        for _, row in filtered_df.iterrows():
            # Convert IST datetime to user's timezone
            user_dt = row['DateTime'].astimezone(user_tz)

            resp = {
                "Id": row['Activity_Id'],
                "Name": row['Activity_Name'],
                "Instructor": row['Instructor'],
                "Date": user_dt.strftime('%Y-%m-%d'),
                "Time": user_dt.strftime('%H:%M'),
                "Duration": row['Duration'],
                "Booking_Status": row['Booked']
            }
            lst.append(resp)

        return jsonify({"result": lst, "error": False}), 200

    except Exception as e:
        print(e)
        msg = "Error in upcoming_fitness_classes API"
        print(msg)
        return jsonify({"message": msg, "error": True}), 500



@app.route("/book",methods=['POST'])
@swag_from("docs/book.yaml")
def book():
    try:
        data = request.get_json()
        activity_id = data.get('class_id')
        client_email = data.get('client_email')
        client_name = data.get('client_name')

        if(activity_id and client_email and client_name):
            activity_id = int(activity_id)
            if(activity_id in [1,2,3]):
                # Check if slots are available or not for that activity id
                res = checkSlot(activity_id)
                if(res['error'] == False):
                    if(res['isAvailable']):
                        # Now you need to book slot at this index
                        res = bookSlot(res['Index'],client_name,client_email)
                        if(res["error"]==False):
                            return jsonify({"message":"Booking Successful","error":False}),200
                        else:
                            return jsonify({"message":"Internal Error","error":True}),500
                    else:
                        return jsonify({"message":"All Slots Booked for this activity","error":False}),200
                else:
                    return jsonify({"message":"Internal Error","error":True}),500
            else:
                return jsonify({"message":"Invalid Activity_Id"}),404
        else:
            return jsonify({"message":"All three fields Id,Email,Name Are Mandatory"}),400
            
    except Exception as e:
        print(e)
        msg = "Error in book API"
        print(msg)
        return jsonify({"message":msg,"error":True}),500
    

@app.route("/bookings",methods=['GET'])
@swag_from("docs/bookings.yaml")
def bookings():
    try:
        email = request.args.get('email')
        if(email):
            email = str(email)
            res = getAllBookings(email)
            if(res["error"]==False):
                if(res["isPresent"]):
                    return jsonify({"Your Bookings":res["data"],"error":False}),200
                else:
                    return jsonify({"message":"No Bookings Made Till Now","error":False}),200
            else:
                return jsonify({"message":"Internal Error","error":True}),500
        else:
            return jsonify({"message":"Email Is Mandatory"}),400

    except Exception as e:
        print(e)
        msg = "Error in bookings API"
        print(msg)
        return jsonify({"message":msg,"error":True}),500

if __name__ == "__main__":
    app.run(debug=True)


