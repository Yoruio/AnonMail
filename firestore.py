from google.cloud import firestore

def add_email_json(receive_address, json_str):
    db = firestore.Client()
    data = {'json': json_str}
    db.collection('emails').document(receive_address).set(data)
