from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import Persoon

@receiver(post_save, sender=get_user_model())
def create_profile(sender, **kwargs):
    '''
    Associate a Persoon with newly created users. The following possibilities arise:
    1. There already is a unnassiociated Persoon with the same email address
    2. There is no unnassociated Persoon with the same email address
    3. There are multiple unnassiociated Personen with the same email address
       (this shouldn't happen in practice, but it is allowed by the database)
    4. The user's email address is empty (because the user was created in the admin)
    5. The user is already associated with a Persoon

    Read the code to see what happens in each of these situations!
    '''

    user = kwargs["instance"]

    try:
        p = user.persoon
    except Persoon.DoesNotExist:
        p = Persoon.objects.filter(email=user.email, user=None).first() if user.email else None
    if not p:
        p = Persoon(email=user.email)

    if not p.voornaam:
        p.voornaam = user.first_name
    if not p.achternaam:
        p.achternaam = user.last_name

    p.user = user
    p.save()
