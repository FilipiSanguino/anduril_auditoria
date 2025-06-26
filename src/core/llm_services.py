import os
import google.generativeai as genai

# Configure com sua API Key do Gemini (armazenada como um Secret no GCP)
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Mock para PoC sem chave configurada
class MockModel:
    def generate_content(self, prompt):
        return type('obj', (object,), {'text': f"Resposta simulada para: {prompt[:50]}..."})()

def get_model(model_name="gemini-1.5-flash"):
    """Retorna um modelo generativo real ou um mock."""
    try:
        # Descomente quando a API Key estiver configurada
        # return genai.GenerativeModel(model_name)
        return MockModel() # Comente para usar o modelo real
    except Exception:
        print("API Key do Gemini não configurada. Usando mock.")
        return MockModel()

def call_llm(prompt: str, model_name: str = "gemini-1.5-flash", temperature: float = 0.7) -> str:
    """Função genérica para chamar um LLM."""
    print(f"Chamando modelo {model_name} com temperatura {temperature}...")
    model = get_model(model_name)
    # A API real pode ter parâmetros de configuração diferentes para temperatura
    response = model.generate_content(prompt)
    return response.text

def auto_consistency(prompt: str, models: list, temperatures: list) -> str:
    """Executa o prompt em várias configurações e usa um modelo de raciocínio para consolidar."""
    responses = []
    for model_name in models:
        for temp in temperatures:
            response_text = call_llm(prompt, model_name, temp)
            responses.append({
                "model": model_name,
                "temperature": temp,
                "response": response_text
            })

    print(f"Total de respostas geradas: {len(responses)}")
    
    # O "reasoning_model" consolida as respostas
    consolidation_prompt = f"""
    As seguintes respostas foram geradas para o mesmo prompt. Analise-as, identifique a resposta mais consistente, correta e completa e a retorne como resultado final.
    Prompt Original: "{prompt}"
    Respostas:
    {responses}
    """
    
    reasoning_model = get_model("gemini-1.5-pro") # Um modelo mais robusto para raciocínio
    final_answer = call_llm(consolidation_prompt, reasoning_model.model_name, 0.5)
    
    return final_answer
