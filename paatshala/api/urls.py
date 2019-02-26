from django.conf.urls import url
from api import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('register', views.register, name="register"),
    
    # url(
    #     r'^updatebio/(?P<useremail>\S+)/',
    #     views.profileBio,
    #     name="profile_bio"
    # ),
    # url(
    #     r'^updateeducation/(?P<useremail>\S+)/',
    #     views.profileEducation,
    #     name="profile_education"
    # ),

    url('updatebio', views.profileBio, name="profile_bio"),
    url('updateeducation', views.profileEducation, name="profile_education"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)