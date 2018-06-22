from accounts.models import Profile


def check_details_status(user):
    """
    Check if user has provided contact details.
    """
    profile = Profile.objects.get(user=user)
    if profile.phone_number and profile.location:
        return True
    else:
        return False
