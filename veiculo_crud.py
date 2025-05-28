# veiculo_crud.py
# Este arquivo contém as funções CRUD (Create, Read, Update, Delete) para a entidade 'veiculos'.

from db_utils import executar_query
from cliente_crud import consultar_cliente_por_id # Usado para verificar se o cliente proprietário existe

def adicionar_veiculo(conexao, marca, modelo, ano, placa, cliente_id):
    """
    Adiciona um novo veículo ao banco de dados, associado a um cliente existente.

    Args:
        conexao: Objeto de conexão com o banco.
        marca (str): Marca do veículo.
        modelo (str): Modelo do veículo.
        ano (int): Ano do veículo.
        placa (str): Placa do veículo (deve ser única).
        cliente_id (int): ID do cliente proprietário do veículo.

    Returns:
        int or None: O ID do veículo adicionado se sucesso, None caso contrário.
    """
    # Verifica se o cliente proprietário existe
    cliente_proprietario = consultar_cliente_por_id(conexao, cliente_id)
    if not cliente_proprietario:
        print(f"Cliente com ID {cliente_id} não encontrado. Não é possível adicionar o veículo.")
        return None

    query = "INSERT INTO veiculos (marca, modelo, ano, placa, cliente_id) VALUES (%s, %s, %s, %s, %s)"
    params = (marca, modelo, ano, placa, cliente_id)
    try:
        veiculo_id = executar_query(conexao, query, params, commit=True)
        if veiculo_id:
            print(f"Veículo {marca} {modelo} (Placa: {placa}) adicionado com sucesso (ID: {veiculo_id}) "
                  f"para o cliente '{cliente_proprietario['nome']}'.")
            return veiculo_id
        else:
            # Isso pode acontecer se a placa já existir (devido à restrição UNIQUE)
            # ou outro erro na execução da query.
            print(f"Falha ao adicionar veículo {marca} {modelo}. Verifique se a placa já está cadastrada.")
            return None
    except Exception as e:
        print(f"Erro inesperado ao adicionar veículo: {e}")
        return None


def listar_veiculos(conexao):
    """
    Lista todos os veículos cadastrados, incluindo informações do proprietário.

    Args:
        conexao: Objeto de conexão com o banco.

    Returns:
        list or None: Uma lista de dicionários representando os veículos, ou None se não houver veículos ou erro.
    """
    # Query SQL com JOIN para buscar dados das tabelas 'veiculos' e 'clientes'
    query = """
        SELECT
            v.id, v.marca, v.modelo, v.ano, v.placa,
            c.nome AS nome_cliente, c.cpf AS cpf_cliente
        FROM veiculos v
        JOIN clientes c ON v.cliente_id = c.id
    """
    veiculos = executar_query(conexao, query, fetch_all=True)
    if veiculos:
        print("\n--- Lista de Veículos ---")
        for veiculo in veiculos:
            print(f"ID: {veiculo['id']}, Marca: {veiculo['marca']}, Modelo: {veiculo['modelo']}, "
                  f"Ano: {veiculo['ano']}, Placa: {veiculo['placa']}, "
                  f"Proprietário: {veiculo['nome_cliente']} (CPF: {veiculo['cpf_cliente']})")
        print("------------------------")
    elif veiculos == []: # Lista vazia
        print("Nenhum veículo cadastrado.")
    else: # None, erro na consulta
        print("Falha ao listar veículos.")
    return veiculos

def consultar_veiculo_por_placa(conexao, placa):
    """
    Consulta um veículo específico pela sua placa.

    Args:
        conexao: Objeto de conexão com o banco.
        placa (str): Placa do veículo a ser consultado.

    Returns:
        dict or None: Um dicionário com os dados do veículo se encontrado, None caso contrário.
    """
    query = """
        SELECT
            v.id, v.marca, v.modelo, v.ano, v.placa, v.cliente_id,
            c.nome AS nome_cliente, c.cpf AS cpf_cliente
        FROM veiculos v
        JOIN clientes c ON v.cliente_id = c.id
        WHERE v.placa = %s
    """
    params = (placa,)
    veiculo = executar_query(conexao, query, params, fetch_one=True)
    if veiculo:
        print("\n--- Veículo Encontrado ---")
        print(f"ID: {veiculo['id']}, Marca: {veiculo['marca']}, Modelo: {veiculo['modelo']}, "
              f"Ano: {veiculo['ano']}, Placa: {veiculo['placa']}, "
              f"Proprietário: {veiculo['nome_cliente']} (CPF: {veiculo['cpf_cliente']}), ID Cliente: {veiculo['cliente_id']}")
        print("------------------------")
    else:
        print(f"Veículo com placa '{placa}' não encontrado.")
    return veiculo

