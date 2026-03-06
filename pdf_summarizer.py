import requests
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("❌ API key not found. Check your .env file.")


def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        return text
    except Exception as e:
        print("❌ Error reading PDF:", e)
        return None


def summarize_notes(text):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Notes Summarizer"
    }

    prompt = f"""
    Summarize the following notes into:
    1. Clear bullet points
    2. 5 key concepts
    
    Notes:
    {text}
    """

    data = {
        "model": "qwen/qwen-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if "error" in result:
            print("❌ API Error:", result["error"]["message"])
            return None

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ Request failed:", e)
        return None


if __name__ == "__main__":
    pdf_path = input("Enter path to your PDF file: ")

    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("❌ Could not extract text from PDF.")
    else:
        summary = summarize_notes(text)

        if summary:
            print("\n===== AI SUMMARY =====\n")
            print(summary)
        else:
            print("❌ Failed to generate summary.")