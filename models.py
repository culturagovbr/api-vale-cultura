# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, SmallInteger, String, Table, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql.base import MONEY
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class SARQUIVOOPERADORA(Base):
    __tablename__ = 'S_ARQUIVO_OPERADORA'

    ID_ARQUIVO = Column(Integer, primary_key=True)
    ID_OPERADORA = Column(ForeignKey('S_OPERADORA.ID_OPERADORA'), nullable=False)
    DS_CAMINHO_ARQUIVO = Column(String(70, 'Latin1_General_CI_AI'))
    DS_ARQUIVO = Column(String(300, 'Latin1_General_CI_AI'))
    DT_UPLOAD_ARQUIVO = Column(DateTime)

    S_OPERADORA = relationship('SOPERADORA')


class SCARGACARTAOTRABALHADOR(Base):
    __tablename__ = 'S_CARGA_CARTAO_TRABALHADOR'
    __table_args__ = (
        Index('UK_S_CARGA_CARTAO_TRABALHADOR', 'ID_OPERADORA', 'NR_OPERACAO', 'CT_OPERACAO', unique=True),
        Index('IX_S_CARGA_CARTAO_TRABALHADOR_ID_TRABALHADOR_ID_BENEFICIARIA_ID_OPERADORA', 'ID_TRABALHADOR', 'ID_BENEFICIARIA', 'ID_OPERADORA')
    )

    ID_CARGA_CARTAO_TRABALHADOR = Column(Integer, primary_key=True)
    NR_OPERACAO = Column(String(14, 'Latin1_General_CI_AI'), nullable=False)
    ID_BENEFICIARIA = Column(ForeignKey('S_BENEFICIARIA.ID_BENEFICIARIA'), nullable=False, index=True)
    ID_OPERADORA = Column(ForeignKey('S_OPERADORA.ID_OPERADORA'), nullable=False, index=True)
    ID_TRABALHADOR = Column(ForeignKey('S_TRABALHADOR.ID_TRABALHADOR'), nullable=False, index=True)
    DT_CARREGAMENTO = Column(DateTime, nullable=False)
    VL_CARREGAMENTO = Column(MONEY, nullable=False)
    DT_ENVIO = Column(DateTime, nullable=False)
    NM_ARQUIVO = Column(String(100, 'Latin1_General_CI_AI'))
    DT_ATUALIZACAO = Column(DateTime, nullable=False)
    CT_OPERACAO = Column(Integer)

    S_BENEFICIARIA = relationship('SBENEFICIARIA')
    S_OPERADORA = relationship('SOPERADORA')
    S_TRABALHADOR = relationship('STRABALHADOR')


class SCONSUMO(Base):
    __tablename__ = 'S_CONSUMO'
    __table_args__ = (
        Index('UK_S_CONSUMO', 'ID_BENEFICIARIA', 'ID_OPERADORA', 'ID_RECEBEDORA', 'ID_TRABALHADOR', 'NR_TRANSACAO', unique=True),
    )

    ID_CONSUMO = Column(Integer, primary_key=True)
    ID_BENEFICIARIA = Column(ForeignKey('S_BENEFICIARIA.ID_BENEFICIARIA'), nullable=False, index=True)
    ID_OPERADORA = Column(ForeignKey('S_OPERADORA.ID_OPERADORA'), nullable=False, index=True)
    ID_RECEBEDORA = Column(Integer, nullable=False, index=True)
    ID_TRABALHADOR = Column(ForeignKey('S_TRABALHADOR.ID_TRABALHADOR'), nullable=False, index=True)
    NR_TRANSACAO = Column(String(30, 'Latin1_General_CI_AI'))
    DT_CONSUMO = Column(DateTime, nullable=False)
    VL_CONSUMO = Column(MONEY, nullable=False)
    DT_REGISTRO = Column(DateTime, nullable=False)

    S_BENEFICIARIA = relationship('SBENEFICIARIA')
    S_OPERADORA = relationship('SOPERADORA')
    S_TRABALHADOR = relationship('STRABALHADOR')


