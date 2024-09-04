from sankhya import *
import os
from dotenv import load_dotenv
load_dotenv()

s = Sankhya(os.getenv('SANKHYA_ID_USERNAME')
            , os.getenv('SANKHYA_PASSWORD')
            , os.getenv('SANKHYA_TOKEN')
            , os.getenv('SANKHYA_APPKEY'))
s.login()