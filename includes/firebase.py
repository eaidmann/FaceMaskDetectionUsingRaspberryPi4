import pyrebase

config = {
    "apiKey" : "",
    "authDomain" : "",
    "databaseURL" : "",
    "storageBucket" : "",
    "serviceAccount" : ""
    }

firebase = pyrebase.initialize_app(config)