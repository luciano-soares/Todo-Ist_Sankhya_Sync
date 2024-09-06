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

#buscando tarefas Todo-ist
try:
    tarefasTodoIst = api.get_tasks(project_id = os.getenv('TODOIST_PROJECT_ID'))
except Exception as error:
    print(error)


#inserindo tarefas no todo-ist
for i in range(len(instanciasFlow)):
    jaImportada = False
    instancia = str(instanciasFlow[i][0])
    for j in range(len(tarefasTodoIst)):
        if ('Instância ' + instancia) in tarefasTodoIst[j].content:
            jaImportada = True
            break
    
    if jaImportada == False:
        print('Inserindo instância ' + instancia)
        try:
            task = api.add_task(content="Instância " + str(instanciasFlow[i][0])
                                , description= "* **Solicitação**: " + instanciasFlow[i][1] + '\n' + 
                                               "* **Solicitante**: " + instanciasFlow[i][2] + '\n' + 
                                               "* **Dono**: "        + instanciasFlow[i][3] + '\n' + 
                                               "* **Tarefa**: "      + instanciasFlow[i][4]
                                , project_id=os.getenv('TODOIST_PROJECT_ID'))
        except Exception as error:
            print(error)

for i in range(len(tarefasTodoIst)):
    print(tarefasTodoIst[i].content)

#for i in range(len(instanciasFlow)):
#    print('Instância: '   + str(instanciasFlow[i][0]))
#    print('Solicitação: ' + instanciasFlow[i][1])
#    print('Solicitante: ' + instanciasFlow[i][2])
#    print('Dono: '        + instanciasFlow[i][3])
#    print('Tarefa: '      + instanciasFlow[i][4], end='\n\n')
#
#    try:
#        task = api.add_task(content="Instância " + str(instanciasFlow[i][0])
#                            , description= "* **Solicitação**: " + instanciasFlow[i][1] + '\n' + 
#                                           "* **Solicitante**: " + instanciasFlow[i][2] + '\n' + 
#                                           "* **Dono**: "        + instanciasFlow[i][3] + '\n' + 
#                                           "* **Tarefa**: "      + instanciasFlow[i][4]
#                            , project_id=os.getenv('TODOIST_PROJECT_ID'))
#        print(task)
#    except Exception as error:
#        print(error)
#s.logout()