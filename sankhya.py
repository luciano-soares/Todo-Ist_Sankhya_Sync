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

    def setToken(self, token):
        self.__token = token

    def getToken(self):
        return self.__token