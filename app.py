import streamlit as st
from firebase_admin import credentials, initialize_app, db
import requests
import os
import sys

# Ensure required modules are installed
def install_dependencies():
    try:
        import streamlit
    except ImportError:
        os.system(f"{sys.executable} -m pip install streamlit firebase-admin requests")
install_dependencies()

# Firebase setup
FIREBASE_CREDENTIALS = {
  "type": "service_account",
  "project_id": "file-pocket",
  "private_key_id": "ddefa027ca2cdbf99ffc1e97e68d18babc40f010",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCWvxsbDSoUkSoA\nsv4JbytSD35vSa50dk1LUll+zXVAFkgLwyhrhbNAFOFa8p8KH+9XYoe8A2AUtihT\n3LzsV+4Aculk+Rv2TMRMMXQ64D6fC+vjOwvd8jqo6kBNabEz3lEF4qbTJi73mQUx\ntjWvCkzyk1/YkNxS/18rgIc3XXeq3iHn9zg4oasWqe1CY300oB8t7xFYu63Oaau0\n4CgXkzxh6V5Q5SdNg3l8Lcon5zUMw2q+DGcwKVNthPdrGcC0JJJdhr5q5mlz+Mfo\nbbKrnyZakP76DcROoAsrE/5XMjlHb4Nx9Uedw6eX0r+YNThBXLmI7GtTB0t5vPeA\nHTKYkQKXAgMBAAECggEAHoCq7m1af3DkK+IMD0KkZGVoMwKYv04U09Hk9AiE2iPo\nDiE+M4uJOsU+2FVRow3VMzxntL6GGYrGXDnFLJmaOhMGcP0LEGp2Keiz2Rn48dvK\nrl8LRqy1++nyeveQ+KragDNdiEoopMccyvNQp4uRCGCTu1GMk2rDCh1mvug1x6f9\nXPkAWoZweY1C7ySu+LoObc9GS/GEKFnDZpQc0PFmiTb8H0CJNnHrGC8kGMcp5/rR\nbwIQwY8uaLV2h7RfHXssOMs7q3Ze9xhgPoyXrJIJwcEivtSpItN1a5CftNvaazBi\nQdvn7daCP15hQjwlj4bL4UcVpE0u+3LLRAPAYDdsGQKBgQDPRJpijQV7zSGiBKVe\nRLeSosU1hgwouPGuJifKBcc6ug0HqoPk1pialTN8CmykeOu9jhSX2wVFOdo24BWZ\nHATUalr4rol7DbpasbEmJoXV50tvn3sq2uXthdFk+kXJoCXGk6ASroJpHMSBROTr\n5mXQ4PZteQpkhr4vU+vpXr7ffQKBgQC6MH4SMycQHDqy5laWXhloAJmStjb6q+l3\n7G9Km/nYkDi+Y5KmxbKRVXk1gNDc7MjhkIBWZUzT4mWFUBmgACvBWSE5G1J6qJZu\nKUPVBnwXGZWCsMecYIHgWkKryiiB0YLj9LQwrFYSfNHOu3RwzxhHYgo0iMura6dz\n7jRn5tVuowKBgC/CMgS1U+cj7DUF9wjSsq3yHZjoq1KS0vV6yz5MuIx6pFf43W1U\nWVN9P6C8Ui5Pwpop6+rVx9ActYBhf/iIsUA0xYN5zCnzjtYpDZWp2LriEcrFp77H\nM6XYaNhopr3/zdSE3aSQW3JW85yJwGnu69UGkSHGezOQrLABGWHrt/WNAoGAXrz7\n+UDD+KOUjqE7n8mDvfLIMem7sfM1mcrZmiohiDtiVCYQYgGoaeEHCt1f6XomgPfp\nBY0H+axyIdJvJ4XOvdQfXpJzdmxAFw+yLzvceliPRe+zsfM9Qq5KzGTSFbRImLtT\n0IxwQ3n1u+6QQjJuVSwiqzaMA86EZy3mxpOjOGcCgYEAyvt/UXH+5HULeRNyRuh1\nTzydZKc6lBhJ9lAxquov5/JmQKfgzHZct9ED6D83EcVaabuQKP7hUoUGDB2J/p8V\nGMGX7ukRya7LJjrAtiYhUzkXUpeYITB92bM6KnmubILv6D50Gj11lEvoWVVV0kkJ\n++/ExC/mkNqX9bLBeypPl2A=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-1cfkz@file-pocket.iam.gserviceaccount.com",
  "client_id": "105567218028486926943",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-1cfkz%40file-pocket.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
FIREBASE_DATABASE_URL = "https://file-pocket.firebaseio.com/"  # Update with your Firebase database URL

# Initialize Firebase
if not hasattr(st.session_state, 'firebase_initialized'):
    try:
        cred = credentials.Certificate(FIREBASE_CREDENTIALS)
        initialize_app(cred, {'databaseURL': FIREBASE_DATABASE_URL})
        st.session_state.firebase_initialized = True
    except Exception as e:
        st.error(f"An error occurred during Firebase initialization: {e}")
        st.stop()

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
    os.makedirs("uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Generate a dummy URL for demonstration (replace with actual storage upload logic)
    file_url = f"https://example.com/uploads/{file_name}"

    # Update Firebase database
    try:
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
    except Exception as e:
        st.error(f"Failed to update the database: {e}")

    # Remove the local file
    try:
        os.remove(file_path)
    except Exception as e:
        st.warning(f"Failed to remove local file: {e}")

# File download
st.header("Download a File")
user_id = "8xxfBXGrOIP7x4tRsiQGdXn1P9E2"  # Replace with dynamic user ID as needed
try:
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
except Exception as e:
    st.error(f"An error occurred while fetching files: {e}")

# Run the app with `streamlit run <filename>.py`