class SCONSUMOPRODUTO(Base):
    __tablename__ = 'S_CONSUMO_PRODUTO'

    ID_CONSUMO_PRODUTO = Column(Integer, primary_key=True)
    ID_CONSUMO = Column(ForeignKey('S_CONSUMO.ID_CONSUMO'), nullable=False)
    DS_CONSUMO_PRODUTO = Column(String(100, 'Latin1_General_CI_AI'), nullable=False)
    VL_CONSUMO_PRODUTO = Column(MONEY, nullable=False)
    QT_CONSUMO_PRODUTO = Column(Integer, nullable=False)

    S_CONSUMO = relationship('SCONSUMO')


class SCONSUMOTRABALHADOR(Base):
    __tablename__ = 'S_CONSUMO_TRABALHADOR'
    __table_args__ = (
        Index('UK_S_CONSUMO_TRABALHADOR_2', 'ID_OPERADORA', 'NR_OPERACAO', unique=True),
        Index('UK_S_CONSUMO_TRABALHADOR', 'ID_BENEFICIARIA', 'ID_OPERADORA', 'ID_RECEBEDORA', 'ID_TRABALHADOR', 'NR_TRANSACAO', unique=True)
    )

    ID_CONSUMO_TRABALHADOR = Column(Integer, primary_key=True)
    NR_OPERACAO = Column(String(14, 'Latin1_General_CI_AI'), nullable=False)
    ID_BENEFICIARIA = Column(ForeignKey('S_BENEFICIARIA.ID_BENEFICIARIA'), nullable=False, index=True)
    ID_OPERADORA = Column(ForeignKey('S_OPERADORA.ID_OPERADORA'), nullable=False, index=True)
    ID_RECEBEDORA = Column(ForeignKey('S_RECEBEDORA.ID_RECEBEDORA'), nullable=False, index=True)
    ID_TRABALHADOR = Column(ForeignKey('S_TRABALHADOR.ID_TRABALHADOR'), nullable=False, index=True)
    NR_TRANSACAO = Column(Unicode(30), nullable=False)
    DT_CONSUMO = Column(DateTime, nullable=False)
    VL_CONSUMO = Column(MONEY, nullable=False)
    DT_ENVIO = Column(DateTime, nullable=False)
    NM_ARQUIVO = Column(String(100, 'Latin1_General_CI_AI'))
    DT_ATUALIZACAO = Column(DateTime, nullable=False)

    S_BENEFICIARIA = relationship('SBENEFICIARIA')
    S_OPERADORA = relationship('SOPERADORA')
    S_RECEBEDORA = relationship('SRECEBEDORA')
    S_TRABALHADOR = relationship('STRABALHADOR')


t_S_DBF = Table(
    'S_DBF', metadata,
    Column('TP_REGISTRO', Integer, nullable=False),
    Column('NR_ANO', String(4, 'Latin1_General_CI_AI'), nullable=False),
    Column('NR_CNPJ_OPERADORA', String(14, 'Latin1_General_CI_AI'), nullable=False),
    Column('NR_CNPJ_BENEFICIARIA', String(14, 'Latin1_General_CI_AI'), nullable=False),
    Column('VL_GERADO', MONEY),
    Column('DS_INFORMACAO', String(250, 'Latin1_General_CI_AI'))
)


class SFAIXASALARIALBENEFICIARIA(Base):
    __tablename__ = 'S_FAIXA_SALARIAL_BENEFICIARIA'

    ID_BENEFICIARIA = Column(ForeignKey('S_BENEFICIARIA.ID_BENEFICIARIA'), primary_key=True, nullable=False)
    ID_TIPO_FAIXA_SALARIAL = Column(ForeignKey('S_TIPO_FAIXA_SALARIAL.ID_TIPO_FAIXA_SALARIAL'), primary_key=True, nullable=False)
    QT_TRABALHADOR_FAIXA_SALARIAL = Column(Integer)

    S_BENEFICIARIA = relationship('SBENEFICIARIA')
    S_TIPO_FAIXA_SALARIAL = relationship('STIPOFAIXASALARIAL')


