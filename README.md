# Projeto de Auditoria Multi-Agente - Anduril

Este reposit\xc3\xb3rio cont\xc3\xa9m uma prova de conceito para um sistema de auditoria interna baseado em agentes de IA.
Ele demonstra como gerar consultas SQL via linguagem natural e como pesquisar normativos usando um banco vetorial.

## Requisitos
- Python 3.11+
- Depend\xc3\xaancias listadas em `src/requirements.txt`

## Instala\xc3\xa7\xc3\xa3o
```bash
pip install -r src/requirements.txt
```

Opcionalmente defina as seguintes vari\xc3\xa1veis de ambiente:
- `GEMINI_API_KEY` para usar o modelo real do Gemini
- `GCS_BUCKET_NAME` para apontar o bucket do Google Cloud onde o \xc3\xadndice FAISS ser\xc3\xa1 salvo

## Executando os testes
```bash
pytest
```

## Executando a aplica\xc3\xa7\xc3\xa3o
```bash
python src/main.py
```
Ou via Docker:
```bash
docker build -t anduril .
docker run -p 8080:8080 anduril
```

Este projeto \xc3\xa9 experimental e serve apenas como demonstra\xc3\xa7\xc3\xa3o de integra\xc3\xa7\xc3\xa3o de IA em processos de auditoria.


