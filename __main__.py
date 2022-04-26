import argparse
import datetime
import logging
import sys
import time

from suporte_console.database_config import create_pool
from suporte_console.db_adapter2 import DBAdapter2

from suporte_console.converte_modo_empresa.converte_modo_empresa_command import ConverteModoEmpresaCommand
from suporte_console.exclusao_empresas.exclusao_empresas_command import ExclusaoEmpresasCommand

COMMANDS = {
    'exclusao_empresas': ExclusaoEmpresasCommand,
    'converte_modo_empresa': ConverteModoEmpresaCommand
}


def config_logger():
    # Configuring logger
    data = datetime.datetime.now()
    log_file_name = f"suporte-console - {data.year}-{data.month}-{data.day}-{data.hour}-{data.minute}.log"

    logger = logging.getLogger('suporte_console')
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(log_file_name)

    console_format = logging.Formatter(
        '%(name)s - %(levelname)s - %(message)s')
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


def clone_database(
    database_default_name: str,
    database_name: str,
    database_user: str,
    database_pass: str,
    database_host: str,
    database_port: str,
    new_database: str
):
    try:
        start_time = time.time()
        logger = logging.getLogger('suporte_console')
        logger.info('Clonando o banco de dados...')

        pool = create_pool(
            database_user,
            database_pass,
            database_host,
            database_port,
            database_default_name,
            1,
            'AUTOCOMMIT'
        )

        # Abrindo conexao com o BD
        with pool.connect() as conn:
            db_adapter = DBAdapter2(conn, False)

            sql = f"create database {new_database} with owner={database_user} template={database_name}"
            db_adapter.execute(sql)
    finally:
        logger.info("- Tempo clonando o banco %s seconds -" %
                    (time.time() - start_time))


def internal_main(
    database_name: str,
    database_user: str,
    database_pass: str,
    database_host: str,
    database_port: str,
    command: str,
    database_default_name: str,
    new_database: str
):
    logger = logging.getLogger('suporte_console')
    logger.info('Abrindo conexão com o banco de dados...')

    start_time = time.time()
    try:
        if new_database is not None:
            clone_database(
                database_default_name,
                database_name,
                database_user,
                database_pass,
                database_host,
                database_port,
                new_database
            )
            database_name = new_database

        # Criando o pool de conexoes
        pool = create_pool(
            database_user,
            database_pass,
            database_host,
            database_port,
            database_name,
            1
        )

        # Abrindo conexao com o BD
        with pool.connect() as conn:
            # Instanciando o DBAdapter
            db_adapter = DBAdapter2(conn)

            # Resolvendo os passos a executar
            commands_list = [k for k in COMMANDS]
            if not(command in commands_list):
                logger.warning(
                    f"Parâmetro command inválido {command}. Use: {commands_list}")
                sys.exit(4)

            # Executando o comando
            command_obj = COMMANDS[command](db_adapter, command)
            command_obj.main()

    finally:
        logger.info("--- TEMPO TOTAL GERAL %s seconds ---" %
                    (time.time() - start_time))


def main():

    try:
        # Configuring logger
        config_logger()
        logger = logging.getLogger('suporte_console')

        # Initialize parser
        parser = argparse.ArgumentParser(
            description="""Utilitário para execução de comandos de suporte ao BD do ERP 2 (via linha de comando: console)."""
        )

        # Adding arguments
        parser.add_argument(
            "-d", "--database", help="Nome do banco de dados para conexão", required=True)
        parser.add_argument(
            "-n", "--new_database", help="Nome do banco de dados criado pelo procedimento", required=False)
        parser.add_argument(
            "-f", "--database_default_name", help="Nome do banco de dados default para conexão, ao criar uma cópia do BD a ser tratado.", required=False, default='postgres')
        parser.add_argument(
            "-u", "--user", help="Usuário para conexão com o banco de dados", required=False, default='postgres')
        parser.add_argument(
            "-p", "--password", help="Senha para conexão com o banco de dados", required=False, default='postgres')
        parser.add_argument(
            "-t", "--host", help="IP ou nome do servidor do banco de dados", required=False, default='localhost')
        parser.add_argument(
            "-o", "--port", help="Porta para conexão com o banco de dados", required=False, default='5432')

        parser.add_argument(
            "-c", "--command", help="Comando a ser executado.", required=True)

        # Read arguments from command line
        args = parser.parse_args()

        internal_main(
            args.database,
            args.user,
            args.password,
            args.host,
            args.port,
            args.command,
            args.database_default_name,
            args.new_database
        )
        sys.exit(0)
    except Exception as e:
        logger.exception(
            f'Erro fatal. Mensagem original do erro {e}')
        sys.exit(5)


if __name__ == '__main__':
    main()