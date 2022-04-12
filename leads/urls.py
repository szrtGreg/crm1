from django.urls import path
from .views import lead_list, lead_detail


urlpatterns = [
    path('', lead_list),
    path('<pk>/', lead_detail),

]
