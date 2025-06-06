Fitness Classes API Project
A Flask-based backend to fetch upcoming fitness classes with timezone support

<!-- Setup Instructions -->

1. Clone the repository
git clone https://github.com/yourusername/fitness-classes-api.git
cd fitness-classes-api

2. Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

3. Run the flask app
python app.py

<!-- Sample Request -->

Get All Activities
curl http://127.0.0.1:5000/allActivities

Get Upcoming Classes(default IST)
curl http://127.0.0.1:5000/classes

Get Classes in User Timezone (e.g., US/Pacific)
curl "http://127.0.0.1:5000/classes?timezone=US/Pacific"

<!-- Sample db -->
The repo also has sample excel file which is used as a db for this project

<!-- Python Version -->
3.11.5



