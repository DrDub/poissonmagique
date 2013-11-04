from webapp.poissonmagique.models import Campaign, Human, Character

def find_character(human, campaign=None):
    try:
        if campaign is None:
            return Character.objects.get(controller=human, campaign__is_active=True)
        else:
            return Character.objects.get(controller=human, campaign=campaign)
    except Character.DoesNotExist:
        return None
