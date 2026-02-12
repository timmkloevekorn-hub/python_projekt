"""Haupteinstiegspunkt für den Passwort-Manager.

Startet die textbasierte Konsolen-Benutzeroberfläche.
"""

from pm_account import Account
from pm_account_manager import AccountManager
from pm_console_ui import run_console_ui    


if __name__ == '__main__':
    run_console_ui()



