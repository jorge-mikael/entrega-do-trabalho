from dotenv import load_dotenv
import os
from pathlib import Path
import tempfile

load_dotenv()

DB_URL = os.getenv('DB_URL')

SUPABASE_URL = os.getenv('SUPABASE_URL')

BASE_PATH = Path(__file__).resolve().parent.parent

TEMP_PATH = Path(tempfile.mkdtemp())
