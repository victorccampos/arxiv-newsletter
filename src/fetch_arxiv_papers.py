"""
O script utiliza de um Python wrapper da API do arXiv para 
selecionar `n_papers` candidatos da categoria cond-mat.mtrl-sci
    * cond-mat -> categoria de física da matéria condensada
    * mtrl-sci -> subárea específica.

Aceita outras áreas como: "physics.comp-ph"
"""

from typing import Any
import arxiv
from urllib.request import urlretrieve



def search_candidates(category: str, n_papers: int= 10) -> list[dict[str, Any]]:
    """
    Procura para uma categoria especificada um total de `n_papers` papers.
    São ordenados de acordo com o tempo de submissão do mais antigo ao mais novo

    Args:
        category: str => categoria. Ex: cond-mat.mtrl-sci, physics.comp-ph
    """
    client = arxiv.Client()
    search = arxiv.Search(
        query=f"cat:{category}",
        max_results=n_papers,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    papers = []
    for paper_idx, result in enumerate(client.results(search=search), start=1):
        paper = {
            "published": result.published.strftime("%d/%m/%Y"),
            "paper_idx": paper_idx,
            "title": result.title,
            "abstract": result.summary,
            "pdf_url": result.pdf_url,
            "entry_id": result.entry_id, # https://arxiv.org/abs/{id}
            "short_id": result.get_short_id()
        }
        papers.append(paper)
    
    return papers

def write_papers_query(papers: list[dict[str, Any]], write: bool = False) -> str:
    """
    Cria a string que será utilizada pelo Gemini para filtrar pela relevância à área.
    """
    papers_text = "\n".join(
        f"""
Paper Number: {paper["paper_idx"]} | URL: {paper["pdf_url"]} | Published: {paper["published"]}
Title: {paper["title"]}
ID: {paper["short_id"]}

ABSTRACT:
{paper["abstract"]}
        """

        for paper_idx, paper in enumerate(papers, start=1)
    )
    
    if write:
        with open("arxiv_query.txt", "w") as f:
            f.write(papers_text)

    return papers_text


def download_paper(paper: dict[str, Any]):
    """
    Recebe um dict do formato:
    {
            "published": result.published.strftime("%d/%m/%Y"),
            "paper_idx": paper_idx,
            "title": result.title,
            "abstract": result.summary,
            "pdf_url": result.pdf_url,
            "entry_id": result.entry_id, # https://arxiv.org/abs/{id}
            "short_id": result.get_short_id()
    }
    """
    
    if "/" in paper["title"]:
        paper["title"] = paper["title"].replace("/", "-")
    if ":" in paper["title"]:
        paper["title"] = paper["title"].replace(":","")
    
    paper_number: str = f"{paper["paper_idx"]:03}_"
    pdf_name = paper_number + "_".join(paper["title"].split(" ")) + ".pdf"
        
    print(f"Downloading {pdf_name} ...")
    urlretrieve(paper["pdf_url"], pdf_name)




    