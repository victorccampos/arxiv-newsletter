from dotenv import load_dotenv
from google import genai
from pathlib import Path
import os


load_dotenv()
API_GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def load_prompt(prompt: Path) -> str:
    """Carrega o prompt definido em arquivo de texto pelo usuário."""
    prompt = Path(prompt) # garante que seja do tipo Path
    prompt_string = prompt.read_text()
    return prompt_string
    
        
def select_papers(prompt: str) -> str:
    """
    Usa a API GenAI do Google Gemini para selecionar papers.

    O conteúdo de ``prompt`` é enviado ao modelo ``gemini-3.5-flash-lite``
    por meio do SDK ``google.genai``. O prompt deve incluir a lista de papers
    candidatos e os critérios que o Gemini deve usar na seleção. A API é
    autenticada com a chave definida na variável de ambiente
    ``GEMINI_API_KEY`` (carregada pelo módulo ``dotenv``).

    Args:
        prompt: Instruções, critérios e lista de papers candidatos enviados
            ao modelo GenAI.

    Returns:
        Texto gerado pelo Gemini contendo a seleção de papers.
    """
    client = genai.Client(api_key=API_GEMINI_KEY)
    # TODO: remover 'prompt-dependence' da formatação do HTML
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt
    )
    return interaction.output_text


    
    
    


