"""Modul für die grafische Benutzeroberfläche (GUI) des Passwort-Managers.

Verwendet ttkbootstrap für eine moderne GUI.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from pm_account_manager import AccountManager
from pm_ki_service import KIService


class PasswortManagerGUI:
    """
    @brief Hauptklasse für die grafische Benutzeroberfläche.
    
    Verwaltet das Hauptfenster und alle GUI-Elemente des Passwort-Managers.
    Verwendet ttkbootstrap für eine moderne Benutzeroberfläche.
    """

    def __init__(self):
        """@brief Initialisiert die GUI und lädt gespeicherte Accounts."""
        self.root = ttk.Window(themename='cosmo')
        self.root.title('Passwort Manager')
        self.root.geometry('900x550')

        self.manager = AccountManager()
        self.manager.load_from_json()

        self.ki_service = KIService()

        self.create_widgets()
        self.load_accounts_into_tree()

    # ---------------- Widgets ----------------

    def create_widgets(self):
        """@brief Erstellt alle GUI-Elemente (Buttons, Tabelle, etc.)."""

        title_label = ttk.Label(
            self.root,
            text='Passwort Manager',
            font=('Segoe UI', 18, 'bold')
        )
        title_label.pack(pady=10)

        # Tabelle
        self.tree = ttk.Treeview(
            self.root,
            columns=('Dienst', 'Benutzername', 'Kategorie', 'Passwort'),
            show='headings',
            height=12
        )

        self.tree.heading('Dienst', text='Dienst')
        self.tree.heading('Benutzername', text='Benutzername')
        self.tree.heading('Kategorie', text='Kategorie')
        self.tree.heading('Passwort', text='Passwort')
        self.tree.column('Dienst', width=220)
        self.tree.column('Benutzername', width=250)
        self.tree.column('Kategorie', width=150)
        self.tree.column('Passwort', width=200)

        self.tree.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Button Frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        # Erste Reihe
        ttk.Button(button_frame, text='Hinzufügen', bootstyle='light',
                   command=self.open_add_account_window).grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(button_frame, text='Anzeigen', bootstyle='light',
                   command=self.show_accounts_window).grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(button_frame, text='Löschen', bootstyle='light',
                   command=self.delete_account_window).grid(row=0, column=2, padx=5, pady=5)

        ttk.Button(button_frame, text='KI Passwort', bootstyle='light',
                   command=self.generate_password_window).grid(row=0, column=3, padx=5, pady=5)

        # Zweite Reihe
        ttk.Button(button_frame, text='KI Bewertung', bootstyle='light',
                   command=self.evaluate_password_window).grid(row=1, column=0, padx=5, pady=5)

        ttk.Button(button_frame, text='Speichern', bootstyle='light',
                   command=self.save_accounts).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(button_frame, text='Laden', bootstyle='light',
                   command=self.load_accounts).grid(row=1, column=2, padx=5, pady=5)

        ttk.Button(button_frame, text='Beenden', bootstyle='danger',
                   command=self.root.destroy).grid(row=1, column=3, padx=5, pady=5)

    # ---------------- Tabelle aktualisieren ----------------

    def load_accounts_into_tree(self):
        """
        @brief Aktualisiert die Treeview-Tabelle mit den aktuellen Accounts.
        
        Löscht alle vorhandenen Einträge und fügt sie neu ein.
        Passwörter werden maskiert angezeigt.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

        for account in self.manager.list_accounts():

            #passowrt maskiert anzeigen
            masked_password = '*' * len(account.password)

            self.tree.insert(
                '',
                'end',
                values=(account.service, account.username, account.category, masked_password)
            )

    # ---------------- Button Funktionen (Platzhalter) ----------------

    def open_add_account_window(self):
        print('Account hinzufügen')

    def show_accounts_window(self):
        print('Accounts anzeigen')

    def delete_account_window(self):
        print('Account löschen')

    def generate_password_window(self):
        print('KI Passwort generieren')

    def evaluate_password_window(self):
        print('KI Passwort bewerten')

    def save_accounts(self):
        """@brief Speichert alle Accounts in die JSON-Datei."""
        self.manager.save_to_json()
        print('Gespeichert')

    def load_accounts(self):
        """@brief Lädt Accounts aus der JSON-Datei und aktualisiert die Anzeige."""
        self.manager.load_from_json()
        self.load_accounts_into_tree()
        print('Geladen')

    # ---------------- Start ----------------

    def run(self):
        """@brief Startet die GUI-Hauptschleife."""
        self.root.mainloop()


if __name__ == '__main__':
    app = PasswortManagerGUI()
    app.run()