class SPAGAMENTOOPERADORA(Base):
    __tablename__ = 'S_PAGAMENTO_OPERADORA'
    __table_args__ = (
        Index('UK_S_PAGAMENTO_OPERADORA', 'NR_OPERACAO', 'ID_OPERADORA', unique=True),
    )

    ID_PAGAMENTO_OPERADORA = Column(Integer, primary_key=True)
    NR_OPERACAO = Column(String(14, 'Latin1_General_CI_AI'), nullable=False)
    ID_BENEFICIARIA = Column(ForeignKey('S_BENEFICIARIA.ID_BENEFICIARIA'), nullable=False, index=True)
    ID_OPERADORA = Column(ForeignKey('S_OPERADORA.ID_OPERADORA'), nullable=False, index=True)
    DT_PAGAMENTO_OPERADORA = Column(DateTime, nullable=False)
    VL_PAGAMENTO_OPERADORA = Column(MONEY, nullable=False)
    DT_ENVIO = Column(DateTime, nullable=False)
    NM_ARQUIVO = Column(String(100, 'Latin1_General_CI_AI'))
    DT_ATUALIZACAO = Column(DateTime, nullable=False)

    S_BENEFICIARIA = relationship('SBENEFICIARIA')
    S_OPERADORA = relationship('SOPERADORA')


class SRECEBEDORAOPERADORA(Base):
    __tablename__ = 'S_RECEBEDORA_OPERADORA'
    __table_args__ = (
        Index('UK_S_RECEBEDORA_OPERADORA', 'ID_OPERADORA', 'NR_OPERACAO', unique=True),
    )

    ID_RECEBEDORA = Column(ForeignKey('S_RECEBEDORA.ID_RECEBEDORA'), primary_key=True, nullable=False)
    ID_OPERADORA = Column(ForeignKey('S_OPERADORA.ID_OPERADORA'), primary_key=True, nullable=False)
    NR_OPERACAO = Column(String(14, 'Latin1_General_CI_AI'), nullable=False)
    DT_ENVIO = Column(DateTime, nullable=False)
    NM_ARQUIVO = Column(String(100, 'Latin1_General_CI_AI'))
    DT_ATUALIZACAO = Column(DateTime, nullable=False)

    S_OPERADORA = relationship('SOPERADORA')
    S_RECEBEDORA = relationship('SRECEBEDORA')


class SSITUACAO(Base):
    __tablename__ = 'S_SITUACAO'

    ID_SITUACAO = Column(Integer, primary_key=True, index=True)
    ID_TIPO_SITUACAO = Column(ForeignKey('S_TIPO_SITUACAO.ID_TIPO_SITUACAO'), nullable=False, index=True)
    ID_PESSOA = Column(ForeignKey('CORPORATIVO.S_PESSOA.ID_PESSOA'), nullable=False, index=True)
    ID_USUARIO = Column(ForeignKey('SEGURANCA.S_USUARIO.ID_USUARIO'))
    DT_SITUACAO = Column(DateTime, nullable=False)
    DS_JUSTIFICATIVA = Column(String(255, 'Latin1_General_CI_AI'), nullable=False)
    TP_ENTIDADE_VALE_CULTURA = Column(String(1, 'Latin1_General_CI_AI'), nullable=False, index=True)

    S_PESSOA = relationship('SPESSOA')
    S_TIPO_SITUACAO = relationship('STIPOSITUACAO')
    S_USUARIO = relationship('SUSUARIO')


class STIPOFAIXASALARIAL(Base):
    __tablename__ = 'S_TIPO_FAIXA_SALARIAL'

    ID_TIPO_FAIXA_SALARIAL = Column(Integer, primary_key=True)
    DS_TIPO_FAIXA_SALARIAL = Column(String(150, 'Latin1_General_CI_AI'), nullable=False)
    NR_PERCENTUAL_DESCONTO = Column(String(50, 'Latin1_General_CI_AI'))
    ST_TIPO_FAIXA_SALARIAL = Column(String(1, 'Latin1_General_CI_AI'), nullable=False)


class STIPOSITUACAO(Base):
    __tablename__ = 'S_TIPO_SITUACAO'

    ID_TIPO_SITUACAO = Column(Integer, primary_key=True)
    DS_TIPO_SITUACAO = Column(String(300, 'Latin1_General_CI_AI'))
    ST_TIPO_SITUACAO = Column(String(1, 'Latin1_General_CI_AI'), nullable=False)


