from webapp.dice.models import Roll, RollOutcome

def find_roll(hashid):
    try:
        return Roll.objects.get(hashid=hashid)
    except Roll.DoesNotExist:
        return None

def set_roll_outcome(roll, text):
    outcome = RollOutcome(roll=roll, outcome_text=text)
    outcome.save()
