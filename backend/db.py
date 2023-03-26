import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)


db = firestore.client()

# initialize pyrebase
import pyrebase
firebaseConfig = {
  "apiKey": "AIzaSyC-nLDRbjp_DAgJe49mLXK16fAX3qfGGWY",
  "authDomain": "siakad18-18629.firebaseapp.com",
  "databaseURL": "https://siakad18-18629-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "siakad18-18629",
  'storageBucket': "siakad18-18629.appspot.com",
  'messagingSenderId': "142758721967",
  'appId': "1:142758721967:web:eefb8de3f08a657565975a"
}
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()