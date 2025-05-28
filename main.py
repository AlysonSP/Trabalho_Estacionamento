# main.py
# Arquivo principal da aplicação de console para gerenciamento de estacionamento.
# Contém os menus e a lógica de interação com o usuário.

import re # Importa o módulo de expressões regulares para validação de placa
from db_utils import conectar_db # Função para conectar ao banco de dados
import cliente_crud             # Módulo com funções CRUD para clientes
import veiculo_crud             # Módulo com funções CRUD para veículos

def validar_placa(placa):
    """
    Valida o formato da placa.
    Aceita formatos como AAA-1234 (antigo), ABC1234 (antigo sem hífen)
    e ABC1D23 (Mercosul Brasil).
    Retorna True se válida, False caso contrário.
    """
    # Padrão antigo: LLL-NNNN ou LLLNNNN
    padrao_antigo = r"^[A-Z]{3}-?\d{4}$"
    # Padrão Mercosul (Brasil): LLLNLNN
    padrao_mercosul = r"^[A-Z]{3}\d[A-Z]\d{2}$"

    if re.match(padrao_antigo, placa, re.IGNORECASE) or re.match(padrao_mercosul, placa, re.IGNORECASE):
        return True
    return False

def exibir_menu_principal():
    """Exibe o menu principal e retorna a escolha do usuário."""
    print("\n--- Sistema de Controle de Estacionamento ---")
    print("1. Gerenciar Clientes")
    print("2. Gerenciar Veículos")
    print("0. Sair do Sistema")
    return input("Escolha uma opção: ").strip()

