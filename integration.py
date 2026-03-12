import streamlit as st
import requests

if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.user = None
    st.session_state.token = None

if not st.session_state.login:
    email = st.text_input("Enter Email")
    password = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        login = requests.post("http://backend:8000/login",json ={
        "email":email,
        "password":password
        })
        if login.status_code == 200:
            st.session_state.user = login.json()["name"]
            st.session_state.token = login.json()["token"]
            st.session_state.login = True
            st.rerun()
        else:
            st.error(login.json()["message"])

if st.session_state.login:

    st.subheader(f"Welcome {st.session_state.user}")
    user = requests.get("http://backend:8000/get-students",headers = {"Authorization": f"Bearer {st.session_state.token}"})
    user_data = user.json()
    for user in user_data:
        st.write(user)

    file_upload = st.file_uploader("upload a file")
    if file_upload is not None:
        file = {
            "file": (file_upload.name, file_upload, file_upload.type)
        }
        response = requests.post("http://backend:8000/upload-file", files=file, headers={"Authorization": f"Bearer {st.session_state.token}"})
        if response.status_code == 200:
            st.success("File uploaded successfully")
        else:
            st.error("Failed to upload file")
    
    filename = st.text_input("Enter file name")
    if st.button("download"):
        response = requests.get(f"http://backend:8000/download/{filename}", headers={"Authorization": f"Bearer {st.session_state.token}"})
        if response.status_code == 200:
            st.image(response.content)
            st.download_button("Download File", data=response.content, file_name=filename  , mime="application/octet-stream")
        else:
            st.error("Failed to download file")
  

