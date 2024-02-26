import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceaccountkey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://faceattendencerealtime-66d5a-default-rtdb.firebaseio.com/"
})

reference = db.reference("Students")

data = {
    "22m1436":
        {
            "name": "Krishnendu Barman",
            "roll": "22m1436",
            "class": "M.Tech.",
            "department": "ESED",
            "starting_year": 2022,
            "attendance": 0,
            "standings": "Good",
            "Year": 2,
            "last_attendance_time": "2023-12-29 13:00:00"
        },
    "22m1435":
        {
            "name": "Prashant Kumar",
            "roll": "22m1435",
            "class": "M.Tech.",
            "department": "ESED",
            "starting_year": 2022,
            "attendance": 0,
            "standings": "Good",
            "Year": 2,
            "last_attendance_time": "2023-12-29 13:00:00"
        },
    "22m1443":
        {
            "name": "Shreya Kundar",
            "roll": "22m1443",
            "class": "M.Tech.",
            "department": "ESED",
            "starting_year": 2022,
            "attendance": 0,
            "standings": "Good",
            "Year": 2,
            "last_attendance_time": "2023-12-29 13:00:00"
        },

    "22m1444":
        {
            "name": "Shrabanti Barman",
            "roll": "22m1444",
            "class": "M.Tech.",
            "department": "Nursing",
            "starting_year": 2020,
            "attendance": 0,
            "standings": "very good",
            "Year": 3,
            "last_attendance_time": "2023-12-29 13:00:00"
        }
}

for key, value in data.items():
    reference.child(key).set(value)
