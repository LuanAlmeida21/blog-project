from site_setup.models import SiteSetup


def site_setup_context(request):
    site_setup = SiteSetup.objects.order_by('-id').first()

    return {
        'site_setup': site_setup
    }
