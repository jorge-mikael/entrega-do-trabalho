from dotenv import load_dotenv
import os
from pathlib import Path
import tempfile

BASE_PATH = Path(__file__).resolve().parent.parent

load_dotenv(BASE_PATH / '.env', override=True)

DB_URL = os.getenv('DB_URL')

SUPABASE_URL = os.getenv('SUPABASE_URL')

TEMP_PATH = Path(tempfile.mkdtemp())
