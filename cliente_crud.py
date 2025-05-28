# cliente_crud.py
# Este arquivo contém as funções CRUD (Create, Read, Update, Delete) para a entidade 'clientes'.

from db_utils import executar_query  # Importa a função para executar queries

def adicionar_cliente(conexao, nome, endereco, cpf, telefone):
    """
    Adiciona um novo cliente ao banco de dados.

    Args:
        conexao: Objeto de conexão com o banco.
        nome (str): Nome do cliente.
        endereco (str): Endereço do cliente.
        cpf (str): CPF do cliente (deve ser único).
        telefone (str): Telefone do cliente.

    Returns:
        int or None: O ID do cliente adicionado se sucesso, None caso contrário.
    """
    query = "INSERT INTO clientes (nome, endereco, cpf, telefone) VALUES (%s, %s, %s, %s)"
    params = (nome, endereco, cpf, telefone)
    try:
        cliente_id = executar_query(conexao, query, params, commit=True)
        if cliente_id:
            print(f"Cliente '{nome}' adicionado com sucesso (ID: {cliente_id}).")
            return cliente_id
        else:
            # Isso pode acontecer se o CPF já existir (devido à restrição UNIQUE)
            # ou outro erro na execução da query.
            print(f"Falha ao adicionar cliente '{nome}'. Verifique se o CPF já está cadastrado.")
            return None
    except Exception as e:
        print(f"Erro inesperado ao adicionar cliente: {e}")
        return None

def listar_clientes(conexao):
    """
    Lista todos os clientes cadastrados no banco de dados.

    Args:
        conexao: Objeto de conexão com o banco.

    Returns:
        list or None: Uma lista de dicionários representando os clientes, ou None se não houver clientes ou erro.
    """
    query = "SELECT id, nome, cpf, telefone, endereco FROM clientes"
    clientes = executar_query(conexao, query, fetch_all=True)
    if clientes:
        print("\n--- Lista de Clientes ---")
        for cliente in clientes:
            print(f"ID: {cliente['id']}, Nome: {cliente['nome']}, CPF: {cliente['cpf']}, "
                  f"Tel: {cliente['telefone']}, End: {cliente['endereco']}")
        print("------------------------")
    elif clientes == []: # Lista vazia significa que não há clientes
        print("Nenhum cliente cadastrado.")
    else: # None significa que houve um erro na consulta
        print("Falha ao listar clientes.")
    return clientes

def consultar_cliente_por_cpf(conexao, cpf):
    """
    Consulta um cliente específico pelo seu CPF.

    Args:
        conexao: Objeto de conexão com o banco.
        cpf (str): CPF do cliente a ser consultado.

    Returns:
        dict or None: Um dicionário com os dados do cliente se encontrado, None caso contrário.
    """
    query = "SELECT id, nome, cpf, telefone, endereco FROM clientes WHERE cpf = %s"
    params = (cpf,)
    cliente = executar_query(conexao, query, params, fetch_one=True)
    if cliente:
        print("\n--- Cliente Encontrado ---")
        print(f"ID: {cliente['id']}, Nome: {cliente['nome']}, CPF: {cliente['cpf']}, "
              f"Tel: {cliente['telefone']}, End: {cliente['endereco']}")
        print("------------------------")
    else:
        print(f"Cliente com CPF '{cpf}' não encontrado.")
    return cliente

def consultar_cliente_por_id(conexao, cliente_id):
    """
    Consulta um cliente específico pelo seu ID.
    Esta função é útil internamente, por exemplo, para verificar se um cliente existe antes de uma atualização ou exclusão.

    Args:
        conexao: Objeto de conexão com o banco.
        cliente_id (int): ID do cliente a ser consultado.

    Returns:
        dict or None: Um dicionário com os dados do cliente se encontrado, None caso contrário.
    """
    query = "SELECT id, nome, cpf, telefone, endereco FROM clientes WHERE id = %s"
    params = (cliente_id,)
    return executar_query(conexao, query, params, fetch_one=True)


def atualizar_cliente(conexao, cliente_id, nome=None, endereco=None, telefone=None):
    """
    Atualiza os dados de um cliente existente.
    O CPF não é atualizável por ser um identificador único importante.

    Args:
        conexao: Objeto de conexão com o banco.
        cliente_id (int): ID do cliente a ser atualizado.
        nome (str, optional): Novo nome do cliente.
        endereco (str, optional): Novo endereço do cliente.
        telefone (str, optional): Novo telefone do cliente.

    Returns:
        bool: True se a atualização foi bem-sucedida, False caso contrário.
    """
    cliente_existente = consultar_cliente_por_id(conexao, cliente_id)
    if not cliente_existente:
        print(f"Cliente com ID {cliente_id} não encontrado. Não é possível atualizar.")
        return False

    campos_para_atualizar = []
    params_valores = []

    if nome is not None and nome.strip() != "":
        campos_para_atualizar.append("nome = %s")
        params_valores.append(nome)
    if endereco is not None and endereco.strip() != "":
        campos_para_atualizar.append("endereco = %s")
        params_valores.append(endereco)
    if telefone is not None and telefone.strip() != "":
        campos_para_atualizar.append("telefone = %s")
        params_valores.append(telefone)

    if not campos_para_atualizar:
        print("Nenhum dado fornecido para atualização ou os dados fornecidos estão vazios.")
        return False

    query = f"UPDATE clientes SET {', '.join(campos_para_atualizar)} WHERE id = %s"
    params_valores.append(cliente_id) # Adiciona o ID do cliente ao final da lista de parâmetros

    # A função executar_query para UPDATE/DELETE retorna rowcount (>=0 se sucesso) ou None se erro.
    resultado_update = executar_query(conexao, query, tuple(params_valores), commit=True)
    if resultado_update is not None: # Se não for None, a query foi executada (mesmo que 0 linhas afetadas)
        print(f"Dados do cliente ID {cliente_id} atualizados com sucesso.")
        return True
    else:
        print(f"Falha ao atualizar dados do cliente ID {cliente_id}.")
        return False


def excluir_cliente(conexao, cliente_id):
    """
    Exclui um cliente do banco de dados.
    Devido à configuração 'ON DELETE CASCADE' na tabela 'veiculos',
    todos os veículos associados a este cliente também serão excluídos.

    Args:
        conexao: Objeto de conexão com o banco.
        cliente_id (int): ID do cliente a ser excluído.

    Returns:
        bool: True se a exclusão foi bem-sucedida, False caso contrário.
    """
    cliente_existente = consultar_cliente_por_id(conexao, cliente_id)
    if not cliente_existente:
        print(f"Cliente com ID {cliente_id} não encontrado. Não é possível excluir.")
        return False

    # Confirmação do usuário antes de excluir
    confirmacao = input(f"Tem certeza que deseja excluir o cliente '{cliente_existente['nome']}' (ID: {cliente_id}) "
                        f"e todos os seus veículos associados? (s/N): ").strip().lower()
    if confirmacao != 's':
        print("Exclusão cancelada pelo usuário.")
        return False

    query = "DELETE FROM clientes WHERE id = %s"
    params = (cliente_id,)
    # A função executar_query para UPDATE/DELETE retorna rowcount (>=0 se sucesso) ou None se erro.
    resultado_delete = executar_query(conexao, query, params, commit=True)
    if resultado_delete is not None:
        print(f"Cliente ID {cliente_id} ('{cliente_existente['nome']}') e seus veículos foram excluídos com sucesso.")
        return True
    else:
        print(f"Falha ao excluir cliente ID {cliente_id}.")
        return False