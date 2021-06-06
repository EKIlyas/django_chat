from django.urls import path


from core.views import SubjectView, RoomView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', SubjectView.as_view(), name='main'),
    path('chat/<int:subject_id>/', RoomView.as_view(), name='room'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main'), name='logout'),
]
