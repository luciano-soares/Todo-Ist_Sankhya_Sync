from sankhya import *
import os
from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI
load_dotenv()

api = TodoistAPI(os.getenv('TODOIST_TOKEN'))
s = Sankhya(  os.getenv('SANKHYA_ID_USERNAME')
            , os.getenv('SANKHYA_PASSWORD')
            , os.getenv('SANKHYA_TOKEN')
            , os.getenv('SANKHYA_APPKEY'))
s.login()
instanciasFlow = s.buscaTarefasFlow()
for i in range(len(instanciasFlow)):
    print('Instância: '   + str(instanciasFlow[i][0]))
    print('Solicitação: ' + instanciasFlow[i][1])
    print('Solicitante: ' + instanciasFlow[i][2])
    print('Dono: '        + instanciasFlow[i][3])
    print('Tarefa: '      + instanciasFlow[i][4], end='\n\n')

    try:
        task = api.add_task(content="Instância " + str(instanciasFlow[i][0])
                            , description= "* **Solicitação**: " + instanciasFlow[i][1] + '\n' + 
                                           "* **Solicitante**: " + instanciasFlow[i][2] + '\n' + 
                                           "* **Dono**: "        + instanciasFlow[i][3] + '\n' + 
                                           "* **Tarefa**: "      + instanciasFlow[i][4]
                            , project_id=os.getenv('TODOIST_PROJECT_ID'))
        print(task)
    except Exception as error:
        print(error)
s.logout()