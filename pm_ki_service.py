"""Modul für KI-gestützte Passwortfunktionen."""

import os
from google import genai


class KIService:
    """
    @brief Service-Klasse für KI-Integration mit Google Gemini.
    
    Bietet Funktionen zur KI-gestützten Passwortgenerierung und -bewertung
    unter Verwendung der Google Gemini API.
    """

    def __init__(self):
        """
        @brief Initialisiert den KI-Service mit API-Key.
        
        @throws ValueError Falls GOOGLE_API_KEY Umgebungsvariable nicht gesetzt ist
        """
        api_key = os.getenv('GOOGLE_API_KEY')

        if not api_key:
            raise ValueError('GOOGLE_API_KEY ist nicht gesetzt.')

        self.client = genai.Client(api_key=api_key)




    # ---------------- Passwort generieren ----------------

    def generate_password(self, length: int = 16) -> str:
        """
        @brief Generiert ein sicheres Passwort mit KI.
        
        @param length Gewünschte Passwortlänge (Standard: 16)
        @return Generiertes Passwort mit Groß-/Kleinbuchstaben, Zahlen und Sonderzeichen
        """
        prompt = (
            f'Erstelle ein sicheres Passwort mit genau {length} Zeichen. '
            'Nutze Großbuchstaben, Kleinbuchstaben, Zahlen und Sonderzeichen. '
            'Gib ausschließlich das Passwort zurück, ohne Erklärung.'
        )

        response = self.client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt
        )

        return response.text.strip()




    # ---------------- Passwort bewerten ----------------

    def evaluate_password(self, password: str) -> str:
        """
        @brief Bewertet die Stärke eines Passworts mit KI.
        
        @param password Das zu bewertende Passwort
        @return Bewertung (schwach/mittel/stark) mit Begründung und Fazit
        """
        prompt = (
            f'Bewerte die Stärke des folgenden Passworts: "{password}".\n\n'
            'Die Antwort muss exakt folgendes Format haben:\n\n'
            '1. Erste Zeile: Nur ein einzelnes Wort zur Bewertung '
            '(schwach, mittel oder stark).\n'
            '2. Zweite Zeile: Eine kurze Begründung in maximal zwei Sätzen.\n'
            '3. Dritte Zeile: Beginne mit "Fazit:" gefolgt von:\n'
            '"Das Passwort kann so bleiben." '
            'oder '
            '"Lege dir besser ein neues Passwort mit dem Passwortgenerator an."\n\n'
            'Gib ausschließlich diese drei Abschnitte zurück und nichts anderes.'
        )

        response = self.client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt
        )

        return response.text.strip()
