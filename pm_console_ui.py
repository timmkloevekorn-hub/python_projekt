"""Modul für die textbasierte Konsolen-Benutzeroberfläche.

Bietet alle Funktionen zur Interaktion mit dem Benutzer über die Konsole.
"""

from importlib.resources import path
from pm_account_manager import AccountManager
from pm_account import Account
from pm_ki_service import KIService


#Standarddatzei für die JSON-Datei
DATA_FILE = 'pm_data.json'


def show_menu():
    """
    @brief Zeigt das Hauptmenü an und gibt die Benutzerauswahl zurück.
    
    @return Die gewählte Menüoption (0-7)
    """
    print('\n--- Passwort-Manager ---')
    print('1. Account hinzufügen')
    print('2. Accounts anzeigen')
    print('3. Account löschen')
    print('4. Passwort generieren - KI')
    print('5. Passwort bewerten - KI')
    print('6. Accounts speichern')
    print('7. Accounts laden')
    print('0. Beenden')

    while True:
        try:
            choice = int(input('Deine Wahl: '))
            if 0 <= choice <= 7:
                return choice
            else:
                print('Bitte eine Zahl zwischen 0 und 7 eingeben.')
        except ValueError:
            print('Ungültige Eingabe. Bitte eine Zahl eingeben.')

#Funktion zum Erstellen eines Accounts
def create_account(manager: AccountManager, ki_service: KIService):
    """
    @brief Erstellt einen neuen Account mit Benutzereingaben.
    
    @param manager Der AccountManager zum Hinzufügen
    @param ki_service KI-Service für optionale Passwortgenerierung
    """
    print('\n--- Account hinzufügen ---')

    service = input('Dienst: ').strip()
    username = input('Benutzername: ').strip()
    category = input('Kategorie: ').strip()

    print('\nPasswort wählen:')
    print('1 - Manuell eingeben')
    print('2 - Von KI generieren')

    choice = input('Deine Wahl: ').strip()

    if choice == '1':
        password = input('Passwort: ').strip()

    elif choice == '2':
        try:
            length = int(input('Gewünschte Passwortlänge: '))
            password = ki_service.generate_password(length)
            print(f'Generiertes Passwort: {password}')
        except Exception as e:
            print('Fehler bei der KI-Verbindung:')
            print(e)
            return

    else:
        print('Ungültige Auswahl.')
        return

    account = Account(service, username, password, category)
    manager.add_account(account)

    print(f'Account für {service} wurde erfolgreich hinzugefügt.')


#Funktion zum Anzeigen aller Accounts
def list_accounts(manager: AccountManager):
    """
    @brief Zeigt alle gespeicherten Accounts an.
    
    Passwörter werden maskiert angezeigt. Benutzer kann ein Passwort wählen,
    um es unmaskiert zu sehen.
    
    @param manager Der AccountManager mit den Accounts
    """
    print('\n--- Gespeicherte Accounts anzeigen ---')

    accounts = manager.list_accounts()

    #Falls keine Accounts vorhanden sind, entsprechende Meldung ausgeben
    if not accounts:
        print('Keine Accounts vorhanden.')
        return
    
    # Accounts auflisten
    for index, account in enumerate(accounts, start=1):
        masked_password = '*' * len(account.password)
        print(f'{index}. Dienst: {account.service}, Benutzername: {account.username}, Kategorie: {account.category}, Passwort: {masked_password}')

    # Erst nach der kompletten Liste fragen
    show_password = input(
        '\nPasswort für eine Nummer anzeigen? '
        '(Nummer eingeben oder Enter zum Überspringen): '
    ).strip()

    if not show_password:
        return

    try:
        index = int(show_password) - 1

        if 0 <= index < len(accounts):
            account = accounts[index]
            print(f'\n{index+1}. Dienst: {account.service}, Benutzername: {account.username}, Kategorie: {account.category}, Passwort: {account.password}')
        else:
            print('Ungültige Nummer.')

    except ValueError:
        print('Bitte eine gültige Zahl eingeben.')



#Funktion zum speichern der Accounts
def save_accounts(manager: AccountManager):
    manager.save_to_json()
    print('Accounts wurden gespeichert.')


#Funktion zum Laden der Accounts
def load_accounts(manager: AccountManager):
    manager.load_from_json()
    print('Accounts wurden geladen.')


#Funktion zum Löschen eines Accounts
def delete_account(manager: AccountManager):
    list_accounts(manager)
    if not manager.accounts:
        return
    
    while True:
        try:
            index = int(input('Gib die Nummer des zu löschenden Accounts ein (0 zum Abbrechen): '))
            if index == 0:
                print('Löschen abgebrochen.')
                return
            elif 1 <= index <= len(manager.accounts):
                manager.delete_account(index - 1)
                print('Account wurde gelöscht.')
                return
            else:
                print(f'Bitte eine Zahl zwischen 1 und {len(manager.accounts)} eingeben.')
        except ValueError:
            print('Ungültige Eingabe. Bitte eine Zahl eingeben.')


#Funktion zum Generieren eines Passworts per KI
def generate_password_ki(ki_service: KIService):
    while True:
        try:
            length = int(input('Gib die gewünschte Länge des Passworts ein (z.B. 16): '))
            if length > 0:
                break
            else:
                print('Bitte eine positive Zahl eingeben.')
        except ValueError:
            print('Ungültige Eingabe. Bitte eine Zahl eingeben.')

    passwort = ki_service.generate_password(length)
    print(f'Generiertes Passwort: {passwort}')


#Funktion zum Bewerten eines Passowrts durch die KI
def evaluate_password_ki(ki_service: KIService):
    passwort = input('Gib das zu bewertende Passwort ein: ').strip()

    if not passwort:
        print('Kein Passwort eingegeben.')
        return

    try:
        bewertung = ki_service.evaluate_password(passwort)
        print(f'Passwortbewertung: {bewertung}')
    except Exception as e:
        print('Fehler bei der KI-Verbindung:')
        print(e)




#Hauptfunktion, die das Menü anzeigt und die Auswahl des Benutzers verarbeitet
def run_console_ui():
    manager = AccountManager()

    #Automatisches Laden der Accounts bei Programmstart
    manager.load_from_json()
    print('Accounts wurden automatisch geladen.')

    #KI-Service initialisieren
    ki_service = KIService()

    while True:
        choice = show_menu()
        
        match choice:
            case 1:
                create_account(manager, ki_service)
            
            case 2:
                list_accounts(manager)
            
            case 3:
                delete_account(manager)
                
            
            case 4:
                generate_password_ki(ki_service)
            
            case 5:
                evaluate_password_ki(ki_service)
            
            case 6:
                save_accounts(manager)
            
            case 7:
                load_accounts(manager)
            
            case 0:
                print('Programm beendet.')
                break