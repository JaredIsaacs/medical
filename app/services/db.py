import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class Database:
  def __init__(self) -> None:

    try:
      # Try to get the existing app instance
      self.app = firebase_admin.get_app() 
    except ValueError as e:
      # If an app instance doesn't exist, initialize it
      self.cred = credentials.Certificate("/Users/jaredisaacs/Desktop/medical/app/services/gorilla-gambling-firebase-adminsdk-vp6ev-29d8040597.json")

      self.app = firebase_admin.initialize_app(self.cred)

    self.db = firestore.client()

  def create_user(self, userId: str):
    data = {"money": 100000}
    self.db.collection("gorillas").document(userId).set(data)

    return data

  def get_user(self, userId: str):
    doc_ref = self.db.collection("gorillas").document(userId)
    doc = doc_ref.get()

    if doc.exists:
      return doc.to_dict()
    else:
      return False
    
  def close(self):
    self.app.delete()
    self.db.close()



