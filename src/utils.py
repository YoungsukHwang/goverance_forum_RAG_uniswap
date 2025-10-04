import os
from dotenv import load_dotenv

def get_secret(key: str, st=None) -> str:
    """Load secret key from Streamlit or .env"""
    if st and "secrets" in dir(st) and key in st.secrets:
        return st.secrets[key]
    load_dotenv()
    val = os.getenv(key)
    if not val:
        raise ValueError(f"Missing secret: {key}")
    return val
