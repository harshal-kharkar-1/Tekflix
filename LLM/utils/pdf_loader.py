# LLM/utils/pdf_loader.py

def chunk_text(text, chunk_size=500):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]





import fitz



def extract_text_from_pdf(file_path):

    doc = fitz.open(file_path)

    return "\n".join([page.get_text() for page in doc])





def chunk_text(text, chunk_size=1000):

    """Splits long text into smaller chunks"""

    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]






