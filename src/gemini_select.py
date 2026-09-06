"""
Script responsável por receber uma query com papers candidatos onde há a 
informação de:
 - Data de Publicação
 - Título
 - PDF_URL:
    Exemplo: https://arxiv.org/pdf/{ID}
 - ID
    Exemplo: 2609.04169v1
"""

import os
from google import genai
from dotenv import load_dotenv


load_dotenv()
API_GEMINI_KEY = os.getenv("GEMINI_API_KEY")

SELECT_PROMPT = """
You are an academic research curator.

Your task is to select exactly 3 papers
from the candidate papers below based on its titles and abstracts.

Target research profile:

- computational condensed matter physics
- computational materials science
- atomistic simulations
- density functional theory
- molecular dynamics
- machine learning potentials / force fields
- materials modeling
- phonons
- electronic structure

Selection criteria, in order:

1. Scientific relevance to the target research profile.
2. Methodological relevance.
3. Potential usefulness to a researcher in this area.
4. Recency.
5. Diversity between the selected papers.

Do not select papers merely because their titles sound interesting.

For every selected paper:

- preserve the exact title;
- preserve the exact arXiv URL;
- write a concise scientific summary of 80-120 words;
- explain why the paper is relevant;
- identify the main methods;
- identify the main contribution.

Do not invent information that is not supported by the title
or abstract.

Your response must be in a appropiate text format so that will be used in
a newsletter. If possible HTML with good aesthetics. Do not insert LLM-like
text like 'Based on your ..., I have selected ...' the content of the e-mail
must be as much as possible close to human writing, but formatted in a cool HTML
way.

The h1 header of the e-mail must contain the title 'JVC arXiv Newsletter'
each article information will be in a <div class="paper">.
The h2 headers will contain the articles titles with href's directing to the pdf
in color blue.
Below the h2 header must have the information about the publication data with a 
smaller gray font. Can be a <div class="metadata">. 
Below the metadaa must have a summary, a <div class="summary">

After the summary, will be a <div> for details containing <p> tags with bold
font containing
    Relevance
    Main methods
    Contribution to the area.
Candidate papers:

{arxiv_result_query}
"""

def select_papers(papers_query: str) -> str:
    """
    Seleciona apenas 3 papers da consulta do Arxiv com base nos critérios 
    definidos `SELECT_PROMPT`.
    """
    client = genai.Client(api_key=API_GEMINI_KEY)
    
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=SELECT_PROMPT.format(arxiv_result_query=papers_query)
    )

    print(interaction.output_text)
    return interaction.output_text


if __name__ == "__main__":
    with open("../query_result.txt", "r") as f:
        query = f.read()



    resultado = select_papers(papers_query=query)
    print(resultado)
    
    
    


