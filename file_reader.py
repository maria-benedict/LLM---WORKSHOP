import pypdf
import docx
import pandas as pd
from PIL import Image


def read_file(file):

    text = ""

    try:

        filename = file.name.lower()

        # ---------- PDF ----------
        if filename.endswith(".pdf"):

            pdf = pypdf.PdfReader(file)

            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"


        # ---------- TXT ----------
        elif filename.endswith(".txt"):

            text = file.read().decode("utf-8", errors="ignore")


        # ---------- DOCX ----------
        elif filename.endswith(".docx"):

            doc = docx.Document(file)

            for para in doc.paragraphs:
                text += para.text + "\n"


        # ---------- IMAGE (NO OCR) ----------
        elif filename.endswith((".png", ".jpg", ".jpeg")):

            text = "Image uploaded. OCR is disabled, so text cannot be extracted."


        # ---------- CSV ----------
        elif filename.endswith(".csv"):

            df = pd.read_csv(file)
            text = df.to_string(index=False)


        # ---------- EXCEL ----------
        elif filename.endswith((".xls", ".xlsx")):

            df = pd.read_excel(file)
            text = df.to_string(index=False)


        # ---------- Unsupported ----------
        else:

            text = "Unsupported file type."


    except Exception as e:

        print("❌ File reading error:", e)
        text = ""

    return text