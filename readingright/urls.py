from rest_framework_simplejwt import views as jwt_views
from django.contrib import admin
from django.urls import path
from main import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('additem', views.AddItemView)
router.register('saveitem', views.SavedItemView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', views.UserAPIVIEW.as_view()),
    path('user/<int:pk>', views.UserAPIVIEW.as_view()),
    path('createuser/', views.UserSignupAPIVIEW.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('item/', views.ItemView.as_view()),
    path('item/<int:pk>', views.ItemView.as_view()),
    path('api/', include(router.urls)),
    path('', views.Home, name="Home"),
    path('additem/', views.AddItem, name="Add Item"),
    path('saveditem/', views.SavedItem, name="Saved List"),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(STATIC_URL,document_root=STATIC_ROOT)
