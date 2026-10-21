from datetime import datetime, timedelta
from config.settings import TEMP_PATH
from config.db import Session
from services.documento import substituir_placeholders
from repositories.municipios_assinantes_repository import MunicipioAssinanteRepository
from repositories.entregas_repository import EntregasRepository
from models.entregas_model import Entrega
from models.empresas_model import Empresa
from config.sessao import Sessao
from exceptions.municipio_exception import MunicipioNaoCadastradoException
from exceptions.obra_fora_tecnica_exception import ObraNaoEstaNaTecnica


class EntregasDoTrabalho():
    def __init__(self, tecnica: dict, empresa: Empresa, destino: str):
        self.tecnica = tecnica
        self.empresa = empresa
        self.destino = destino

    
    def gerar_documento(self, obra: str):

        try:
            substituicoes, sob = self._definir_variaveis(obra)
        except MunicipioNaoCadastradoException as e:
            raise e
        except ObraNaoEstaNaTecnica as e:
            raise e
        except Exception as e:
            raise e(f'Erro ao definir as variáveis da obra: [{obra}]')

        nome = f'{obra}_{sob}_entrega_do_trabalho_assinado_enel'
        caminho_saida = TEMP_PATH / f'{nome}.docx'

        try:
            substituir_placeholders(
                substituicoes, caminho_saida, nome, self.destino
            )
        except Exception as e:
            raise Exception(f'Erro ao gerar o documento da obra: {obra}')


    def _buscar_municipio(self, municipio):
        with Session() as session:
            repo = MunicipioAssinanteRepository(session)
            
            registro = repo.buscar_por_municipio(municipio)

        return registro


    def _salvar_banco(self, dados: dict):
        with Session() as session:
            repo = EntregasRepository(session)
            entrega = Entrega()
            entrega.trabalho = dados.get('trabalho')
            entrega.empresa = dados.get('empresa')
            entrega.municipio = dados.get('municipio')
            entrega.endereco = dados.get('endereco')
            entrega.prazo = dados.get('prazo')
            entrega.usuarios_id = dados.get('usuario')
            repo.adicionar(entrega)
            session.commit()

            return entrega.id


    def _definir_variaveis(self, obra: str):

        dados: dict =  self.tecnica.get(obra)

        if dados is None:
            raise ObraNaoEstaNaTecnica(f'A obra {obra} não está na técnica')
        
        municipio = dados.get('MUNICIPIO')
        sob = dados.get('NUM_SOB')
        ceco = dados.get('CECO')
        projeto = dados.get('PROJETO_INVESTIMENTO')
        endereco = dados.get('ENDERECO')
        pdl = dados.get('NUMERO_PDL')
        mt = float(dados.get('TOTAL_MT').replace('.', '').replace(',', '.'))
        bt = float(dados.get('TOTAL_BT').replace('.', '').replace(',', '.'))
        trafos = int(dados.get('QTDE_TRAFOS').replace('.', ''))
        postes = int(dados.get('QTDE_POSTES').replace('.', ''))
        latitude = dados.get('LATITUDE')
        longitude = dados.get('LONGITUDE')
        dias = int(dados.get('PRAZO_EXECUCAO'))
            
        assinantes = self._buscar_municipio(municipio)

        if assinantes is None:
            raise  MunicipioNaoCadastradoException(f'Não existe o município {municipio} no banco de dados')

        responsavel_contratante = assinantes.aprovador_nome
        matricula_contratante = assinantes.aprovador_matricula
        email_contratante = assinantes.aprovador_email
        telefone_contratante = assinantes.aprovador_telefone
        regional = assinantes.regional
        elaborador = assinantes.assinatura_elaborador
        aprovador = assinantes.aprovador_assinatura


        empresa = self.empresa.razao_social
       
        cnpj = self.empresa.cnpj
        contrato = self.empresa.contrato
        responsavel = self.empresa.responsavel
        email = self.empresa.email
        telefone = self.empresa.telefone
        sigla = self.empresa.sigla

        hoje = datetime.now()

        prazo = hoje + timedelta(days=(2 * dias))
        #prazo = prazo.strftime('%d/%m/%Y')

        banco = {
            'trabalho': obra,
            'empresa': empresa,
            'municipio': municipio,
            'endereco': endereco,
            'prazo': prazo.date(),
            'usuario': Sessao.get_id()
        }

        id_entrega = self._salvar_banco(banco)

        intervencao = 'MT' if dias > 60 else 'BT'

        cabecalho = f'ETR - {intervencao} - {ceco} - {sigla} - {id_entrega}'

        descricao = (
            f'OT: {obra} / OS: {sob} / PDL: {pdl} / {municipio}, {endereco}'
        )

        atividades = self._definir_atividades(
            projeto, endereco, postes, trafos, bt, mt
        )

        coordenadas = f'COORDENADAS DA OBRA: {latitude}, {longitude}'

        data_sub = hoje - timedelta(minutes=45)
        data1 = data_sub.strftime('%d/%m/%Y')
        hora1 = data_sub.strftime('%H:%M')
        data2 = hoje.strftime('%d/%m/%Y')
        hora2 = hoje.strftime('%H:%M')

        substituicoes = {
            '{{cabecalho}}': str(cabecalho),
            '{{empresa}}': str(empresa),
            '{{cnpj}}': str(cnpj),
            '{{contrato}}': str(contrato),
            '{{responsavel}}': str(responsavel),
            '{{email}}': str(email),
            '{{telefone}}': str(telefone),
            '{{endereco}}': str(endereco),
            '{{descricao}}': str(descricao),
            '{{atividades}}': str(atividades),
            '{{coordenadas}}': str(coordenadas),
            '{{prazo}}': prazo.strftime('%d/%m/%Y'),
            '{{data1}}': str(data1),
            '{{hora1}}': str(hora1),
            '{{data2}}': str(data2),
            '{{hora2}}': str(hora2),
            '{{responsavel_contratante}}': str(responsavel_contratante),
            '{{matricula_contratante}}': str(matricula_contratante),
            '{{email_contratante}}': str(email_contratante),
            '{{telefone_contratante}}': str(telefone_contratante),
            '{{regional}}': str(regional),
            '{{elaborador}}': str(elaborador),
            '{{aprovador}}': str(aprovador)
        }

        return substituicoes, sob
    

    def _definir_atividades(self, projeto: str, endereco: str, postes: int, trafos:int,
                       bt: str, mt:str) -> str:
        """Define as atividades a serem realizadas."""
        def atividade(texto1: str, qtd: int | float, texto2: str) -> str:
            texto = f'\u2022 ATIVIDADE {qtd_ativ}: {texto1} {qtd} {texto2}.\n'

            return texto

        qtd_ativ = 1
        atividades = ''

        tele = 'CCIMTCBSTTTNST_REA-14347 - Proyecto Telecontrol Latam - Coelce'
        if projeto == tele:
            atividades += f'\u2022 ATIVIDADE {qtd_ativ}: {endereco}\n'
            qtd_ativ += 1

        if postes > 0:
            if int(postes) == 1:
                atividades += atividade('IMPLANTAÇÃO DE', postes, 'POSTE')
            else:
                atividades += atividade('IMPLANTAÇÃO DE', postes, 'POSTES')
            qtd_ativ += 1

        if trafos > 0:
            if int(trafos) == 1:
                atividades += atividade('INSTALAÇÃO DE', postes, 'TRAFO')
            else:
                atividades += atividade('INSTALAÇÃO DE', postes, 'TRAFOS')
            qtd_ativ += 1

        if int(bt) > 0:
            atividades += atividade('EXTENSÃO DE', bt, 'M DE BT')
            qtd_ativ += 1

        if int(mt) > 0:
            atividades += atividade('EXTENSÃO DE', mt, 'M DE MT')
            qtd_ativ += 1

        return atividades
