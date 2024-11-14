# Importando a biblioteca 'os' que pode ser usada para acessar variáveis de ambiente e manipular caminhos de arquivos
import os


# Definindo uma classe de configuração para o aplicativo Flask
class Config:
    # Chave secreta para proteger dados e sessões (deve ser mantida em segredo)
    SECRET_KEY = 'your_secret_key'

    # URI do banco de dados que o Flask SQLAlchemy irá usar (aqui está configurado para usar um banco SQLite local)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    # Desabilita o rastreamento de modificações no banco de dados (melhora a performance e evita alertas desnecessários)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
