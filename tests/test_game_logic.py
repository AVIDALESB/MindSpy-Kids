from src.game_logic import MindSpyKids
def test_select_random_country():
    game = MindSpyKids()
    countries = [
        {'name': {'common': 'México'}},
        {'name': {'common': 'España'}},
        {'name': {'common': 'Argentina'}}
    ]
    country = game.select_random_country(countries)
    assert country is not None
    assert country['name']['common'] in [c['name']['common'] for c in countries]