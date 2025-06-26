import sqlparse
from .llm_services import call_llm

def generate_sql(natural_language_query: str, schema_info: str) -> str:
    """Gera uma query SQL a partir de linguagem natural e a valida."""
    prompt = f"""
    Com base no schema de banco de dados abaixo, gere uma query SQL que responda à seguinte pergunta em linguagem natural.
    Retorne APENAS o código SQL, sem nenhuma explicação adicional.

    Schema:
    ---
    {schema_info}
    ---

    Pergunta: "{natural_language_query}"
    """
    
    generated_sql = call_llm(prompt, model_name="gemini-1.5-flash", temperature=0.2)
    
    # Limpeza e validação básica de sintaxe
    cleaned_sql = generated_sql.strip().replace("`", "").replace("sql", "", 1).strip()
    
    try:
        # Valida se a sintaxe é parseável
        sqlparse.parse(cleaned_sql)
        print("SQL gerado é sintaticamente válido.")
        return cleaned_sql
    except Exception as e:
        print(f"Erro de sintaxe no SQL gerado: {e}")
        return f"-- ERRO: SQL Inválido Gerado\n-- {cleaned_sql}"