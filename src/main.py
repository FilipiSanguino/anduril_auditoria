import os
from flask import Flask, request, jsonify
from core.sql_generator import generate_sql
from core.vector_db import search_documents, add_document

app = Flask(__name__)

@app.route('/')
def hello():
    return "API do Sistema de Auditoria est\xc3\xa1 no ar!"

@app.route('/generate-sql', methods=['POST'])
def handle_generate_sql():
    data = request.json
    schema_info = "Tabela: transacoes (id INT, valor DECIMAL, cliente_id INT, status STRING)"
    sql = generate_sql(data['query'], schema_info)
    return jsonify({"sql_query": sql})

@app.route('/search-docs', methods=['POST'])
def handle_search_docs():
    data = request.json
    results = search_documents(data['query'], required_role=data.get('role', 'public'))
    return jsonify(results)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

