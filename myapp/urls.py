
from django.urls import path
from . import views
app_name='myapp'

urlpatterns = [
    path('',views.index,name='index'),
    path('author/<name>',views.getauthor,name='author'),
    path('article/<int:id>',views.getsingle,name='single_post'),
    path('topic/<name>',views.getTopic,name='topic'),
    path('login',views.getLogin,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('create',views.getCreate,name='create'),
    path('profile',views.getProfile,name='profile'),
    path('update/<int:id>',views.getUpdate,name='update'),
    path('delete/<int:id>',views.getDelete,name='delete'),
    path('signup',views.getRegister,name='signup'),
    path('category',views.getCategory,name='category'),
    path('create/topic',views.createTopic,name='createTopic'),
    path('pdf/<int:id>',views.pdf.as_view(),name='pdf'),

]
