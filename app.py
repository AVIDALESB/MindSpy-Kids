import streamlit as st
import requests
from src.api_handler import CountryAPI
from src.game_logic import MindSpyKids

# Configuración inicial de la página (debe ser lo primero)
st.set_page_config(
    page_title="MindSpy Kids",
    page_icon="🌍",
    layout="wide"
)

class MindSpyApp:
    def __init__(self):
        self.api = CountryAPI()
        self.init_session_state()

    def init_session_state(self):
        """Inicialización de variables de estado"""
        if 'game' not in st.session_state:
            st.session_state.game = MindSpyKids()
        if 'countries' not in st.session_state:
            self.load_countries()
        if 'attempts' not in st.session_state:
            st.session_state.attempts = 0
        if 'correct_guesses' not in st.session_state:
            st.session_state.correct_guesses = 0

    def load_countries(self):
        """Carga de datos de países con manejo de errores"""
        with st.spinner('Cargando datos de países... 🌍'):
            try:
                response = requests.get('https://restcountries.com/v3.1/all', timeout=5)
                response.raise_for_status()
                st.session_state.countries = response.json()
            except requests.exceptions.RequestException as e:
                st.error("❌ No se pudieron cargar los países. ¡Inténtalo de nuevo!")
                st.session_state.countries = []

    def render_header(self):
        """Renderizado del encabezado con estilos mejorados"""
        st.markdown("""
            <style>
                .main-title {
                    color: #2E86C1;
                    text-align: center;
                    padding: 20px;
                    border-radius: 10px;
                    background-color: #F8F9F9;
                    margin-bottom: 20px;
                }
                .score-box {
                    padding: 10px;
                    border-radius: 5px;
                    background-color: #E8F6F3;
                    text-align: center;
                }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<h1 class="main-title">🌍 MindSpy Kids - Explorador de Países</h1>', 
                   unsafe_allow_html=True)

    def handle_game_logic(self):
        """Lógica principal del juego con interacciones mejoradas"""
        col1, col2 = st.columns([2, 1])

        with col2:
            st.markdown("### 🎮 Panel de Control")
            if st.button("¡Nuevo País! 🎲", key="new_game"):
                self.start_new_game()

            st.markdown("### 📊 Tu Progreso")
            st.markdown('<div class="score-box">', unsafe_allow_html=True)
            st.metric("Puntaje", st.session_state.game.score)
            st.metric("Intentos", st.session_state.attempts)
            st.metric("Países Adivinados", st.session_state.correct_guesses)
            st.markdown('</div>', unsafe_allow_html=True)

        with col1:
            if st.session_state.get('current_country'):
                self.show_game_interface()

    def start_new_game(self):
        """Iniciar nuevo juego"""
        country = st.session_state.game.select_random_country(st.session_state.countries)
        if country:
            st.session_state.current_country = country
            st.success("🎲 ¡Nuevo país seleccionado! ¿Podrás adivinarlo?")
            st.session_state.attempts = 0
        else:
            st.error("No hay más países disponibles. ¡Reinicia el juego!")

    def show_game_interface(self):
        """Mostrar interfaz principal del juego"""
        country = st.session_state.current_country
        hints = st.session_state.game.generate_hint(country)

        st.markdown("### 🔍 Pistas")
        for i, hint in enumerate(hints, 1):
            st.info(f"Pista #{i}: {hint}")

        col1, col2 = st.columns([3, 1])
        with col1:
            guess = st.text_input("¿Qué país crees que es?", 
                                key="country_guess",
                                placeholder="Escribe el nombre del país...").strip()
        with col2:
            if st.button("Comprobar 🎯") and guess:
                self.check_answer(guess, country)

    def check_answer(self, guess, country):
        """Verificar respuesta del usuario"""
        st.session_state.attempts += 1
        
        if st.session_state.game.check_guess(guess.lower(), country):
            self.handle_correct_guess(country)
        else:
            self.handle_incorrect_guess()

    def handle_correct_guess(self, country):
        """Manejar respuesta correcta"""
        st.balloons()
        st.success("🎉 ¡Felicitaciones! ¡Lo adivinaste!")
        st.session_state.game.update_score(10)
        st.session_state.correct_guesses += 1
        
        if 'flags' in country and 'png' in country['flags']:
            st.image(country['flags']['png'], width=200)
        
        with st.expander("📚 Más información sobre el país"):
            if 'capital' in country:
                st.write(f"🏛️ Capital: {country['capital'][0]}")
            if 'population' in country:
                st.write(f"👥 Población: {country['population']:,}")
            if 'region' in country:
                st.write(f"🌎 Región: {country['region']}")

    def handle_incorrect_guess(self):
        """Manejar respuesta incorrecta"""
        st.error("❌ ¡Incorrecto! ¡Sigue intentando!")
        st.session_state.game.update_score(-1)
        
        if st.session_state.attempts >= 3:
            st.warning("💡 Consejo: Lee cuidadosamente todas las pistas.")

    def run(self):
        """Ejecutar la aplicación"""
        self.render_header()
        self.handle_game_logic()

if __name__ == "__main__":
    app = MindSpyApp()
    app.run()