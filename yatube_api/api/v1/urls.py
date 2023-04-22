from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers

from api.v1 import views

router = routers.DefaultRouter()
router.register(r"posts", views.PostViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(
    r"posts/(?P<post_id>\d+)/comments",
    views.CommentViewSet,
    basename="comments",
)
router.register(r"follow", views.FollowViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("", include("djoser.urls.jwt")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