class STRABALHADORBENEFICIARIA(Base):
    __tablename__ = 'S_TRABALHADOR_BENEFICIARIA'
    __table_args__ = (
        Index('UK_S_TRABALHADOR_BENEFICIARIA', 'ID_BENEFICIARIA', 'ID_OPERADORA', 'ID_TRABALHADOR', 'NR_ANO_REFERENCIA', 'NR_MES_REFERENCIA', unique=True),
    )

    ID_TRABALHADOR_BENEFICIARIA = Column(Integer, primary_key=True)
    ID_BENEFICIARIA = Column(ForeignKey('S_BENEFICIARIA.ID_BENEFICIARIA'), nullable=False, index=True)
    ID_OPERADORA = Column(ForeignKey('S_OPERADORA.ID_OPERADORA'), nullable=False, index=True)
    ID_TRABALHADOR = Column(ForeignKey('S_TRABALHADOR.ID_TRABALHADOR'), nullable=False, index=True)
    NR_MES_REFERENCIA = Column(Integer, nullable=False)
    NR_ANO_REFERENCIA = Column(SmallInteger, nullable=False)
    DT_ENVIO = Column(DateTime, nullable=False)

    S_BENEFICIARIA = relationship('SBENEFICIARIA')
    S_OPERADORA = relationship('SOPERADORA')
    S_TRABALHADOR = relationship('STRABALHADOR')


class STRABALHADOREMPREGOBENEFICIO(Base):
    __tablename__ = 'S_TRABALHADOR_EMPREGO_BENEFICIO'

    ID_TRABALHADOR = Column(ForeignKey('S_TRABALHADOR.ID_TRABALHADOR'), primary_key=True, nullable=False)
    ID_BENEFICIARIA = Column(ForeignKey('S_BENEFICIARIA.ID_BENEFICIARIA'), primary_key=True, nullable=False)
    VL_SALARIO = Column(MONEY)
    DT_ADMISSAO = Column(Date)
    DT_DESLIGAMENTO = Column(Date)
    DT_INICIO_BENEFICIO = Column(Date)
    DT_FIM_BENEFICIO = Column(Date)
    NR_CARTAO_BENEFICIO = Column(Integer)

    S_BENEFICIARIA = relationship('SBENEFICIARIA')
    S_TRABALHADOR = relationship('STRABALHADOR')


class SVALORREPASSEBENEFICIARIAOPERADORA(Base):
    __tablename__ = 'S_VALOR_REPASSE_BENEFICIARIA_OPERADORA'

    ID_OPERADORA = Column(ForeignKey('S_OPERADORA.ID_OPERADORA'), primary_key=True, nullable=False)
    ID_BENEFICIARIA = Column(ForeignKey('S_BENEFICIARIA.ID_BENEFICIARIA'), primary_key=True, nullable=False)
    NR_ANO = Column(Integer, nullable=False)
    VL_REPASSE = Column(MONEY, nullable=False)

    S_BENEFICIARIA = relationship('SBENEFICIARIA')
    S_OPERADORA = relationship('SOPERADORA')


class SMESOREGIAO(Base):
    __tablename__ = 'S_MESOREGIAO'
    __table_args__ = {'schema': 'CORPORATIVO'}

    ID_MESOREGIAO = Column(Integer, primary_key=True)
    SG_UF = Column(ForeignKey('CORPORATIVO.S_UF.SG_UF'), nullable=False)
    NM_MESOREGIAO = Column(String(100, 'Latin1_General_CI_AI'), nullable=False)
    CD_MESOREGIAO = Column(String(2, 'Latin1_General_CI_AI'))

    S_UF = relationship('SUF')


class SMICROREGIAO(Base):
    __tablename__ = 'S_MICROREGIAO'
    __table_args__ = {'schema': 'CORPORATIVO'}

    ID_MICROREGIAO = Column(Integer, primary_key=True)
    ID_MESOREGIAO = Column(ForeignKey('CORPORATIVO.S_MESOREGIAO.ID_MESOREGIAO'), nullable=False)
    NM_MICROREGIAO = Column(String(100, 'Latin1_General_CI_AI'), nullable=False)
    CD_MICROREGIAO = Column(String(3, 'Latin1_General_CI_AI'))

    S_MESOREGIAO = relationship('SMESOREGIAO')


