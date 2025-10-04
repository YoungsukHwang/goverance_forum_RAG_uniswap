import os
from dotenv import load_dotenv

def get_secret(key: str, st=None) -> str:
    """
    Load secret key flexibly from:
    1. Streamlit Cloud (st.secrets)
    2. Colab/Environment variables
    3. Local .env file
    """
    # 1. Streamlit
    if st and "secrets" in dir(st) and key in st.secrets:
        return st.secrets[key]

    # 2. Environment (Colab / local export)
    if key in os.environ:
        return os.environ[key]

    # 3. .env file
    load_dotenv()
    val = os.getenv(key)
    if val:
        return val

    raise ValueError(f"❌ Missing required secret: {key}")
