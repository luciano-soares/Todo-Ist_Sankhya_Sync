import requests

class Sankhya:
    """
    Classe para interagir com o ERP Sankhya.

    Esta classe fornece métodos para realizar operações básicas de autenticação
    e consulta no sistema ERP da Sankhya. Inclui funcionalidades para login, logout
    e execução de consultas no ERP.

    Atributos:
        Usuario: Email do sankhya ID.
        Senha: Senha do sankhya ID.

    Métodos:
        - login(): Realiza o login no ERP com as credenciais fornecidas.

    Exemplo de uso:
    """

    def __init__(self, usuario, senha, token, appkey):
        self.usuario = usuario
        self.senha   = senha
        self.token   = token
        self.appkey  = appkey

    def login(self):
        url = 'https://api.sankhya.com.br/login'
        headers= {
            'token':    self.token,
            'appkey':   self.appkey,
            'username': self.usuario,
            'password': self.senha
        }

        response = requests.request('POST', url, headers=headers)
        print(response.text)