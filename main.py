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


#Inserindo tarefas no todo-ist
for i in range(len(instanciasFlow)):
    instanciaImportada = False
    instancia = str(instanciasFlow[i][0])
    for j in range(len(tarefasTodoIst)):
        if ('Instância ' + instancia) in tarefasTodoIst[j].content:
            instanciaImportada = True
            break
    
    if instanciaImportada == False:
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

#Atualizando/concluindo tarefas no todo-ist
for i in range(len(tarefasTodoIst)):
    finalizada = True
    for j in range(len(instanciasFlow)):
        #Caso a tarefa já tenha sido finalizada no sankhya flow, marca como concluida a tarefa no todo-ist 
        if tarefasTodoIst[i].content == ('Instância ' + str(instanciasFlow[j][0])):
            finalizada = False
            
            #Caso ocorra alguma mudança no dono da tarefa ou no nome da tarefa (processo andou mas continua com o mesmo dono), atualiza a tarefa com as novas informações.
            if (instanciasFlow[j][3] not in tarefasTodoIst[i].description) or (instanciasFlow[j][4] not in tarefasTodoIst[i].description):
                api.update_task(task_id=tarefasTodoIst[i].id, 
                                description= "* **Solicitação**: " + instanciasFlow[j][1] + '\n' + 
                                             "* **Solicitante**: " + instanciasFlow[j][2] + '\n' + 
                                             "* **Dono**: "        + instanciasFlow[j][3] + '\n' + 
                                             "* **Tarefa**: "      + instanciasFlow[j][4])
            break
    
    if finalizada == True and 'Instância ' in tarefasTodoIst[i].content:
        try:
            api.close_task(task_id = tarefasTodoIst[i].id)
        except Exception as error:
            print(error)