class SMUNICIPIO(Base):
    __tablename__ = 'S_MUNICIPIO'
    __table_args__ = {'schema': 'CORPORATIVO'}

    ID_MUNICIPIO = Column(Integer, primary_key=True)
    SG_PAIS = Column(ForeignKey('CORPORATIVO.S_PAIS.SG_PAIS'), nullable=False)
    SG_UF = Column(ForeignKey('CORPORATIVO.S_UF.SG_UF'), nullable=False, index=True)
    ID_MICROREGIAO = Column(ForeignKey('CORPORATIVO.S_MICROREGIAO.ID_MICROREGIAO'))
    ID_MUNICIPIO_SUBORDINACAO = Column(ForeignKey('CORPORATIVO.S_MUNICIPIO.ID_MUNICIPIO'))
    CD_SITUACAO_MUNICIPIO = Column(ForeignKey('CORPORATIVO.S_SITUACAO_MUNICIPIO.CD_SITUACAO_MUNICIPIO'))
    CD_DDD = Column(Integer)
    NM_MUNICIPIO = Column(String(100, 'Latin1_General_CI_AI'), nullable=False)
    CD_MUNICIPIO_IBGE = Column(String(7, 'Latin1_General_CI_AI'), nullable=False)
    CD_MUNICIPIO_BACEN = Column(String(6, 'Latin1_General_CI_AI'))
    CD_MUNICIPIO_RF = Column(String(4, 'Latin1_General_CI_AI'))
    CD_MUNICIPIO_CORREIO = Column(Integer)
    CD_MUNICIPIO_SIAPE = Column(Integer)
    CD_MICROREGIAO = Column(String(3, 'Latin1_General_CI_AI'))
    ST_CAPITAL = Column(String(1, 'Latin1_General_CI_AI'))
    TP_LOCALIDADE = Column(String(1, 'Latin1_General_CI_AI'))

    S_SITUACAO_MUNICIPIO = relationship('SSITUACAOMUNICIPIO')
    S_MICROREGIAO = relationship('SMICROREGIAO')
    parent = relationship('SMUNICIPIO', remote_side=[ID_MUNICIPIO])
    S_PAI = relationship('SPAI')
    S_UF = relationship('SUF')


class SNATUREZAJURIDICA(Base):
    __tablename__ = 'S_NATUREZA_JURIDICA'
    __table_args__ = {'schema': 'CORPORATIVO'}

    CD_NATUREZA_JURIDICA = Column(String(4, 'Latin1_General_CI_AI'), primary_key=True)
    DS_NATUREZA_JURIDICA = Column(String(200, 'Latin1_General_CI_AI'), nullable=False)


class SPAI(Base):
    __tablename__ = 'S_PAIS'
    __table_args__ = {'schema': 'CORPORATIVO'}

    SG_PAIS = Column(String(3, 'Latin1_General_CI_AI'), primary_key=True)
    NM_PAIS = Column(String(50, 'Latin1_General_CI_AI'), nullable=False)
    CD_DDI = Column(String(20, 'Latin1_General_CI_AI'))
    SG_PAIS_ISO = Column(String(2, 'Latin1_General_CI_AI'))


class SPESSOA(Base):
    __tablename__ = 'S_PESSOA'
    __table_args__ = {'schema': 'CORPORATIVO'}

    ID_PESSOA = Column(Integer, primary_key=True)
    CD_TIPO_ABRANGENCIA = Column(ForeignKey('CORPORATIVO.S_TIPO_ABRANGENCIA.CD_TIPO_ABRANGENCIA'), nullable=False)
    CD_TIPO_PESSOA = Column(ForeignKey('CORPORATIVO.S_TIPO_PESSOA.CD_TIPO_PESSOA'), nullable=False)
    SG_PAIS = Column(ForeignKey('CORPORATIVO.S_PAIS.SG_PAIS'), nullable=False)
    DT_REGISTRO = Column(Date, nullable=False)

    S_TIPO_ABRANGENCIA = relationship('STIPOABRANGENCIA')
    S_TIPO_PESSOA = relationship('STIPOPESSOA')
    S_PAI = relationship('SPAI')


