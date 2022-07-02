from django.urls import include, path

from core.views import CreateUserView, CurrentUserView, LoginUserView
from core.views import GetUsersView

urlpatterns = [
    path('<user_type>/create/', CreateUserView.as_view(), name='create user'),
    path('<user_type>/login/', LoginUserView.as_view(), name='login user'),
    path('<user_type>/', GetUsersView.as_view(), name='get all user'),
    path('user/', CurrentUserView.as_view(), name='current user operations'),
]