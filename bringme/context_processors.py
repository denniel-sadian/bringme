from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def others(request):
    """Adds more context."""
    site = get_current_site(request)
    return {
        'domain': site.domain,
        'protocol': 'http{}'.format('s' if settings.USE_HTTPS else ''),
        'STATIC_PREFIX': 'http{}://{}'.format('s' if settings.USE_HTTPS else '', site.domain)
    }