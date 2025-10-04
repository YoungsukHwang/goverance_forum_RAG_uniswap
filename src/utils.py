import os
from dotenv import load_dotenv

def get_secret(key: str, st=None) -> str:
    """
    Load secret key flexibly from:
    1. Streamlit Cloud (st.secrets)
    2. Colab userdata (if available)
    3. Environment variables
    4. Local .env file
    """
    # 1. Streamlit
    if st and "secrets" in dir(st) and key in st.secrets:
        return st.secrets[key]

    # 2. Colab secrets
    try:
        from google.colab import userdata
        if key in userdata:
            return userdata.get(key)
    except ImportError:
        pass

    # 3. Environment
    if key in os.environ:
        return os.environ[key]

    # 4. .env file
    load_dotenv()
    val = os.getenv(key)
    if val:
        return val

    raise ValueError(f"❌ Missing required secret: {key}")
