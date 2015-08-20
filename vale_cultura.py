import getpass
import json
from flask import Flask, jsonify, abort
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.restful.representations.json import output_json
from sqlalchemy import *
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import DeclarativeMeta
from collections import defaultdict
from models import *

app = Flask(__name__)
api = Api(app)

engine = create_engine('mssql+pymssql://user:senha@minc10/dbminc', encoding='cp1252')
meta = MetaData()
meta.reflect(bind=engine)
beneficiarias = Table('S_BENEFICIARIA', meta, autoload=True, autoload_with=engine)
pj = Table('CORPORATIVO.S_PESSOA_JURIDICA', meta, autoload=True, autoload_with=engine)
natureza_juridica = Table('CORPORATIVO.S_NATUREZA_JURIDICA', meta, autoload=True, autoload_with=engine)
operadora = Table('S_OPERADORA', meta, autoload=True, autoload_with=engine)
pf = Table('CORPORATIVO.S_PESSOA', meta, autoload=True, autoload_with=engine)
situacao = Table('S_SITUACAO', meta, autoload=True, autoload_with=engine)
tipo_situacao = Table('S_TIPO_SITUACAO', meta, autoload=True, autoload_with=engine)
# endereco = Table('CORPORATIVO.S_ENDERECO', meta, autoload=True, autoload_with=engine)
# logradouro = Table('CORPORATIVO.S_LOGRADOURO', meta, autoload=True, autoload_with=engine)
# municipio = Table('CORPORATIVO.S_MUNICIPIO', meta, autoload=True, autoload_with=engine)
session = Session(bind=engine)


class Beneficiarias(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('cnpj', type=str)
        super(Beneficiarias, self).__init__()

    def get(self):
        valores = session.query(beneficiarias, pj.c.ID_PESSOA_JURIDICA,
            pj.c.NR_CNPJ,
            pf.c.ID_PESSOA, pf.c.CD_TIPO_ABRANGENCIA, situacao.c.ID_PESSOA,
            tipo_situacao.c.DS_TIPO_SITUACAO).join(pj).join(pf).join(situacao)\
            .join(tipo_situacao)
        colunas = [valores.column_descriptions[i]['name'] for i in range(len(valores.column_descriptions))]
        args = self.reqparse.parse_args()
        if args['cnpj']:
            valores = valores.filter(pj.c.NR_CNPJ == args['cnpj'])
        valores = valores.all()
        result = []
        for i in range(len(valores)):
            temp = {}
            for j in range(len(valores[i])):
                temp.update({colunas[j]:valores[i][j]})
            result.append(temp)
        return jsonify(beneficiarias = result)

class BeneficiariaPorCNPJ(Resource):
    def get(self, cnpj):
        valores = session.query(
            beneficiarias.c.ID_BENEFICIARIA.label('id'),
            beneficiarias.c.DT_INSCRICAO.label('data_inscricao'),
            natureza_juridica.c.DS_NATUREZA_JURIDICA.label('natureza_juridica'),
            pj.c.NR_CNPJ.label('cnpj'),
            pj.c.NR_INSCRICAO_ESTADUAL.label('inscricao_estadual'),
            pj.c.NM_RAZAO_SOCIAL.label('razao_social'),
            pj.c.NM_FANTASIA.label('nome_fantasia'),
            # logradouro.c.SG_UF.label('uf'),
            # municipio.c.NM_MUNICIPIO.label('municipio'),
            # municipio.c.CD_MUNICIPIO_IBGE.label('codigo_ibge'),
            # municipio.c.CD_MUNICIPIO_CORREIO.label('codigo_correio'),
            tipo_situacao.c.DS_TIPO_SITUACAO.label('situacao')).join(pj)\
            .join(natureza_juridica)\
            .join(pf)\
            .join(situacao)\
            .join(tipo_situacao)
            # .join(endereco)\
            # .join(logradouro)\
            # .join(municipio)\
        colunas = [valores.column_descriptions[i]['name'] for i in range(len(valores.column_descriptions))]
        valores = valores.filter(pj.c.NR_CNPJ == cnpj).order_by(desc(situacao.c.DT_SITUACAO)).limit(1)
        if not valores.count():
            abort(404)
        valores = valores.all()
        result = []
        for i in range(len(valores)):
            temp = {}
            for j in range(len(valores[i])):
                temp.update({colunas[j]:valores[i][j]})
            result.append(temp)
        return jsonify(beneficiaria = result)

api.add_resource(Beneficiarias, '/vale-cultura/v1/beneficiarias', endpoint='beneficiarias')
api.add_resource(BeneficiariaPorCNPJ, '/vale-cultura/doc/beneficiaria/<cnpj>', endpoint='beneficiaria')
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
