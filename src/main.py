from flask import Flask, request, jsonify
from core.sql_generator import generate_sql
from core.vector_db import search_documents, add_document

app = Flask(__name__)

@app.route('/')
def hello():
    return "API do Sistema de Auditoria está no ar!"

@app.route('/generate-sql', methods=['POST'])
def handle_generate_sql():
    data = request.json
    # Em um projeto real, o schema viria de um catálogo de dados
    schema_info = "Tabela: transacoes (id INT, valor DECIMAL, cliente_id INT, status STRING)"
    sql = generate_sql(data['query'], schema_info)
    return jsonify({"sql_query": sql})

@app.route('/search-docs', methods=['POST'])
def handle_search_docs():
    data = request.json
    results = search_documents(data['query'], required_role=data.get('role', 'public'))
    return jsonify(results)

# Função principal para o Cloud Functions
def main(request):
    # Isso permite que o Flask lide com o request do Cloud Functions
    internal_ctx = app.test_request_context(path=request.full_path, method=request.method)
    internal_ctx.request = request
    return app.full_dispatch_request()