class SPESSOAFISICA(SPESSOA):
    __tablename__ = 'S_PESSOA_FISICA'
    __table_args__ = {'schema': 'CORPORATIVO'}

    ID_PESSOA_FISICA = Column(ForeignKey('CORPORATIVO.S_PESSOA.ID_PESSOA'), primary_key=True)
    ID_MUNICIPIO_NATURAL = Column(ForeignKey('CORPORATIVO.S_MUNICIPIO.ID_MUNICIPIO'))
    CD_ESTADO_CIVIL = Column(String(2, 'Latin1_General_CI_AI'))
    CD_ESCOLARIDADE = Column(Integer)
    NM_PESSOA_FISICA = Column(String(100, 'Latin1_General_CI_AI'), nullable=False)
    NR_CPF = Column(String(11, 'Latin1_General_CI_AI'), nullable=False, unique=True)
    NM_MAE = Column(String(100, 'Latin1_General_CI_AI'))
    NM_PAI = Column(String(100, 'Latin1_General_CI_AI'))
    DT_NASCIMENTO = Column(Date)
    SG_SEXO = Column(String(10, 'Latin1_General_CI_AI'))
    DS_TIPO_SANGUINEO = Column(String(3, 'Latin1_General_CI_AI'))
    ST_DOADOR = Column(String(10, 'Latin1_General_CI_AI'))
    TP_SITUACAO_CADASTRAL = Column(String(1, 'Latin1_General_CI_AI'))
    TP_RESIDENTE_EXTERIOR = Column(String(1, 'Latin1_General_CI_AI'))

    S_MUNICIPIO = relationship('SMUNICIPIO')


class STRABALHADOR(SPESSOAFISICA):
    __tablename__ = 'S_TRABALHADOR'

    ID_TRABALHADOR = Column(ForeignKey('CORPORATIVO.S_PESSOA_FISICA.ID_PESSOA_FISICA'), primary_key=True)


class SPESSOAJURIDICA(SPESSOA):
    __tablename__ = 'S_PESSOA_JURIDICA'
    __table_args__ = {'schema': 'CORPORATIVO'}

    ID_PESSOA_JURIDICA = Column(ForeignKey('CORPORATIVO.S_PESSOA.ID_PESSOA'), primary_key=True)
    CD_NATUREZA_JURIDICA = Column(ForeignKey('CORPORATIVO.S_NATUREZA_JURIDICA.CD_NATUREZA_JURIDICA'), index=True)
    ID_TIPO_LUCRO = Column(ForeignKey('CORPORATIVO.S_TIPO_LUCRO.ID_TIPO_LUCRO'))
    NR_CNPJ = Column(String(14, 'Latin1_General_CI_AI'), nullable=False, unique=True)
    NR_INSCRICAO_ESTADUAL = Column(String(20, 'Latin1_General_CI_AI'))
    NM_RAZAO_SOCIAL = Column(String(150, 'Latin1_General_CI_AI'), nullable=False)
    NM_FANTASIA = Column(String(150, 'Latin1_General_CI_AI'))
    NR_CEI = Column(String(11, 'Latin1_General_CI_AI'))

    S_NATUREZA_JURIDICA = relationship('SNATUREZAJURIDICA')
    S_TIPO_LUCRO = relationship('STIPOLUCRO')


class SOPERADORA(SPESSOAJURIDICA):
    __tablename__ = 'S_OPERADORA'

    ID_OPERADORA = Column(ForeignKey('CORPORATIVO.S_PESSOA_JURIDICA.ID_PESSOA_JURIDICA'), primary_key=True)
    DT_INSCRICAO = Column(DateTime)
    NR_COMPROVANTE_INSCRICAO = Column(Integer)
    NR_CERTIFICADO = Column(Integer)


class SBENEFICIARIA(SPESSOAJURIDICA):
    __tablename__ = 'S_BENEFICIARIA'

    ID_BENEFICIARIA = Column(ForeignKey('CORPORATIVO.S_PESSOA_JURIDICA.ID_PESSOA_JURIDICA'), primary_key=True)
    ID_OPERADORA = Column(ForeignKey('S_OPERADORA.ID_OPERADORA'), nullable=False, index=True)
    DT_INSCRICAO = Column(DateTime, nullable=False)
    NR_COMPROVANTE_INSCRICAO = Column(Integer)
    NR_CERTIFICADO = Column(Integer)
    ST_DIVULGAR_DADOS = Column(String(1, 'Latin1_General_CI_AI'), nullable=False)
    ST_ATUALIZADO_OPERADORA = Column(String(1, 'Latin1_General_CI_AI'))

    # S_OPERADORA = relationship('SOPERADORA')


