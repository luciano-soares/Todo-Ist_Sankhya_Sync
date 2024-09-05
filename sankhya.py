import requests
import json

class Sankhya:
    __token = None
    """
    Classe para interagir com o ERP Sankhya.

    Esta classe fornece métodos para realizar operações básicas de autenticação
    e consulta no sistema ERP da Sankhya. Inclui funcionalidades para login, logout
    e execução de consultas no ERP.

    Atributos:
        Usuario: Email do sankhya ID.
        Senha: Senha do sankhya ID.
        Token: Gerado na tela "Configurações Gatway", dentro do sistema sankhya. Documentação para geração de token: https://ajuda.sankhya.com.br/hc/pt-br/articles/12226863277591-Como-gerar-o-TOKEN-API-de-Servi%C3%A7os-Gateway
        appkey: Gerado pela propria sankhya. Para realizar a criação, basta preencher o formulario "Dados de contato" no site: https://www.sankhya.com.br/parceiros/#

    Métodos:
        - login(): Realiza o login no ERP com as credenciais fornecidas.

    Exemplo de uso:
    """

    def __init__(self, usuario, senha, token, appkey):
        """
        Início da classe.

        Atributos obrigatórios:

        Atributos:
        Usuario: Email do sankhya ID.
        Senha: Senha do sankhya ID.
        Token: Gerado na tela "Configurações Gatway", dentro do sistema sankhya. Documentação para geração de token: https://ajuda.sankhya.com.br/hc/pt-br/articles/12226863277591-Como-gerar-o-TOKEN-API-de-Servi%C3%A7os-Gateway
        appkey: Gerado pela propria sankhya. Para realizar a criação, basta preencher o formulario "Dados de contato" no site: https://www.sankhya.com.br/parceiros/#
        """
        self.usuario = usuario
        self.senha   = senha
        self.token   = token
        self.appkey  = appkey

    def login(self):
        """
        Realiza login no sistema sankhya. Caso o login seja bem-sucessido, o token é armazenado para futuras requisições.

        Retorno da API em caso de sucesso:
        {
            "bearerToken": "123...",
            "error": null
        }

        Retorno da API em caso de falha no login:
        -Token invalido
            {
                "bearerToken": null,
                "error": {
                    "codigo": "4303",
                    "descricao": "Token invalido ou inativado."
                }
            }
        
        - AppKey invalida: 
            {
                "bearerToken": null,
                "error": {
                    "codigo": "4405",
                    "descricao": "Token e Appkey nao associados."
                }
            }
        
        - Usuário invalido:
            {
                "bearerToken": null,
                "error": {
                    "codigo": "GTW3501",
                    "descricao": "Usuario invalido."
                }
            }
        
        - Senha invalida:
            {
                "bearerToken": null,
                "error": {
                    "codigo": "GTW3502",
                    "descricao": "Password invalido."
                }
            }

        """
        url = 'https://api.sankhya.com.br/login'
        headers= {
            'token':    self.token,
            'appkey':   self.appkey,
            'username': self.usuario,
            'password': self.senha
        }

        response = requests.request('POST', url, headers=headers)
        response = json.loads(response.text)

        #Login efetuado com sucesso
        if response['error'] == None:
            self.setToken(response['bearerToken'])
        #Ocorreu algum problema ao efetuar o login.
        else:
            return False
        
    def logout(self):
        """
        Realiza logout no sistema sankhya, invalidando o token utilizado nas requisições.

        Retorno da API em caso de sucesso:
        {
            "serviceName": "MobileLoginSP.logout",
            "status": "1",
            "pendingPrinting": "false",
            "transactionId": "7EE534E462383455C5343056C9E70812",
            "responseBody": {}
        }

        Retorno da API em caso de falha no login:
        -Token invalido
            {
                "fieldSet": null,
                "paginate": null,
                "error": {
                    "codigo": "GTW3403",
                    "descricao": "Bearer Token inválido ou Expirado."
                }
            }
        
        - AppKey invalida: 
            {
                "serviceName": "MobileLoginSP.logout",
                "status": "1",
                "pendingPrinting": "false",
                "transactionId": "C8C929917EE164DCCC4271DC176F6A01",
                "responseBody": {}
            }
        """
        url = 'https://api.sankhya.com.br/gateway/v1/mge/service.sbr?serviceName=MobileLoginSP.logout&outputType=json'

        headers = {
            'Content-Type': 'application/json',
            'appkey': self.appkey,
            'Authorization': 'Bearer ' + self.__token
        }

        requests.request("GET", url, headers=headers)

    def buscaTarefasFlow(self):
        """
        Realiza logout no sistema sankhya, invalidando o token utilizado nas requisições.
        Busca as instâncias no sistema sankhya as instâncias/protocolo que serão analisadas.

        Retorno da API em caso de sucesso:
        {
            "serviceName": "DbExplorerSP.executeQuery",
            "status": "1",
            "pendingPrinting": "false",
            "transactionId": "5BE354E79262E9AA867471BDB69AAE88",
            "responseBody": {
                "fieldsMetadata": [
                    {
                        "name": "INSTANCIA",
                        "description": "INSTANCIA",
                        "order": 1,
                        "userType": "I"
                    },
                    {
                        "name": "SOLICITACAO",
                        "description": "SOLICITACAO",
                        "order": 2,
                        "userType": "S"
                    },
                    {
                        "name": "SOLICITANTE",
                        "description": "SOLICITANTE",
                        "order": 3,
                        "userType": "S"
                    },
                    {
                        "name": "DONO",
                        "description": "DONO",
                        "order": 4,
                        "userType": "S"
                    },
                    {
                        "name": "TAREFA",
                        "description": "TAREFA",
                        "order": 5,
                        "userType": "S"
                    },
                    {
                        "name": "NOMEPROCESSO",
                        "description": "NOMEPROCESSO",
                        "order": 6,
                        "userType": "S"
                    }
                ],
                "rows": [
                    [
                        123,
                        "Criação de expositor 1",
                        "Criação de expositor 1",
                        "Solicitante 1",
                        "Dono 1",
                        "Tarefa Flow",
                        "Processo Flow"
                    ],
                    [
                        456,
                        "Criação de expositor 2",
                        "Solicitante 2",
                        "Dono 2",
                        "Tarefa Flow",
                        "Processo Flow"
                    ],
                    [
                        789,
                        "Criação de expositor 3",
                        "Solicitante 3",
                        "Dono 3",
                        "Tarefa Flow",
                        "Processo Flow"
                    ],
                    [
                        987,
                        "Solicito impressão do certificado 'mandou bem'",
                        "Solicitante 4",
                        "Dono 4",
                        "Tarefa Flow",
                        "Processo flow"
                    ]
                ],
                "burstLimit": false,
                "timeQuery": "6,251s",
                "timeResultSet": "1ms"
            }
        }

        Retorno da API em caso de falha no login:
        -Token expirado
            {
                "serviceName": "DbExplorerSP.executeQuery",
                "status": "3",
                "pendingPrinting": "false",
                "transactionId": "CC8DEFBD6A98621BFB56F7A5AF3A239A",
                "statusMessage": "Não autorizado."
            }
        
        - Token invalido: 
            {
                "fieldSet": null,
                "paginate": null,
                "error": {
                    "codigo": "GTW3403",
                    "descricao": "Bearer Token inválido ou Expirado."
                }
            }
        
        - Comando sql invalido (Erro ao executar o código SQL)
        {
            "serviceName": "DbExplorerSP.executeQuery",
            "status": "0",
            "pendingPrinting": "false",
            "transactionId": "4632B24428FEBA6A32CF6578D2E258EA",
            "statusMessage": mensagem_de_erro(varia de erro para erro)
        }
        """
        url = 'https://api.sankhya.com.br/gateway/v1/mge/service.sbr?serviceName=DbExplorerSP.executeQuery&outputType=json'
        body = json.dumps({
            "serviceName": "DbExplorerSP.executeQuery",
            "requestBody": {
                "sql": """SELECT pdv.idinstprn AS instancia
                        , TO_CHAR(pdv.objet) AS solicitacao
                        , NVL(INITCAP(parsolic.nomeparc), INITCAP(ususolic.nomeusu)) AS solicitante
                        , NVL(INITCAP(pardono.nomeparc), INITCAP(usudono.nomeusu)) AS dono
                        , ele.nome AS tarefa
                        , 'Solicitação de PDV' AS nomeProcesso
                    FROM twfitar tar
                    INNER JOIN ad_ppdv pdv     ON pdv.idinstprn    = tar.idinstprn
                    INNER JOIN tsiusu ususolic ON ususolic.codusu  = tar.codususolicitante
                    LEFT  JOIN tgfpar parsolic ON parsolic.codparc = ususolic.codparc
                    INNER JOIN tsiusu usudono  ON usudono.codusu   = tar.codusudono
                    LEFT  JOIN tgfpar pardono  ON pardono.codparc  = usudono.codparc
                    INNER JOIN twfele ele      ON ele.idelemento   = tar.idelemento
                    WHERE dhconclusao IS NULL
                    AND ele.versao = (SELECT MAX(versao) FROM twfele WHERE idelemento = ele.idelemento)

                    UNION ALL

                    SELECT imp.idinstprn AS instancia
                        , imp.apelido AS solicitacao
                        , NVL(INITCAP(parsolic.nomeparc), INITCAP(ususolic.nomeusu)) AS solicitante
                        , NVL(INITCAP(pardono.nomeparc), INITCAP(usudono.nomeusu)) AS dono
                        , ele.nome AS tarefa
                        , 'Solicitação de impressão' AS nomeProcesso
                    FROM twfitar tar
                    INNER JOIN ad_pimp imp     ON imp.idinstprn = tar.idinstprn
                    INNER JOIN tsiusu ususolic ON ususolic.codusu  = tar.codususolicitante
                    LEFT  JOIN tgfpar parsolic ON parsolic.codparc = ususolic.codparc
                    INNER JOIN tsiusu usudono  ON usudono.codusu   = tar.codusudono
                    LEFT  JOIN tgfpar pardono  ON pardono.codparc  = usudono.codparc
                    INNER JOIN twfele ele      ON ele.idelemento   = tar.idelemento
                    WHERE dhconclusao IS NULL
                    AND ele.versao = (SELECT MAX(versao) FROM twfele WHERE idelemento = ele.idelemento)"""
            }
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.__token
        }

        response = requests.request("POST", url, headers=headers, data=body)
        response = json.loads(response.text)
        if response['status'] == '1':
            return response['responseBody']['rows']
        else:
            return []

    def setToken(self, token):
        self.__token = token

    def getToken(self):
        return self.__token