import streamlit as st
import json
import os

# Check if required packages are installed
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Firebase Admin SDK not installed. Please run: pip install firebase-admin")
    st.error(f"Error: {e}")
    FIREBASE_AVAILABLE = False

def load_configs():
    """Load temple configurations from config.json file"""
    try:
        with open('config.json', 'r') as f:
            configs = json.load(f)
        return configs
    except FileNotFoundError:
        st.error("❌ config.json file not found. Please create it with your temple configurations.")
        return []
    except json.JSONDecodeError as e:
        st.error(f"❌ Error parsing config.json: {e}")
        return []
    except Exception as e:
        st.error(f"❌ Error loading configs: {e}")
        return []


# Initialize Firebase (only once)
if "firebase_initialized" not in st.session_state:
    st.session_state.firebase_initialized = False


def validate_service_account_json(json_content):
    """Validate the service account JSON structure"""
    required_fields = [
        "type", "project_id", "private_key_id", "private_key", 
        "client_email", "client_id", "auth_uri", "token_uri"
    ]
    
    try:
        data = json.loads(json_content)
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        if data.get("type") != "service_account":
            return False, "Invalid type. Must be 'service_account'"
            
        return True, "Valid service account JSON"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON format: {e}"


def init_firestore(service_json):
    if not FIREBASE_AVAILABLE:
        st.error("Firebase Admin SDK not available")
        return None
        
    if not st.session_state.firebase_initialized:
        try:
            # Read the uploaded file content
            json_content = service_json.read().decode('utf-8')
            
            # Validate the JSON structure
            is_valid, message = validate_service_account_json(json_content)
            if not is_valid:
                st.error(f"❌ Invalid service account JSON: {message}")
                return None
            
            # Parse the JSON content into a dictionary
            service_account_info = json.loads(json_content)
            
            # Pass the dictionary directly to credentials.Certificate
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred)
            st.session_state.db = firestore.client()
            st.session_state.firebase_initialized = True
            st.success("✅ Firebase initialized successfully!")
            return st.session_state.db
            
        except Exception as e:
            st.error(f"❌ Error initializing Firebase: {str(e)}")
            st.error("Please check your service account JSON file and try again.")
            return None
    
    return st.session_state.db


st.set_page_config(page_title="Upcoming Events Uploader", layout="wide")

st.title("📅 Upcoming Events Manager")

if not FIREBASE_AVAILABLE:
    st.stop()

# Firebase setup options
st.write("### 🔑 Firebase Setup")
st.write("Choose one of the following options:")

# Option 1: Upload file
st.write("**Option 1: Upload Service Account JSON**")
st.write("1. Go to [Firebase Console](https://console.firebase.google.com/)")
st.write("2. Select your project → Project Settings → Service Accounts")
st.write("3. Click 'Generate New Private Key' to download the JSON file")
st.write("4. Upload the JSON file below:")

service_json = st.file_uploader("Upload Firestore Service Account (JSON)", type=["json"])

# Option 2: File path
st.write("**Option 2: Use File Path (if file is in repo)**")
service_json_path = st.text_input("Enter path to service account JSON file:", 
                                 placeholder="e.g., ./prod_nri_firebase.json or /full/path/to/file.json")

# Check which option is used
if service_json:
    # Use uploaded file
    db = init_firestore(service_json)
elif service_json_path and os.path.exists(service_json_path):
    # Use file path
    try:
        with open(service_json_path, 'r') as f:
            service_account_info = json.load(f)
        
        # Validate the JSON structure
        is_valid, message = validate_service_account_json(json.dumps(service_account_info))
        if not is_valid:
            st.error(f"❌ Invalid service account JSON: {message}")
        else:
            if not st.session_state.firebase_initialized:
                try:
                    cred = credentials.Certificate(service_account_info)
                    firebase_admin.initialize_app(cred)
                    st.session_state.db = firestore.client()
                    st.session_state.firebase_initialized = True
                    st.success("✅ Firebase initialized successfully!")
                    db = st.session_state.db
                except Exception as e:
                    st.error(f"❌ Error initializing Firebase: {str(e)}")
                    db = None
            else:
                db = st.session_state.db
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
        db = None
elif service_json_path:
    st.error(f"❌ File not found: {service_json_path}")
    db = None
else:
    db = None

if db:  # Only proceed if Firebase is initialized
    st.sidebar.header("📍 Input Configs")

    # Load configs from config.json
    configs = load_configs()

    if not configs:
        st.warning("No temple configurations found in config.json. Please ensure it contains valid JSON.")
        st.stop()

    selected_config = st.sidebar.radio(
        "Select a Place", configs, format_func=lambda x: x["site_name"]
    )

    st.subheader(f"🕌 {selected_config['site_name']} - {selected_config['location']}")
    st.markdown(f"[🌐 Visit Source]({selected_config['source_url']})")

    st.write("### Paste Upcoming Events JSON")
    events_json_text = st.text_area(
        "Paste JSON array of events here",
        height=300,
        placeholder='[{"event_name": "Janmashtami", "date_time": "Aug 24, 2025, 7 PM", "venue": "Temple Hall"}]'
    )

    if st.button("🚀 Upload to Firestore"):
        try:
            events = json.loads(events_json_text)

            if not isinstance(events, list):
                st.error("Events must be a JSON array (list of objects).")
            else:
                doc_data = {
                    "place_id": selected_config["place_id"],
                    "site_name": selected_config["site_name"],
                    "location": selected_config["location"],
                    "source_url": selected_config["source_url"],
                    "last_updated": selected_config["last_updated"],
                    "events": events
                }

                # Firestore save: use place_id as ref_id
                ref = db.collection("temple_events").document(selected_config["place_id"])
                ref.set(doc_data)

                st.success(f"✅ Events uploaded successfully for {selected_config['site_name']}")
        except Exception as e:
            st.error(f"Error parsing JSON or uploading: {e}")
else:
    st.info("👆 Please upload your Firebase service account JSON file or provide a file path to continue")
