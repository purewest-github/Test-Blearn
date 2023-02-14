from django.urls import path, include
# from django.contrib import admin


from .views import signupfunc, loginfunc, logoutfunc, ContentCreate, ContentList, ContentDetail, ContentUpdate, ContentDelete


urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('logout/', logoutfunc, name='logout'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('detail/<int:pk>', ContentDetail.as_view(), name='detail'),
    path('list/', ContentList.as_view(), name='list'),
    path('create/', ContentCreate.as_view(), name='create'),
    path('update/<int:pk>', ContentUpdate.as_view(), name='update'),
    path('delete/<int:pk>', ContentDelete.as_view(), name='delete'),
]