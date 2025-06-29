from unittest.mock import patch, MagicMock
import importlib
import sys
import faiss
import numpy as np


def test_search_documents_when_empty_returns_message():
    mock_model = MagicMock()
    mock_model.encode.return_value = np.zeros((1, 1), dtype='float32')
    with patch('sentence_transformers.SentenceTransformer', return_value=mock_model):
        if 'core.vector_db' in sys.modules:
            del sys.modules['core.vector_db']
        vector_db = importlib.import_module('core.vector_db')
        index = faiss.IndexFlatL2(1)
        with patch.object(vector_db, 'get_vector_db_from_gcs', return_value=(index, [])):
            results = vector_db.search_documents('consulta')
    assert results[0]['text'].startswith('O banco de dados vetorial')

