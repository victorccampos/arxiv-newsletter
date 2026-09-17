"""
O script utiliza de um Python wrapper da API do arXiv para
selecionar `n_papers` candidatos da categoria cond-mat.mtrl-sci
    * cond-mat -> categoria de física da matéria condensada
    * mtrl-sci -> subárea específica.

Aceita outras áreas como: "physics.comp-ph"
"""

import arxiv
from typing import Any
from pathlib import Path
from urllib.request import urlretrieve


def search_candidates(category: str, candidate_papers: int = 10) -> list[dict[str, Any]]:
    """
    Procura para uma categoria especificada um total de `candidate_papers` papers.
    São ordenados de acordo com o tempo de submissão do mais antigo ao mais novo

    Args:
        category: Categoria do arXiv a ser pesquisada, como "cond-mat.mtrl-sci".
        candidate_papers: Número máximo de papers candidatos a buscar.

    Returns:
        Lista de dicionários contendo os metadados dos papers encontrados.
    """
    print(f"Looking for {candidate_papers} papers in {category} ...")
    client = arxiv.Client()
    search = arxiv.Search(
        query=f"cat:{category}",
        max_results=candidate_papers,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    papers = []
    for paper_idx, result in enumerate(client.results(search=search), start=1):
        paper = {
            "title": result.title,
            "abstract": result.summary,
            "published": result.published.strftime("%d/%m/%Y"),
            "pdf_url": result.pdf_url,
            "entry_id": result.entry_id,  # https://arxiv.org/abs/{id}
            "short_id": result.get_short_id(),
            "paper_idx": paper_idx,
        }
        papers.append(paper)

    return papers


def write_papers_list(papers: list[dict[str, Any]]) -> str:
    """
    Formata os papers para análise de relevância pelo Gemini.

    Cada paper é convertido em um bloco de texto contendo seu índice, título,
    data de publicação, URL, identificador curto e resumo. Os blocos são
    separados por uma linha em branco e o texto completo é retornado.

    Args:
        papers: Lista de dicionários com os metadados dos papers. Cada item
            deve conter, pelo menos, as chaves ``paper_idx``, ``title``,
            ``published``, ``pdf_url``, ``short_id`` e ``abstract``.

    Returns:
        Texto formatado com os metadados e abstract de todos os papers.
    """
    papers_list = "\n".join(
        f"""[{paper["paper_idx"]}] {paper["title"]}
Published: {paper["published"]}
URL: {paper["pdf_url"]}
ID: {paper["short_id"]}

ABSTRACT:
{paper["abstract"]}
        """
        for paper_idx, paper in enumerate(papers, start=1)
    )

    
    Path("../candidate_papers.txt").write_text(papers_list)

    return papers_list


def format_pdf_name(paper: dict[str, Any]) -> str:
    """Gera um nome de arquivo PDF a partir dos metadados de um paper.

    O nome contém o índice do paper, seguido do título normalizado, com
    caracteres que podem interferir no caminho do arquivo substituídos ou
    removidos.

    Args:
        paper: Dicionário contendo ``paper_idx`` e ``title``.

    Returns:
        Nome do arquivo PDF formatado, com a extensão ``.pdf``.
    """

    if "/" in paper["title"]:
        paper["title"] = paper["title"].replace("/", "-")
    if ":" in paper["title"]:
        paper["title"] = paper["title"].replace(":", "")
    paper_number = f"{paper['paper_idx']:03}_"
    title_parts = paper["title"].split(" ")
    filename    = paper_number + "_".join(title_parts) + ".pdf"
    return filename

    

def download_paper(paper: dict[str, Any]):
    pdf_name = format_pdf_name(paper)
    print(f"Downloading {pdf_name} ...")
    urlretrieve(paper["pdf_url"], pdf_name)
