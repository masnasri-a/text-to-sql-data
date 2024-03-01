from requests import get, post
from dotenv import load_dotenv
import os

load_dotenv()


class Gemini:
    def __init__(self):
        self.token = os.getenv("GEMINI_TOKEN")
        self.uri = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key="

    """
    Fetch data from gemini API
    """
    def fetch(self, message: str):
        body = {"contents": [{"parts": [{"text": message}]}]}
        response = post(self.uri + self.token, json=body)
        return response.json()

    """
    Parse response from gemini API
    """
    def parse_response(self, response):
        data: str = response['candidates'][0]['content']['parts'][0]['text']
        return (data.replace("<SQL>", "").replace("</SQL>", "")
                .replace("```", "").replace("sql", "")).replace('"', "'")
