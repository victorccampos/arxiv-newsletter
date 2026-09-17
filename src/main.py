from fetch_arxiv_papers import search_candidates, write_papers_list
from gemini_select import select_papers, load_prompt
from send_newsletter_email import send_email, format_html

def main():
    # Buscar papers candidatos do Arxiv
    papers = search_candidates(category="physics.comp-ph", candidate_papers=20)
    
    # Monta o prompt completo com a lista de candidatos
    prompt = load_prompt("../prompts/prompt.txt") + write_papers_list(papers)
    
    # Selecionar os papers com Gemini
    html_newsletter = format_html(select_papers(prompt))
    
    # Enviar e-mail
    send_email(subject="Newsletter do JVC", html_content=html_newsletter)


if __name__ == "__main__":
    main()
