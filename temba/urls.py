from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.i18n import JavaScriptCatalog

from temba.channels.views import register, sync

# javascript translation packages
js_info_dict = {"packages": ()}  # this is empty due to the fact that all translation are in one folder

urlpatterns = [
    url(r"^", include("temba.airtime.urls")),
    url(r"^", include("temba.api.urls")),
    url(r"^", include("temba.apks.urls")),
    url(r"^", include("temba.archives.urls")),
    url(r"^", include("temba.campaigns.urls")),
    url(r"^", include("temba.channels.urls")),
    url(r"^", include("temba.classifiers.urls")),
    url(r"^", include("temba.contacts.urls")),
    url(r"^", include("temba.dashboard.urls")),
    url(r"^", include("temba.flows.urls")),
    url(r"^", include("temba.globals.urls")),
    url(r"^", include("temba.ivr.urls")),
    url(r"^", include("temba.locations.urls")),
    url(r"^", include("temba.msgs.urls")),
    url(r"^", include("temba.notifications.urls")),
    url(r"^", include("temba.policies.urls")),
    url(r"^", include("temba.public.urls")),
    url(r"^", include("temba.request_logs.urls")),
    url(r"^", include("temba.schedules.urls")),
    url(r"^", include("temba.tickets.urls")),
    url(r"^", include("temba.triggers.urls")),
    url(r"^", include("temba.orgs.urls")),
    url(r"^relayers/relayer/sync/(\d+)/$", sync, {}, "sync"),
    url(r"^relayers/relayer/register/$", register, {}, "register"),
    url(r"users/user/forget/", RedirectView.as_view(pattern_name="orgs.user_forget", permanent=True)),
    url(r"^users/", include("smartmin.users.urls")),
    url(r"^imports/", include("smartmin.csv_imports.urls")),
    url(r"^assets/", include("temba.assets.urls")),
    url(r"^jsi18n/$", JavaScriptCatalog.as_view(), js_info_dict, name="django.views.i18n.javascript_catalog"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# import any additional urls
for app in settings.APP_URLS:  # pragma: needs cover
    urlpatterns.append(url(r"^", include(app)))


def handler500(request):
    """
    500 error handler which includes ``request`` in the context.

    Templates: `500.html`
    Context: None
    """
    from django.template import loader
    from django.http import HttpResponseServerError

    t = loader.get_template("500.html")
    return HttpResponseServerError(t.render({"request": request}))  # pragma: needs cover
