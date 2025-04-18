from django.urls import path

from .views import share_cv_email, CVListCreateView, CVRetrieveUpdateDestroyView, cv_list

urlpatterns = [
    path('share/email/<int:cv_id>/', share_cv_email, name='share_cv_email'),
    path('api/cvs/', CVListCreateView.as_view(), name='cv-list-create'), 
    path('api/cvs/<int:pk>/', CVRetrieveUpdateDest), 
    path('cvs/', cv_list, name='cv_list'),  
]