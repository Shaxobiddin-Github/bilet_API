from django.urls import path, include
from .views import SamDUkfDocViewSet, UploadQuestions, GenerateTickets, ExportTickets
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (
     UquvYiliViewSet, BosqichViewSet, TalimYunalishiViewSet,
    SemestrViewSet, FanViewSet, SamDUkfViewSet
)
router = DefaultRouter()

router.register(r'uquv-yili', UquvYiliViewSet)
router.register(r'bosqich', BosqichViewSet)
router.register(r'talim-yunalishi', TalimYunalishiViewSet)
router.register(r'semestr', SemestrViewSet)
router.register(r'fan', FanViewSet)
router.register(r'samdukf', SamDUkfViewSet)
router.register(r'samdukfdoc', SamDUkfDocViewSet)


app_name = "api"

urlpatterns = [
    path('upload/', UploadQuestions.as_view(), name='upload_questions'),
    path('generate_tickets/', GenerateTickets.as_view(), name='generate_tickets'),
    path('export_tickets/', ExportTickets.as_view(), name='export_tickets'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),

]