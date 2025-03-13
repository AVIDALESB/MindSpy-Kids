import random
from typing import List, Dict, Optional

class MindSpyKids:
    def __init__(self):
        self.score = 0
        self.current_country = None
        self.countries_played = set()

    def select_random_country(self, countries: List[Dict]) -> Optional[Dict]:
        """
        Selecciona un país aleatorio que no haya sido jugado anteriormente.
        
        Args:
            countries: Lista de diccionarios con información de países
            
        Returns:
            Dict: Diccionario con información del país seleccionado
        """
        available_countries = [c for c in countries if c['name']['common'] not in self.countries_played]
        if available_countries:
            self.current_country = random.choice(available_countries)
            self.countries_played.add(self.current_country['name']['common'])
            return self.current_country
        return None

    def generate_hint(self, country: Dict) -> List[str]:
        """
        Genera pistas sobre el país seleccionado.
        
        Args:
            country: Diccionario con información del país
            
        Returns:
            List[str]: Lista de pistas sobre el país
        """
        hints = []
        if country:
            if 'region' in country:
                hints.append(f"Este país está en {country['region']}")
            if 'capital' in country:
                hints.append(f"Su capital es {country['capital'][0]}")
            if 'population' in country:
                hints.append(f"Tiene una población de aproximadamente {country['population']} habitantes")
            if 'languages' in country:
                languages = list(country['languages'].values())
                hints.append(f"Se habla: {', '.join(languages)}")
        return hints

    def check_guess(self, guess: str, country: Dict) -> bool:
        """
        Verifica si la respuesta del usuario es correcta.
        
        Args:
            guess: Respuesta del usuario
            country: Diccionario con información del país
            
        Returns:
            bool: True si la respuesta es correcta, False en caso contrario
        """
        if country and 'name' in country:
            return guess.lower() == country['name']['common'].lower()
        return False

    def update_score(self, points: int) -> None:
        """
        Actualiza el puntaje del jugador.
        
        Args:
            points: Puntos a sumar o restar
        """
        self.score += points

    def reset_game(self) -> None:
        """
        Reinicia el juego a su estado inicial.
        """
        self.score = 0
        self.current_country = None
        self.countries_played.clear()