def consultar_veiculo_por_id(conexao, veiculo_id):
    """
    Consulta um veículo específico pelo seu ID.
    Útil internamente para verificações.

    Args:
        conexao: Objeto de conexão com o banco.
        veiculo_id (int): ID do veículo a ser consultado.

    Returns:
        dict or None: Um dicionário com os dados do veículo se encontrado, None caso contrário.
    """
    query = "SELECT id, marca, modelo, ano, placa, cliente_id FROM veiculos WHERE id = %s"
    params = (veiculo_id,)
    return executar_query(conexao, query, params, fetch_one=True)

def atualizar_veiculo(conexao, veiculo_id, marca=None, modelo=None, ano=None, cliente_id_novo=None):
    """
    Atualiza os dados de um veículo existente.
    A placa não é atualizável por ser um identificador único.

    Args:
        conexao: Objeto de conexão com o banco.
        veiculo_id (int): ID do veículo a ser atualizado.
        marca (str, optional): Nova marca do veículo.
        modelo (str, optional): Novo modelo do veículo.
        ano (int, optional): Novo ano do veículo.
        cliente_id_novo (int, optional): Novo ID do cliente proprietário.

    Returns:
        bool: True se a atualização foi bem-sucedida, False caso contrário.
    """
    veiculo_existente = consultar_veiculo_por_id(conexao, veiculo_id)
    if not veiculo_existente:
        print(f"Veículo com ID {veiculo_id} não encontrado. Não é possível atualizar.")
        return False

    campos_para_atualizar = []
    params_valores = []

    if marca is not None and marca.strip() != "":
        campos_para_atualizar.append("marca = %s")
        params_valores.append(marca)
    if modelo is not None and modelo.strip() != "":
        campos_para_atualizar.append("modelo = %s")
        params_valores.append(modelo)
    if ano is not None: # ano pode ser 0, mas aqui assumimos que None significa não alterar
        try:
            # Validar se o ano é um inteiro antes de adicionar
            ano_int = int(ano)
            campos_para_atualizar.append("ano = %s")
            params_valores.append(ano_int)
        except ValueError:
            print("Ano inválido fornecido para atualização. O ano não será alterado.")

    if cliente_id_novo is not None:
        # Verifica se o novo cliente proprietário existe
        novo_proprietario = consultar_cliente_por_id(conexao, cliente_id_novo)
        if not novo_proprietario:
            print(f"Novo cliente proprietário com ID {cliente_id_novo} não encontrado. "
                  "O proprietário do veículo não será alterado.")
        else:
            campos_para_atualizar.append("cliente_id = %s")
            params_valores.append(cliente_id_novo)

    if not campos_para_atualizar:
        print("Nenhum dado válido fornecido para atualização do veículo.")
        return False

    query = f"UPDATE veiculos SET {', '.join(campos_para_atualizar)} WHERE id = %s"
    params_valores.append(veiculo_id) # Adiciona o ID do veículo ao final

    resultado_update = executar_query(conexao, query, tuple(params_valores), commit=True)
    if resultado_update is not None:
        print(f"Dados do veículo ID {veiculo_id} atualizados com sucesso.")
        return True
    else:
        print(f"Falha ao atualizar dados do veículo ID {veiculo_id}.")
        return False

def excluir_veiculo(conexao, veiculo_id):
    """
    Exclui um veículo do banco de dados.

    Args:
        conexao: Objeto de conexão com o banco.
        veiculo_id (int): ID do veículo a ser excluído.

    Returns:
        bool: True se a exclusão foi bem-sucedida, False caso contrário.
    """
    veiculo_existente = consultar_veiculo_por_id(conexao, veiculo_id)
    if not veiculo_existente:
        print(f"Veículo com ID {veiculo_id} não encontrado. Não é possível excluir.")
        return False

    # Confirmação do usuário
    confirmacao = input(f"Tem certeza que deseja excluir o veículo {veiculo_existente['marca']} "
                        f"{veiculo_existente['modelo']} (Placa: {veiculo_existente['placa']})? (s/N): ").strip().lower()
    if confirmacao != 's':
        print("Exclusão cancelada pelo usuário.")
        return False

    query = "DELETE FROM veiculos WHERE id = %s"
    params = (veiculo_id,)
    resultado_delete = executar_query(conexao, query, params, commit=True)
    if resultado_delete is not None:
        print(f"Veículo ID {veiculo_id} ('{veiculo_existente['marca']} {veiculo_existente['modelo']}') excluído com sucesso.")
        return True
    else:
        print(f"Falha ao excluir veículo ID {veiculo_id}.")
        return False