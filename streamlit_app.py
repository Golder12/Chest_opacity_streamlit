import streamlit as st
import streamlit_authenticator as stauth

with open('../credentials.yaml') as file:
	config = yaml.load(file, Loader=SafeLoader)
	
authenticator = Authenticate(config['credentials'],config['cookie']['stayLoggedIn'],config['cookie']['5l99yd'],config['cookie']['1'],config['preauthorized'])

name, authentication_status, username = authenticator.login('Login','main')

url = 'https://golder12-chest-opacity-streamlit-rps-app-sicknormal-v647t5.streamlitapp.com/'

if authentication_status:
	webbrowser.open_new_tab(url)
	