class SRECEBEDORA(SPESSOAJURIDICA):
    __tablename__ = 'S_RECEBEDORA'

    ID_RECEBEDORA = Column(ForeignKey('CORPORATIVO.S_PESSOA_JURIDICA.ID_PESSOA_JURIDICA'), primary_key=True)


class SREGIAO(Base):
    __tablename__ = 'S_REGIAO'
    __table_args__ = {'schema': 'CORPORATIVO'}

    SG_REGIAO = Column(String(2, 'Latin1_General_CI_AI'), primary_key=True)
    NM_REGIAO = Column(String(40, 'Latin1_General_CI_AI'), nullable=False)
    CD_REGIAO_IBGE = Column(String(2, 'Latin1_General_CI_AI'))


class SSITUACAOMUNICIPIO(Base):
    __tablename__ = 'S_SITUACAO_MUNICIPIO'
    __table_args__ = {'schema': 'CORPORATIVO'}

    CD_SITUACAO_MUNICIPIO = Column(String(1, 'Latin1_General_CI_AI'), primary_key=True)
    DS_SITUACAO_MUNICIPIO = Column(String(30, 'Latin1_General_CI_AI'), nullable=False)


class STIPOABRANGENCIA(Base):
    __tablename__ = 'S_TIPO_ABRANGENCIA'
    __table_args__ = {'schema': 'CORPORATIVO'}

    CD_TIPO_ABRANGENCIA = Column(String(1, 'Latin1_General_CI_AI'), primary_key=True)
    DS_TIPO_ABRANGENCIA = Column(String(50, 'Latin1_General_CI_AI'), nullable=False)


class STIPOLUCRO(Base):
    __tablename__ = 'S_TIPO_LUCRO'
    __table_args__ = {'schema': 'CORPORATIVO'}

    ID_TIPO_LUCRO = Column(Integer, primary_key=True)
    DS_TIPO_LUCRO = Column(String(100, 'Latin1_General_CI_AI'), nullable=False)


class STIPOPESSOA(Base):
    __tablename__ = 'S_TIPO_PESSOA'
    __table_args__ = {'schema': 'CORPORATIVO'}

    CD_TIPO_PESSOA = Column(String(1, 'Latin1_General_CI_AI'), primary_key=True)
    DS_TIPO_PESSOA = Column(String(50, 'Latin1_General_CI_AI'), nullable=False)


class SUF(Base):
    __tablename__ = 'S_UF'
    __table_args__ = {'schema': 'CORPORATIVO'}

    SG_UF = Column(String(2, 'Latin1_General_CI_AI'), primary_key=True)
    SG_REGIAO = Column(ForeignKey('CORPORATIVO.S_REGIAO.SG_REGIAO'))
    NM_UF = Column(String(100, 'Latin1_General_CI_AI'), nullable=False)
    CD_UF_RF = Column(String(4, 'Latin1_General_CI_AI'))
    CD_UF_IBGE = Column(String(2, 'Latin1_General_CI_AI'))

    S_REGIAO = relationship('SREGIAO')


class SUSUARIO(Base):
    __tablename__ = 'S_USUARIO'
    __table_args__ = {'schema': 'SEGURANCA'}

    ID_USUARIO = Column(Integer, primary_key=True)
    ID_PESSOA_FISICA = Column(ForeignKey('CORPORATIVO.S_PESSOA_FISICA.ID_PESSOA_FISICA'), nullable=False, unique=True)
    DS_LOGIN = Column(String(30, 'Latin1_General_CI_AI'), nullable=False, unique=True)
    DS_SENHA = Column(String(50, 'Latin1_General_CI_AI'), nullable=False)
    DS_SENHA_TEMP = Column(String(50, 'Latin1_General_CI_AI'))
    DT_EXPIRACAO_SENHA = Column(Date)
    DT_VALIDADE_SENHA = Column(Date)
    DT_CRIACAO_USUARIO = Column(Date)
    ST_USUARIO = Column(String(1, 'Latin1_General_CI_AI'), nullable=False)
    TP_ORIGEM = Column(String(1, 'Latin1_General_CI_AI'))
    DS_TERMO = Column(Unicode(2000))

    S_PESSOA_FISICA = relationship('SPESSOAFISICA')