def menu_gerenciar_clientes(conexao):
    """Exibe o menu de gerenciamento de clientes e processa as opções."""
    while True:
        print("\n--- Gerenciar Clientes ---")
        print("1. Adicionar Novo Cliente")
        print("2. Listar Todos os Clientes")
        print("3. Consultar Cliente por CPF")
        print("4. Atualizar Dados do Cliente")
        print("5. Excluir Cliente")
        print("0. Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            nome = input("Nome completo do cliente: ").strip()
            endereco = input("Endereço do cliente: ").strip()
            while True:
                cpf = input("CPF (11 dígitos, apenas números): ").strip()
                if len(cpf) == 11 and cpf.isdigit():
                    break
                print("CPF inválido. Deve conter exatamente 11 dígitos numéricos.")
            telefone = input("Telefone do cliente: ").strip()
            if nome and cpf: # Campos obrigatórios
                 cliente_crud.adicionar_cliente(conexao, nome, endereco, cpf, telefone)
            else:
                print("Nome e CPF são obrigatórios.")
        elif opcao == '2':
            cliente_crud.listar_clientes(conexao)
        elif opcao == '3':
            cpf = input("Digite o CPF do cliente a consultar (11 dígitos): ").strip()
            if len(cpf) == 11 and cpf.isdigit():
                cliente_crud.consultar_cliente_por_cpf(conexao, cpf)
            else:
                print("CPF inválido para consulta.")
        elif opcao == '4':
            cliente_id_str = input("Digite o ID do cliente que deseja atualizar: ").strip()
            if cliente_id_str.isdigit():
                cliente_id = int(cliente_id_str)
                cliente_atual = cliente_crud.consultar_cliente_por_id(conexao, cliente_id)
                if not cliente_atual:
                    print(f"Cliente com ID {cliente_id} não encontrado.")
                    continue

                print("Deixe o campo em branco se não desejar alterá-lo.")
                nome_atual = cliente_atual.get('nome', 'N/A')
                endereco_atual = cliente_atual.get('endereco', 'N/A')
                telefone_atual = cliente_atual.get('telefone', 'N/A')

                nome_novo = input(f"Novo nome (atual: {nome_atual}): ").strip()
                endereco_novo = input(f"Novo endereço (atual: {endereco_atual}): ").strip()
                telefone_novo = input(f"Novo telefone (atual: {telefone_atual}): ").strip()
                
                # Passa None se o campo ficou em branco, caso contrário passa o valor
                nome_param = nome_novo if nome_novo else None
                endereco_param = endereco_novo if endereco_novo else None
                telefone_param = telefone_novo if telefone_novo else None
                
                cliente_crud.atualizar_cliente(conexao, cliente_id, nome_param, endereco_param, telefone_param)
            else:
                print("ID do cliente inválido.")
        elif opcao == '5':
            cliente_id_str = input("Digite o ID do cliente que deseja excluir: ").strip()
            if cliente_id_str.isdigit():
                cliente_crud.excluir_cliente(conexao, int(cliente_id_str))
            else:
                print("ID do cliente inválido.")
        elif opcao == '0':
            print("Retornando ao Menu Principal...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_gerenciar_veiculos(conexao):
    """Exibe o menu de gerenciamento de veículos e processa as opções."""
    while True:
        print("\n--- Gerenciar Veículos ---")
        print("1. Adicionar Novo Veículo")
        print("2. Listar Todos os Veículos")
        print("3. Consultar Veículo por Placa")
        print("4. Atualizar Dados do Veículo")
        print("5. Excluir Veículo")
        print("0. Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            marca = input("Marca do veículo: ").strip()
            modelo = input("Modelo do veículo: ").strip()
            ano = None
            while True:
                ano_str = input("Ano do veículo (ex: 2023): ").strip()
                if ano_str.isdigit() and len(ano_str) == 4:
                    ano = int(ano_str)
                    break
                print("Ano inválido. Deve ser um número de 4 dígitos.")
            placa = ""
            while True:
                placa_input = input("Placa do veículo (formatos: AAA-1234, ABC1234, ABC1D23): ").strip().upper()
                if validar_placa(placa_input):
                     placa = placa_input
                     break
                print("Formato de placa inválido. Tente novamente.")

            print("\n--- Clientes Cadastrados ---")
            clientes_disponiveis = cliente_crud.listar_clientes(conexao)
            if not clientes_disponiveis: # Checa se a lista é None ou vazia
                print("Nenhum cliente cadastrado. Adicione um cliente antes de adicionar um veículo.")
                continue
            
            cliente_id_str = input("Digite o ID do cliente proprietário: ").strip()

            if not (marca and modelo and placa and cliente_id_str.isdigit()):
                print("Marca, modelo, placa e ID do cliente são obrigatórios e o ID deve ser um número.")
                continue
            veiculo_crud.adicionar_veiculo(conexao, marca, modelo, ano, placa, int(cliente_id_str))
        elif opcao == '2':
            veiculo_crud.listar_veiculos(conexao)
        elif opcao == '3':
            placa = input("Digite a placa do veículo a consultar: ").strip().upper()
            if validar_placa(placa):
                veiculo_crud.consultar_veiculo_por_placa(conexao, placa)
            else:
                print("Formato de placa inválido para consulta.")
        elif opcao == '4':
            veiculo_id_str = input("Digite o ID do veículo que deseja atualizar: ").strip()
            if veiculo_id_str.isdigit():
                veiculo_id = int(veiculo_id_str)
                veiculo_atual = veiculo_crud.consultar_veiculo_por_id(conexao, veiculo_id)
                if not veiculo_atual:
                    print(f"Veículo com ID {veiculo_id} não encontrado.")
                    continue

                print("Deixe o campo em branco se não desejar alterá-lo.")
                marca_atual = veiculo_atual.get('marca', 'N/A')
                modelo_atual = veiculo_atual.get('modelo', 'N/A')
                ano_atual_val = veiculo_atual.get('ano', 'N/A')
                cliente_id_prop_atual = veiculo_atual.get('cliente_id', 'N/A')


                marca_nova = input(f"Nova marca (atual: {marca_atual}): ").strip()
                modelo_novo = input(f"Novo modelo (atual: {modelo_atual}): ").strip()
                ano_novo_str = input(f"Novo ano (atual: {ano_atual_val}): ").strip()
                
                ano_param = None
                if ano_novo_str: # Se algo foi digitado para o ano
                    if ano_novo_str.isdigit() and len(ano_novo_str) == 4:
                        ano_param = int(ano_novo_str)
                    else:
                        print("Formato de ano inválido. O ano não será alterado.")
                
                marca_param = marca_nova if marca_nova else None
                modelo_param = modelo_novo if modelo_novo else None

                cliente_id_novo_param = None
                mudar_proprietario = input("Deseja alterar o proprietário do veículo? (s/N): ").strip().lower()
                if mudar_proprietario == 's':
                    print("\n--- Clientes Cadastrados ---")
                    clientes_disponiveis_upd = cliente_crud.listar_clientes(conexao)
                    if not clientes_disponiveis_upd:
                        print("Nenhum cliente cadastrado para selecionar como novo proprietário.")
                    else:
                        cliente_id_novo_str = input(f"Novo ID do cliente proprietário (atual: {cliente_id_prop_atual}): ").strip()
                        if cliente_id_novo_str.isdigit():
                            cliente_id_novo_param = int(cliente_id_novo_str)
                        else:
                            print("ID do novo proprietário inválido. O proprietário não será alterado.")
                
                veiculo_crud.atualizar_veiculo(conexao, veiculo_id, marca_param, modelo_param, ano_param, cliente_id_novo_param)
            else:
                print("ID do veículo inválido.")
        elif opcao == '5':
            veiculo_id_str = input("Digite o ID do veículo que deseja excluir: ").strip()
            if veiculo_id_str.isdigit():
                veiculo_crud.excluir_veiculo(conexao, int(veiculo_id_str))
            else:
                print("ID do veículo inválido.")
        elif opcao == '0':
            print("Retornando ao Menu Principal...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Ponto de entrada da aplicação
if __name__ == "__main__":
    # Tenta conectar ao banco de dados
    conexao_db = conectar_db()

    if conexao_db:
        print("Conexão com o banco de dados estabelecida com sucesso!")
        try:
            while True:
                escolha_principal = exibir_menu_principal()
                if escolha_principal == '1':
                    menu_gerenciar_clientes(conexao_db)
                elif escolha_principal == '2':
                    menu_gerenciar_veiculos(conexao_db)
                elif escolha_principal == '0':
                    print("Saindo do sistema de estacionamento. Até logo!")
                    break
                else:
                    print("Opção principal inválida. Por favor, tente novamente.")
        finally:
            # Garante que a conexão com o banco de dados seja fechada ao sair
            if conexao_db and conexao_db.is_connected():
                conexao_db.close()
                print("Conexão com o banco de dados encerrada.")
    else:
        print("Falha ao conectar ao banco de dados. O sistema não pode ser iniciado.")
        print("Verifique as configurações em 'db_config.py' (especialmente a SENHA) e se o servidor MySQL está em execução.")