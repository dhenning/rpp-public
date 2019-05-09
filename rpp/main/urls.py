"""rpp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.redirect_homepage, name="index"),
    path("index.html/", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("profile/", views.update_profile, name="profile"),
    path("streams/", views.streams, name="streams"),
    path("ranks/", views.ranks, name="ranks"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("store/", views.store, name="store"),
    path("effect/", views.effect, name="effect"),
    path("team/", views.the_team, name="team"),
    path("one/", views.one, name="one"),
    path("two/", views.two, name="two"),
    path("calendar/", views.calendar, name="calendar"),
    path("maps/", views.maps, name="maps"),
    path("auth/", views.auth, name="auth"),
    path("rpp/", views.rpp, name="rpp"),
    path("discord_link/", views.discord_link, name="discord_link")
]

handler404 = 'my_app.views.handler404'
handler500 = 'my_app.views.handler500'
handler403 = 'my_app.views.handler403'
handler400 = 'my_app.views.handler400'