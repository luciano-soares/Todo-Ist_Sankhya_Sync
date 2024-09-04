from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv
import os
load_dotenv()

api = TodoistAPI(os.getenv('TOKEN_TODOIST'))

try:
    projects = api.get_projects()
    print(projects[0].name)
except Exception as error:
    print(error)