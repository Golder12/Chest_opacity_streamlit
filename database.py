import os

from deta import Deta 
from dotenv import load_dotenv
 
 
DETA_KEY = "c047zwt7_KsjtGySxoHLJPJYjvAs3DmRiAjhZVJuy"
 
#initialize deta object with a project key
deta = Deta(DETA_KEY)

#This is how to connect/create a database
db = deta.Base("patients")

def insert_patient(patientId, name, image, note):
	return db.put({"key": patientId, "name": name, "image": image, "diagnosis": note})
	


