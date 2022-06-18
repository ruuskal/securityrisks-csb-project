from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('create/', views.create, name='create'),
    path('<int:question_id>/addchoices/', views.addchoices, name='addchoices'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('pollusers/', views.pollusers, name='pollusers'),
    path('<polluser_id>/lastloggedin/', views.lastloggedin, name='lastloggedin'),
]