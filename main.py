from sankhya import *
import os
from dotenv import load_dotenv
load_dotenv()

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
s.logout()