from django.conf.urls import patterns, include, url
from members import views as member_views
from balance_and_dividend import views as balance_and_dividend_views
from loan import views as loan_views
from aausca_site import views as aausca_site_views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'final_project.views.home', name='home'),
    # url(r'^final_project/', include('final_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/',include(admin.site.urls)),
    url(r'^home_page/',aausca_site_views.home_page),
    url(r'^register_page/',aausca_site_views.register_page),
    url(r'^request_loan/',loan_views.request_loan_page),
    url(r'^register_member/',aausca_site_views.register_member),
    url(r'^view_profile/',aausca_site_views.view_profile),
    url(r'^edit_profile/',aausca_site_views.edit_profile),
    url(r'^extend_loan/',aausca_site_views.extend_loan),
    url(r'^transactions/',aausca_site_views.transactions),
    url(r'^logout/',aausca_site_views.logout),
    url(r'^member_login/',aausca_site_views.member_login),
    url(r'^member_logout/',aausca_site_views.member_logout), 

    url(r'^loan_request/',loan_views.loan_request),       

    url(r'^member_edit_profile/',aausca_site_views.member_edit_profile),
    url(r'^login_page/',aausca_site_views.login_page),
    url(r'^apply/',aausca_site_views.apply),
    url(r'^login/',aausca_site_views.login),
    url(r'^member/',aausca_site_views.member_home),
    url(r'^member_loan_request/',loan_views.member_loan_request),
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
