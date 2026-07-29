from django.conf import settings


def site_meta(request):
    """
    Site-wide constants for use in base.html and the SEO block, so every
    template has access to consistent defaults without repeating them.
    """
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_TAGLINE": settings.SITE_TAGLINE,
        "SITE_DEFAULT_DESCRIPTION": settings.SITE_DEFAULT_DESCRIPTION,
        "SITE_DOMAIN": settings.SITE_DOMAIN,
        "SOCIAL_INSTAGRAM": settings.SOCIAL_INSTAGRAM,
    }
