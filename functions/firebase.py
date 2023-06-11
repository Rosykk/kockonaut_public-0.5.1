import pyrebase
import json
import os

firebase_config = {
    'apiKey': "AIzaSyCfm4rrDmy0nQy0ZHG5rvthKBbXdGFrp5k",
    'authDomain': "kockonaut-a8e99.firebaseapp.com",
    'databaseURL': "https://kockonaut-a8e99-default-rtdb.europe-west1.firebasedatabase.app",
    'projectId': "kockonaut-a8e99",
    'storageBucket': "kockonaut-a8e99.appspot.com",
    'messagingSenderId': "60439510163",
    'appId': "1:60439510163:web:f06881156b6dd899522166",
    'measurementId': "G-6PS61B92SR",
    'serviceAccount': 'key.json'
}

db = pyrebase.initialize_app(firebase_config).database()
