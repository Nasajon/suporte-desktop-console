import argparse
import time
import uuid

from typing import Any, Dict, List

from suporte_console.command import Command


class UnificaGruposEmpresariaisCommand(Command):

    # Dicionário entre a numeração dos cadastros, e suas respectivas tabelas de associação com os dados:
    CADASTROS = {
        0: 'conjuntosprodutos',
        1: 'conjuntosunidades',
        2: 'conjuntoscombustiveis',
        3: 'conjuntosservicos',
        4: 'conjuntosclassificacoesparticipantes',
        5: 'conjuntosfichas',
        6: 'conjuntosclientes',
        7: 'conjuntosfornecedores',
        8: 'conjuntostransportadoras',
        9: 'conjuntosvendedores',
        10: 'conjuntosservicosdecatalogos',
        11: 'conjuntosmodeloscontratos',
        12: 'conjuntostecnicos',
        13: 'conjuntosrubricas',
        14: 'conjuntosrepresentantescomerciais',
        15: 'conjuntosrepresentantestecnicos',
        16: 'conjuntosprospects'
    }

    # Queries para ajustar apontamento dos grupos_empresariais
    QUERIES_GRUPOS_EMPRESARIAIS = [
        'update compras.acordoscompras set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update compras.itenscompras set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update contabilizacao.classificacaofinanceiraporcontas set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update crm.documenttemplate set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update crm.documenttemplate set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update crm.listascontatos set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update crm.negociosoperacoes set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update crm.old_propostas set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update crm.pagemaster set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update crm.pagemaster set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update crm.segmentosatuacao set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update crm.tabelas_de_precos set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update estoque.atributos set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update estoque.categoriasdeprodutos set id_grupo_empresarial=:grupo_destino where id_grupo_empresarial in :grupos_origem',
        'update estoque.figurastributarias set id_grupo_empresarial=:grupo_destino where id_grupo_empresarial in :grupos_origem',
        'update estoque.itensparacalculosaldo set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update estoque.operacoes set id_grupo_empresarial=:grupo_destino where id_grupo_empresarial in :grupos_origem',
        'update estoque.perfil_importacao set id_grupo_empresarial=:grupo_destino where id_grupo_empresarial in :grupos_origem',
        'update estoque.perfiltrib_est set id_grupo_empresarial=:grupo_destino where id_grupo_empresarial in :grupos_origem',
        'update estoque.perfiltrib_fed set id_grupo_empresarial=:grupo_destino where id_grupo_empresarial in :grupos_origem',
        'update estoque.producao_modelos set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update estoque.producao_modelos_processos set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update estoque.rotas set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.ajustes set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.aplicacoes set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.arquivoretornoserasa set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update financas.arquivosremessaserasa set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update financas.benspatrimoniais set familia=:grupo_destino where familia in :grupos_origem',
        'update financas.cenariosorcamentarios set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.centroscustos set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.chequescustodias set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update financas.classificacoesfinanceiras set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.clientesenviadosserasa set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update financas.configuracoescontasinvestimentos set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.configuracoesfluxocaixa set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.configuracoesintegracoesconciliadoras set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.configuracoesterceirizacao set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update financas.contas set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update financas.contratos set familia=:grupo_destino where familia in :grupos_origem',
        'update financas.contratoscartoes set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.gruposcotgruposemp set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.historicosanalisesinadimplencias set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.inadimplenciasexcecoesclientes set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update financas.lancamentostituloscoberturascontas set idgrupoempresarial=:grupo_destino where idgrupoempresarial in :grupos_origem',
        'update financas.processamentoscontratos set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.projetos set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.rateiospadrao set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.rateiospadraorestricoes set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.reguascobrancas set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.reguascobrancas set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.relatoriosgruposclassificadores set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.renegociacoescontratos set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update financas.resgates set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.restricoescobrancas set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.restricoescobrancas set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update financas.vinculosgruposempresariais set grupoempresarialorigem=:grupo_destino where grupoempresarialorigem in :grupos_origem',
        'update financas.vinculosgruposempresariais set grupoempresarialvinculado=:grupo_destino where grupoempresarialvinculado in :grupos_origem',
        'update locacoes.lancamentomultiploativos set grupoempresarial_id=:grupo_destino where grupoempresarial_id in :grupos_origem',
        'update locacoes.modalidadesdepagamento set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update ns.atributos set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update ns.configuracoes set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update ns.configuracoescategoriasporclassfinan set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update ns.configuracoesnumeracoesdnf set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update ns.destinos_sincronizacao_gruposempresariais set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update ns.df_docfis set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update ns.documentosgeddetalhes set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update ns.emailsenviados set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update ns.empresas set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update ns.faixasdecreditos set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update ns.filtrosformularios set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update ns.gruposempresariaisacessosusuarios set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update ns.gruposempresariaiscadastros set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update ns.limitesdecreditosacessos set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update ns.limitesdecreditosconfiguracoes set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update ns.limitesdecreditosentidadesempresariais set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update ns.locaisdeuso set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update ns.pendencias set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update ns.regrasvencimentosclientes set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update ns.tabelas_precos_de_entregas set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update ns.usuarios set ultimogrupo=:grupo_destino where ultimogrupo in :grupos_origem',
        'update servicos.catalogosdeofertas set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update servicos.categoriasfuncoes set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update servicos.componentes set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update servicos.composicoes set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update servicos.custosmaodeobra set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update servicos.docpedidosvendasservicos set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update servicos.eventoscontratos set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update servicos.funcoes set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update servicos.gruposdecomponentes set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update servicos.gruposdeservicos set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update servicos.nfsoperacoes set grupoempresarial_id=:grupo_destino where grupoempresarial_id in :grupos_origem',
        'update servicos.objetosservicosbase set grupoempresarial_id=:grupo_destino where grupoempresarial_id in :grupos_origem',
        'update servicos.orcamentos set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update servicos.ordensservicos set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update servicos.pedidosvendasservicos set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update servicos.receitasdespesas set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update servicos.rpss set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update servicos.servicostecnicos set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update servicos.tiposfuncoes set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update servicos.tiposprojetos set grupoempresarial_id=:grupo_destino where grupoempresarial_id in :grupos_origem',
        'update servicos.tiposservicos set id_grupoempresarial=:grupo_destino where id_grupoempresarial in :grupos_origem',
        'update servicos.variaveisorcamentarias set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem',
        'update util.indices_gruposempresariais set grupoempresarial=:grupo_destino where grupoempresarial in :grupos_origem'
    ]

    def ajusta_persmissoes_group_nasajon(self):
        """
        Roda a função ns.permissoes, para ajustar as permissões do BD.
        """

        try:
            sql = f"select * from ns.permissoes()"
            self.db_adapter.execute(sql)
        except Exception as e:
            self.log_warning(
                f"Erro manipulando permissões do BD clonado: {e}")

    def is_modo_empresa(self):
        """
        Retorna true se o BD estiver em modo empresa, e false, caso contrário.
        """

        sql = """
        SELECT VALOR as modo FROM NS.CONFIGURACOES WHERE CAMPO = 1 AND APLICACAO = 0
        """

        modo = self.db_adapter.execute_query_first_result(sql)

        if str(modo['modo']) == '0':
            return True
        else:
            return False

    def get_conjuntos_grupos(self, codigos_grupos: List[str]) -> List[Dict[str, Any]]:
        sql = f"""
        select
            gemp.grupoempresarial, ec.cadastro, ec.conjunto
        from
            ns.estabelecimentosconjuntos as ec
            join ns.estabelecimentos as est on (est.estabelecimento = ec.estabelecimento)
            join ns.empresas as emp on (emp.empresa = est.empresa)
            join ns.gruposempresariais as gemp on (gemp.grupoempresarial = emp.grupoempresarial)
        where
            gemp.codigo in :codigos_grupos
            and ec.cadastro <> 13
        	and ec.conjunto <> coalesce((select conjunto from ns.conjuntos where cadastro=7 and codigo='11'), '00000000-0000-0000-0000-000000000000'::UUID)
        group by
            gemp.grupoempresarial, ec.cadastro, ec.conjunto
        """

        return self.db_adapter.execute_query(
            sql, codigos_grupos=tuple(codigos_grupos))

    def migra_dados_conjunto(self, tipo_cadastro: int, conjunto_origem: uuid.UUID, conjunto_destino: uuid.UUID):

        tabela = UnificaGruposEmpresariaisCommand.CADASTROS[tipo_cadastro]
        sql = f"update {tabela} set conjunto=:conjunto_destino where conjunto=:conjunto_origem"
        self.db_adapter.execute(
            sql, conjunto_origem=conjunto_origem, conjunto_destino=conjunto_destino)

    def migra_estabelecimentos_conjunto(self, tipo_cadastro: int, conjunto_origem: uuid.UUID, conjunto_destino: uuid.UUID):

        sql = f"update ns.estabelecimentosconjuntos set conjunto=:conjunto_destino where conjunto=:conjunto_origem and cadastro=:tipo_cadastro"
        self.db_adapter.execute(
            sql, conjunto_origem=conjunto_origem, conjunto_destino=conjunto_destino, tipo_cadastro=tipo_cadastro)

    def excluir_conjunto(self, tipo_cadastro: int, conjunto: uuid.UUID):

        sql = f"delete from ns.conjuntos where conjunto=:conjunto and cadastro=:tipo_cadastro"
        self.db_adapter.execute(sql, conjunto=conjunto,
                                tipo_cadastro=tipo_cadastro)

    def get_ids_grupos(self, codigos_grupos: List[str]) -> List[uuid.UUID]:
        sql = f"""
        select
            gemp.grupoempresarial
        from
            ns.gruposempresariais as gemp
        where
            gemp.codigo in :codigos_grupos
        """

        lista = self.db_adapter.execute_query(
            sql, codigos_grupos=tuple(codigos_grupos))

        return [g['grupoempresarial'] for g in lista]

    def excluir_grupos_empresariais(self, ids_grupos_empresariais: List[uuid.UUID]):

        sql = f"delete from ns.gruposempresariais where grupoempresarial in :grupos"
        self.db_adapter.execute(sql, grupos=tuple(ids_grupos_empresariais))

    def backup_grupos_empresariais(self):

        # Criando tabela de backup
        try:
            sql = "create table gruposempresariais_bkp as select * from ns.gruposempresariais"
            self.db_adapter.execute(sql)
        except Exception as e:
            self.log_warning(f'Problema ao criar tabela de backup: {e}')

        # Tratando do owner da tabela de backup
        try:
            sql = f"alter table gruposempresariais_bkp owner to group_nasajon;"
            self.db_adapter.execute(sql)
        except:
            pass

    def main(self, pars: List[str]):
        # self.config_logger()

        start_time = time.time()
        try:
            # Parsing command line arguments
            parser = argparse.ArgumentParser(
                description="""Utilitário para unificar vários grupos empresariais num único grupo de destino.""")

            parser.add_argument(
                "-r", "--origem", help="Lista dos códigos dos grupos empresariais de origem, os quais deixarão de existir (separados por vírgulas).", required=True)

            parser.add_argument(
                "-i", "--destino", help="Código do grupo empresarial de destino, que receberá todas os dados dos grupos de origem.", required=True)

            # Guardando os parâmetros de entrada em variáveis para uso interno
            args, _ = parser.parse_known_args(pars)
            grupos_origem = args.origem.split(',')
            grupos_origem = [c for c in grupos_origem if c.strip() != '']

            grupo_destino = args.destino

            # Notificando início do processamento
            self.log(
                f"Unificando os grupos empresariais de origem: {grupos_origem}, para o grupo de destino {grupo_destino}")

            # Ajustando as permissões do BD
            self.log('Ajustando permissoes do group nasajon')
            self.ajusta_persmissoes_group_nasajon()

            if self.is_modo_empresa():
                # Fazendo backup da estrutura de conjuntos:
                self.log('Copiando a estrutura de conjuntos')
                self.backup_conjuntos()

                # Recuperando os conjuntos (por tipo de cadastro), do grupo empresarial de destino
                conjuntos_destino = self.get_conjuntos_grupos([grupo_destino])
                conjuntos_destino = {c['cadastro']: c['conjunto']
                                     for c in conjuntos_destino}

                # Recuperando os conjuntos (por tipo de cadastro), dos grupos empresariais de origem
                conjuntos_origem = self.get_conjuntos_grupos(grupos_origem)

                # Migrando os dados de cada conjunto de origem, para o destino correspondente
                for conjunto in conjuntos_origem:
                    # Migrando os dados
                    self.migra_dados_conjunto(
                        conjunto['cadastro'], conjunto['conjunto'], conjuntos_destino[conjunto['cadastro']])

                    # Migrando os estabelecimentos
                    self.migra_estabelecimentos_conjunto(
                        conjunto['cadastro'], conjunto['conjunto'], conjuntos_destino[conjunto['cadastro']])

                    # Excluíndo o conjunto de origem
                    self.excluir_conjunto(
                        conjunto['cadastro'], conjunto['conjunto'])

            # Fazendo backup dos grupos_empresariais
            self.backup_grupos_empresariais()

            # Recuperando os ids dos grupos empresariais envolvidos
            ids_grupos_origem = self.get_ids_grupos(grupos_origem)
            id_grupo_destino = self.get_ids_grupos(grupo_destino)[0]

            # Reponterando as tabelas que apontavam para os grupos empresariais de origem para o destino
            for sql in self.QUERIES_GRUPOS_EMPRESARIAIS:
                self.db_adapter.execute(
                    sql, grupo_destino=id_grupo_destino, grupos_origem=tuple(ids_grupos_origem))

            # Excluindo os grupos_empresariais
            self.excluir_grupos_empresariais(ids_grupos_origem)

            # Notificando o fim do processamento
            self.log('Concluindo a unificação dos grupos empresariais')
        finally:
            self.log("--- TEMPO TOTAL GERAL %s seconds ---" %
                     (time.time() - start_time))
