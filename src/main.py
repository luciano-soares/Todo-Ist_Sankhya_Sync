from sankhya import *
import os
import logging
from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI

# Configuração do logging para registrar eventos e erros no arquivo debug.txt
logging.basicConfig(filename='../logs/debug.log', level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Cria um logger para o módulo principal
logger = logging.getLogger('main')
logger.info(">>>>>>>>>Begin program<<<<<<<<<<")

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa a API do Todoist com o token armazenado nas variáveis de ambiente
api = TodoistAPI(os.getenv('TODOIST_TOKEN'))

# Cria uma instância da classe Sankhya, passando as credenciais necessárias
s = Sankhya(  os.getenv('SANKHYA_ID_USERNAME')
            , os.getenv('SANKHYA_PASSWORD')
            , os.getenv('SANKHYA_TOKEN')
            , os.getenv('SANKHYA_APPKEY'))

# Realiza login no sistema Sankhya
s.login()

# Busca as tarefas pendentes do Sankhya Flow
instanciasFlow = s.buscaTarefasFlow()

# Encerra a sessão de login no Sankhya
s.logout()
logger.info('Instâncias a serem analisadas: ' + str(instanciasFlow))

#buscando tarefas Todo-ist
try:
    tarefasTodoIst = api.get_tasks(project_id = os.getenv('TODOIST_PROJECT_ID'))
except Exception as error:
    # Caso haja erro, registra no log
    logger.error(f"Erro ao buscar tarefas no todo-ist. Motivo: {error}")

logger.info("Tarefas todo-ist a serem analisadas: " + str(tarefasTodoIst))

# Inserindo novas instâncias do Sankhya no Todoist, se ainda não existirem
for i in range(len(instanciasFlow)):
    instanciaImportada = False
    instancia = str(instanciasFlow[i][0])

    # Verifica se a instância já está no Todoist
    for j in range(len(tarefasTodoIst)):
        if ('Instância ' + instancia) in tarefasTodoIst[j].content:
            instanciaImportada = True
            break
    
    # Se a instância não está no Todoist, insere a nova tarefa
    if instanciaImportada == False:
        logger.info(f"Inserindo instância {instancia} no todo-ist")
        try:
            task = api.add_task(content="Instância " + str(instanciasFlow[i][0])
                                , description= "* **Solicitação**: " + instanciasFlow[i][1] + '\n' + 
                                               "* **Solicitante**: " + instanciasFlow[i][2] + '\n' + 
                                               "* **Dono**: "        + instanciasFlow[i][3] + '\n' + 
                                               "* **Tarefa**: "      + instanciasFlow[i][4]
                                , project_id=os.getenv('TODOIST_PROJECT_ID'))
            logger.info(f"Instância {instancia} inserida no todo-ist com sucesso")
        except Exception as error:
            logger.error(f"Instância {instancia} não inserida no todo-ist. Motivo: {error}")

#Atualizando/concluindo tarefas no todo-ist
for i in range(len(tarefasTodoIst)):
    finalizada = True
    for j in range(len(instanciasFlow)):
        #Caso a tarefa já tenha sido finalizada no sankhya flow, marca como concluida a tarefa no todo-ist 
        if tarefasTodoIst[i].content == ('Instância ' + str(instanciasFlow[j][0])):
            finalizada = False
            
            #Caso ocorra alguma mudança no dono da tarefa ou no nome da tarefa (processo andou mas continua com o mesmo dono), atualiza a tarefa com as novas informações.
            if ("* **Dono**: "        + instanciasFlow[j][3] not in tarefasTodoIst[i].description) or ("* **Tarefa**: "      + instanciasFlow[j][4] not in tarefasTodoIst[i].description):
                logger.info(f"Atualizando tarefa {tarefasTodoIst[i].content}.")
                api.update_task(task_id=tarefasTodoIst[i].id, 
                                description= "* **Solicitação**: " + instanciasFlow[j][1] + '\n' + 
                                             "* **Solicitante**: " + instanciasFlow[j][2] + '\n' + 
                                             "* **Dono**: "        + instanciasFlow[j][3] + '\n' + 
                                             "* **Tarefa**: "      + instanciasFlow[j][4])
            break
    
    # Se a instância foi finalizada no Sankhya, encerra a tarefa no Todoist
    if finalizada == True and 'Instância ' in tarefasTodoIst[i].content:
        try:
            api.close_task(task_id = tarefasTodoIst[i].id)
            logger.info(f"Tarefa {tarefasTodoIst[i].content} finalizada no Todo-Ist.")
        except Exception as error:
            logger.error(f"Tarefa {tarefasTodoIst[i].content} não finalizada. Motivo: {error}")

logger.info(">>>>>>>>>>>End program<<<<<<<<< \n\n")