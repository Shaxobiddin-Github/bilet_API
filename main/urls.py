from django.urls import path
from .views import SamDUkfViewSet, UploadQuestions, GenerateTickets, ExportTickets
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


samdukf_list = SamDUkfViewSet.as_view({'get': 'list', 'post': 'create'})


urlpatterns = [
    path('upload/', UploadQuestions.as_view(), name='upload_questions'),
    path('generate/', GenerateTickets.as_view(), name='generate_tickets'),
    path('export/', ExportTickets.as_view(), name='export_tickets'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('samdukf/', samdukf_list, name='samdukf-list'), 

]