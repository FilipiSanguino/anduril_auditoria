from unittest.mock import patch
from core.sql_generator import generate_sql


def test_generate_sql_returns_cleaned_sql():
    mock_response = """```sql
SELECT * FROM tabela;
```"""
    with patch('core.sql_generator.call_llm', return_value=mock_response):
        result = generate_sql("obter dados", "Tabela: tabela (id INT)")
    assert result == "SELECT * FROM tabela;"


