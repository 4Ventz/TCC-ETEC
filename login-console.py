import mysql.connector
import hashlib
import bcrypt

# Conectar ao banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Teste@1",
    database="ulc"
)

# Criar tabela de usuários
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS clientes (id INT AUTO_INCREMENT PRIMARY KEY, clienteNome VARCHAR(255), clienteEmail VARCHAR(255), clienteCelular VARCHAR(11), senhaHashed VARCHAR(512), salt VARCHAR(255) )")

def cadastrar_usuario():
    nome = input("Nome: ")
    email = input("E-mail: ")
    celular = input("Celular (DDD + numero sem espaço e caracteres):")
    senha = input("Senha: ")
    
    # Gerar o salt usando bcrypt
    salt = bcrypt.gensalt().decode()
    senha_hash_salt = bcrypt.hashpw(senha.encode('utf-8'), salt.encode('utf-8')).decode()
    print('salt:')
    print(salt)
    print('senha_hash_salt:')
    print(senha_hash_salt)

    # Inserir usuário no banco de dados
    cursor.execute("INSERT INTO clientes (clienteNome, clienteEmail, clienteCelular, salt, senhaHashed) VALUES (%s, %s, %s, %s, %s)",
                   (nome, email, celular, salt, senha_hash_salt))
    db.commit()

# Função para fazer login
def fazer_login():
    email = input("Digite seu e-mail: ")
    senha = input("Digite sua senha: ")

    # Buscar usuário no banco de dados
    cursor.execute("SELECT * FROM clientes WHERE clienteEmail = %s", (email,))
    usuario = cursor.fetchone()

    if usuario is None:
        print("Usuário não encontrado.")
        return

    salt = usuario[5]
    senha_hash = usuario[4]

    if bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8')):
        print("Login bem sucedido!")
    else:
        print("Senha incorreta.")

# Menu
while True:
    opcao = input("Escolha uma opção:\n1 - Cadastrar usuário\n2 - Fazer login\n3 - Sair\n")

    if opcao == "1":
        cadastrar_usuario()
    elif opcao == "2":
        fazer_login()
    elif opcao == "3":
        break
    else:
        print("Opção inválida")
