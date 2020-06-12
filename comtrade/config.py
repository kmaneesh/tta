import os
import sys
from pathlib import Path
from dotenv import load_dotenv
ROOT_DIR = Path(os.path.abspath(__file__)).parents[1]
env_path = ROOT_DIR / '.env'
load_dotenv(dotenv_path=env_path)
# Add ROOT_DIR in system path
sys.path.append(str(ROOT_DIR))
