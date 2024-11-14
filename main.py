# Importando a função 'create_app' do arquivo 'app' para criar a instância do aplicativo Flask
# E importando o objeto 'db' que é utilizado para interagir com o banco de dados
from app import create_app, db

# Criando a instância do aplicativo Flask chamando a função 'create_app'
app = create_app()

# Usando o contexto de aplicativo para garantir que o código abaixo tenha acesso à configuração do app
# O contexto de aplicativo é necessário para que operações no banco de dados funcionem corretamente
with app.app_context():
    # Criando todas as tabelas definidas no modelo do banco de dados
    # Isso cria as tabelas no banco de dados conforme os modelos definidos (ex.: User, Task)
    db.create_all()

# Verificando se o script está sendo executado diretamente (não importado como módulo)
# Isso é útil para garantir que o servidor Flask seja iniciado apenas quando o script for executado diretamente
if __name__ == '__main__':
    # Inicia o servidor de desenvolvimento Flask com o modo de depuração ativado
    # O servidor será recarregado automaticamente em caso de mudanças no código e erros serão exibidos com mais detalhes
    app.run(debug=True)
