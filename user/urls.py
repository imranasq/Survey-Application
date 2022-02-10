from django.urls import path
from .views import hello, LoginView , AdminHomeView, CustomerHomeView, SignUpView, UserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('', hello, name='hello'),
    path('login/', LoginView.as_view(), name="login"),
    path('admin-panel/', AdminHomeView, name="admin_panel"),
    path('customer-panel/', CustomerHomeView, name="customer_panel"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
router = DefaultRouter()
router.register(r"user", UserView, basename="user")
urlpatterns += router.urls
