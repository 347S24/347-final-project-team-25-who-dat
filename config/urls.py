# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from whodat.homepage.views import homepage

urlpatterns = [
    # path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("", homepage, name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("tictactoe.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("whodat/", include("whodat.whodat.urls", namespace="whodatpages")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path("400/", default_views.bad_request, kwargs={"exception": Exception("Bad Request!")}),
        path("403/", default_views.permission_denied, kwargs={"exception": Exception("Permission Denied")}),
        path("404/", default_views.page_not_found, kwargs={"exception": Exception("Page not Found")}),
        path("500/", default_views.server_error),
    ]

    # Add Django Debug Toolbar
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

# Note that custom_404 is not used; if you want to use a custom 404 view, you should set it in your settings.py like so:
# handler404 = 'path.to.custom_404'
