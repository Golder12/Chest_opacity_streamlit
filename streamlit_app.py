import streamlit as st
import streamlit_authenticator as stauth
import tensorflow as tf
import cv2
from PIL import Image, ImageOps
import numpy as np
from pathlib import Path
import pickle
import mysql.connector
from mysql.connector import Error
#from deta import Deta 
#import database as db



#DETA_KEY = "c047zwt7_KsjtGySxoHLJPJYjvAs3DmRiAjhZVJuy"
 
#initialize deta object with a project key
#deta = Deta(DETA_KEY)

#This is how to connect/create a database
#db = deta.Base("patients")

#def insert_patient(patientId, name, image, note):
	#return db.put({"key": patientId, "name": name, "image": image, "diagnosis": note})
	
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

# ---- User authentication -----
names = ["Moses Ntanda", "Doki Golder"]
usernames = ["kmntanda","golderdoki"]

#load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
	hashed_passwords = pickle.load(file)
	
authenticator = stauth.Authenticate(names,usernames, hashed_passwords, "opacity dashboard", "abcedf", cookie_expiry_days=2)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
	st.error("Username/password is incorrect")
	
if authentication_status == None:
	st.warning("Please enter your username and password")

if authentication_status:
	model = tf.keras.models.load_model('sickNormalModel.h5')


	st.write("""
		 # Chest Opacity Classification
		 """
		 )
	st.write("This is a simple image classification web app to diagnose chest opacities in patients")
	
	imageUpload = st.container()
	diagnosisNote = st.container()
	
	with st.form(key = 'my_form'):
		with imageUpload:
			file = st.file_uploader("Please upload an image file", type=["jpg", "png", "jpeg"])


			def import_and_predict(image_data, model):
				img = cv2.resize(np.float32(image_data),(96,122))
				image = img.reshape([-1,96,122,1])
				prediction = model.predict(image)
				return prediction
		
			authenticator.logout("Logout", "sidebar")
			st.sidebar.title(f"Welcome {name}")
	
			if file is None:
				st.text("Please upload an image file")
		
			else:
				image = Image.open(file)
				prediction = import_and_predict(image, model)
				st.write("DIAGNOSIS:")
				if np.argmax(prediction) == 0:
					st.success("HEALTHY")
					currentDiagnosis = "good"
				else:
					st.warning("SICK")
					currentdiagnosis = "bad"
				st.image(image)
	    
		with diagnosisNote:
			txt = st.text_area('Notes about patient ultrasound...')   
		
		
		save_button = st.form_submit_button(label='Save')
		if save_button:
			try:
				print("Connecting to Database")
				connection = mysql.connector.connect(host='sql3.freesqldatabase.com',database='sql3506133',user='sql3506133',password='zFmkCylKBD')

				patient = [];

				sql_select_Query = """select * from UltrasoundPatient ORDER BY patientid DESC LIMIT 1"""

				cursor = connection.cursor(dictionary=True)
				cursor.execute(sql_select_Query)
				records = cursor.fetchall()
			
				print("Fetching each row using column name")
				for row in records:
					id = row["patientId"]
					patient.append(id)
					print(id)
					print(type(patient))
				
				mySql_insert_query = """INSERT INTO UltrasoundImage (image, diagnosis,patientId)VALUES(%s, %s, %s) """
			
				savedImage = convertToBinaryData(image)

				record = (savedImage, currentDiagnosis, patient)
				cursor = connection.cursor()
				cursor.execute(mySql_insert_query, record)
				connection.commit()
				print(cursor.rowcount, "Record inserted successfully into UltrasoundImage table")
				cursor.close()

			except mysql.connector.Error as error:
				print("Failed to insert record into Laptop table {}".format(error))

		#finally:
			#if connection.is_connected():
				#connection.close()
				#print("MySQL connection is closed")	    #st.text("Probability (0: Normal, 1: Sick")
	    #st.write(prediction)
	    
	    #--sidebar
	
	
	
	
