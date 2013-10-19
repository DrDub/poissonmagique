from webapp.poissonmagique.models import Campaign, Human, Character

def find_character(human):
    characters = Character.objects.filter(controller=human, is_active=True)
    if len(characters) == 0:
        return None
    else:
        return characters[0]
