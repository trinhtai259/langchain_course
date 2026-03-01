from langchain_community.document_loaders import PyPDFLoader
import re
import os

def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    content = ''
    for page in pages:
        content += page.page_content + "\n"
    return content
def clean_text(text):
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    return text
def split_chapters(text):
    pattern = r'(Chương\s+[IVXLCDM0-9]+.*?)((?=Chương\s+[IVXLCDM0-9]+)|$)'
    return re.findall(pattern, text, flags=re.DOTALL)


def split_articles(chapter_text):
    pattern = r'(Điều\s+\d+\.\s.*?)(?=(Điều\s+\d+\.|\Z))'
    return re.findall(pattern, chapter_text, flags=re.DOTALL)


def split_clauses(article_text):
    pattern = r'(\d+\.\s.*?)(?=(\d+\.|\Z))'
    return re.findall(pattern, article_text, flags=re.DOTALL)


def split_points(clause_text):
    pattern = r'([a-zđ]\)\s.*?)(?=([a-zđ]\)|\Z))'
    return re.findall(pattern, clause_text, flags=re.DOTALL)

def parse_law(text,LAW_NAME):
    structured_data = []

    chapters = split_chapters(text)
    

    for chapter_full, _ in chapters:
        chapter_match = re.search(r'Chương\s+([IVXLCDM0-9]+)', chapter_full)
        chapter_number = chapter_match.group(1) if chapter_match else None

        articles = split_articles(chapter_full)

        for article_full, _ in articles:
            article_header_match = re.match(r'^Điều\s+(\d+)\.\s*(.+?)(?:\n|$)',article_full)
            if not article_header_match:
                continue

            article_number = int(article_header_match.group(1))
            article_title = article_header_match.group(2)

            clauses = split_clauses(article_full)

            if not clauses:
                structured_data.append({
                    "law_name": LAW_NAME,
                    "chapter": chapter_number,
                    "article": article_number,
                    "article_title": article_title,
                    "content": article_full.strip()
                })
                continue

            for clause_full, _ in clauses:
                clause_match = re.match(r'(\d+)\.', clause_full)
                clause_number = int(clause_match.group(1)) if clause_match else None

                points = split_points(clause_full)

                if not points:
                    structured_data.append({
                        "law_name": LAW_NAME,
                        "chapter": chapter_number,
                        "article": article_number,
                        "article_title": article_title,
                        "clause": clause_number,
                        "content": clause_full.strip()
                    })
                    continue

                for point_full, _ in points:
                    point_match = re.match(r'([a-zđ])\)', point_full)
                    point_letter = point_match.group(1) if point_match else None

                    structured_data.append({
                        "law_name": LAW_NAME,
                        "chapter": chapter_number,
                        "article": article_number,
                        "article_title": article_title,
                        "clause": clause_number,
                        "point": point_letter,
                        "content": point_full.strip()
                    })

    return structured_data

