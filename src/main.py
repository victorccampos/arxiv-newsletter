from typing import Any
from fetch_arxiv_papers import search_candidates, write_papers_query
from gemini_select import select_papers
from send_newsletter_email import send_email, clean_markdown_response

def main():
    # Buscar papers do Arxiv
    print("Looking for papers in ArXiv...")
    papers: list[dict[str, Any]] = search_candidates(category="cond-mat.mtrl-sci", n_papers=10)
    
    # Escrever a query do Arxiv 
    print("Writing paper query to insert in Gemini prompt.")
    papers_query: str = write_papers_query(papers, write=True)

    # Selecionar os 3 melhores papers com base no prompt
    print("Selecting 3 best papers to create newsletter content.")
    markdown_text: str = select_papers(papers_query=papers_query)

    html_content = clean_markdown_response(markdown_text)
    
    with open("newsletter_content.html", "w") as f:
        f.write(html_content)


    # Enviar e-mail
    send_email(subject="Newsletter do JVC", html_content=html_content)


if __name__ == "__main__":
    main()