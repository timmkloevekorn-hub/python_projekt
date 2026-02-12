"""Modul für die Account-Klasse."""

class Account:
    """
    @brief Repräsentiert einen gespeicherten Account mit Login-Daten.
    
    Diese Klasse enthält alle relevanten Informationen für einen Account
    und bietet Methoden zur Serialisierung und Deserialisierung.
    """
    
    def __init__(self, service, username, password, category):
        """
        @brief Initialisiert einen neuen Account.
        
        @param service Name des Dienstes (z.B. Gmail, Netflix)
        @param username Benutzername für den Account
        @param password Passwort für den Account
        @param category Kategorie zur Gruppierung (z.B. Email, Streaming)
        """
        self.service = service
        self.username = username
        self.password = password
        self.category = category

    def to_dict(self):
        """
        @brief Konvertiert den Account in ein Dictionary für JSON-Speicherung.
        
        @return Dictionary mit Account-Daten (Service, Username, Password, Category)
        """
        return {
            'Service': self.service,
            'Username': self.username,
            'Password': self.password,
            'Category': self.category
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        @brief Erstellt einen Account aus einem Dictionary.
        
        @param data Dictionary mit Account-Daten
        @return Neuer Account mit den geladenen Daten
        """
        return cls(
            service=data['Service'],
            username=data['Username'],
            password=data['Password'],
            category=data['Category']
        )
