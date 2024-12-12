import streamlit as st
from firebase_admin import credentials, initialize_app, db
import requests
import os

# Firebase setup
FIREBASE_CREDENTIALS = "path/to/your/firebase_credentials.json"  # Update with your Firebase credentials path
FIREBASE_DATABASE_URL = "https://file-pocket.firebaseio.com/"  # Update with your Firebase database URL

# Initialize Firebase
if not hasattr(st.session_state, 'firebase_initialized'):
    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
    initialize_app(cred, {'databaseURL': FIREBASE_DATABASE_URL})
    st.session_state.firebase_initialized = True

# Streamlit app interface
st.title("File Upload and Download with Firebase")

# File upload
st.header("Upload a File")
uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png", "pdf", "txt", "csv", "xlsx"])
if uploaded_file is not None:
    file_name = uploaded_file.name
    file_path = os.path.join("uploads", file_name)
    user_id = "8xxfBXGrOIP7x4tRsiQGdXn1P9E2"  # Replace with dynamic user ID as needed

    # Save the file locally
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Generate a dummy URL for demonstration (replace with actual storage upload logic)
    file_url = f"https://example.com/uploads/{file_name}"

    # Update Firebase database
    db_ref = db.reference(f"Users/{user_id}/Files")
    file_data = {
        "fileName": file_name,
        "fileUri": file_url,
        "timestamp": "1234567890",  # Replace with actual timestamp logic
        "type": "DOC",
        "uid": user_id
    }
    db_ref.push(file_data)
    st.success(f"File '{file_name}' uploaded and database updated!")

    # Remove the local file
    os.remove(file_path)

# File download
st.header("Download a File")
user_id = "8xxfBXGrOIP7x4tRsiQGdXn1P9E2"  # Replace with dynamic user ID as needed
db_ref = db.reference(f"Users/{user_id}/Files")
files = db_ref.get()

if files:
    file_options = {file_info['fileName']: file_info['fileUri'] for file_info in files.values()}
    selected_file = st.selectbox("Select a file to download:", list(file_options.keys()))

    if st.button("Download"):
        file_url = file_options[selected_file]
        response = requests.get(file_url)

        if response.status_code == 200:
            st.download_button(
                label=f"Download {selected_file}",
                data=response.content,
                file_name=selected_file
            )
        else:
            st.error("Failed to download the file.")
else:
    st.write("No files available for download.")

# Run the app with `streamlit run <filename>.py`
