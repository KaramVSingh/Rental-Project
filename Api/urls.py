from django.conf.urls import url
from Api import views

urlpatterns = [
    url(r'^users/$', views.users),
    url(r'^users/(?P<pk>[0-9]+)/$', views.specific_user),
    url(r'^users/(?P<pk>[0-9]+)/userroles/$', views.specific_user_user_roles),
    url(r'^users/(?P<pk>[0-9]+)/autos/$', views.specific_user_autos),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^roles/$', views.roles),
    url(r'^roles/(?P<pk>[a-zA-Z]+)/$', views.specific_role),
    url(r'^userroles/$', views.user_roles),
    url(r'^userroles/(?P<pk>[0-9]+)/$', views.specific_user_role),
    url(r'^partners/$', views.partners),
    url(r'^partners/(?P<pk>[0-9]+)/$', views.specific_partner),
    url(r'^partners/(?P<pk>[0-9]+)/users/$', views.specific_partner_users),
    url(r'^airports/$', views.airports),
    url(r'^airports/(?P<pk>[a-zA-Z]+)/$', views.specific_airport),
    url(r'^autotypes/$', views.autotypes),
    url(r'^autotypes/(?P<pk>[0-9]+)/$', views.specific_autotype),
    url(r'^autos/$', views.autos),
    url(r'^autos/(?P<pk>[0-9]+)/$', views.specific_auto),
    url(r'^companydefaults/$', views.company_defaults),
    url(r'^itineraries/$', views.itineraries),
    url(r'^itineraries/(?P<pk>[0-9]+)/$', views.specific_itinerary),
    url(r'^sublettables/$', views.sublettables),
    url(r'^sublettables/(?P<pk>[0-9]+)/$', views.specific_sublettable),
    url(r'^parks/$', views.parks),
    url(r'^parks/(?P<pk>[0-9]+)/$', views.specific_park),
    url(r'^cleardatabase/$', views.clear_database),
]