"""Modul für die Verwaltung von Accounts."""

from pm_account import Account
import json


class AccountManager:
    """
    @brief Verwaltet eine Liste von Accounts und bietet Speicher-/Ladefunktionen.
    
    Diese Klasse ist verantwortlich für das Hinzufügen, Auflisten und 
    persistente Speichern von Accounts in einer JSON-Datei.
    """

    #Zentraler Speicherort für die Datenbankdatei → einfache Anpassung möglich
    DATA_FILE = 'pm_data.json' 

    def __init__(self):
        """@brief Initialisiert den AccountManager mit leerer Account-Liste."""
        self.accounts = []

    # ---------------- Hinzufügen ----------------

    def add_account(self, account):
        """
        @brief Fügt einen neuen Account zur Liste hinzu.
        
        @param account Der hinzuzufügende Account
        """
        self.accounts.append(account)

   
   
    # ---------------- Auflisten ----------------

    def list_accounts(self):
        """
        @brief Gibt alle gespeicherten Accounts zurück.
        
        @return Liste aller Account-Objekte
        """
        return self.accounts

    
    
    # ---------------- Speichern ----------------

    def save_to_json(self):
        """
        @brief Speichert alle Accounts in die JSON-Datei.
        
        Die Accounts werden als Liste von Dictionaries im JSON-Format gespeichert.
        """
        with open(self.DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(
                [account.to_dict() for account in self.accounts],
                file,
                indent=2,
                ensure_ascii=False
            )

    
    
    # ---------------- Laden ----------------

    def load_from_json(self):
        """
        @brief Lädt Accounts aus der JSON-Datei.
        
        Erstellt eine neue leere Datei, falls diese nicht existiert.
        """
        try:
            with open(self.DATA_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.accounts = [
                    Account.from_dict(item) for item in data
                ]

        except FileNotFoundError:
            # Falls Datei nicht existiert → leere Liste + neue Datei
            self.accounts = []

            with open(self.DATA_FILE, 'w', encoding='utf-8') as file:
                json.dump([], file, indent=2, ensure_ascii=False)

    
    
    # ---------------- Löschen ----------------

    def delete_account(self, index: int):
        if 0 <= index < len(self.accounts):
            del self.accounts[index]
            return True
        return False

