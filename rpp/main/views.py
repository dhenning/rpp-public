from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import NewUserForm, Raidersform, ProfileUserForm
from .models import Effect
from collections import OrderedDict
from .fusioncharts import FusionCharts
from django.core.paginator import Paginator
from urllib.request import urlopen
import json
import requests
import random


def homepage(request):
    with open("/var/www/rpp/main/leaderboard.json", "r") as f:
        ranking = json.load(f)
    return render(request=request,
                  template_name="main/home.html",
                  context={'ranking': ranking["board"]})


def redirect_homepage(request):
    return redirect('/index.html')


def register(request):
    if request.method == 'POST':
        userform = NewUserForm(request.POST)
        raiderform = Raidersform(request.POST)
        if userform.is_valid() and raiderform.is_valid():
            user = userform.save()
            raider = raiderform.save(commit=False)
            raider.user = user
            raider.save()
            username = userform.cleaned_data.get('username')
            messages.success(request, f"new account created: {username}")
            login(request, user)
            return redirect("main:homepage")
        else:
            for msg in userform.error_messages:
                messages.error(request, f"{msg}: {userform.error_messages[msg]}")
            for msg in raiderform.error_messages:
                messages.error(request, f"{msg}: {raiderform.error_messages[msg]}")

    userform = NewUserForm
    raiderform = Raidersform
    return render(request=request,
                  template_name="main/register.html",
                  context={'userform': userform,
                           'raiderform': raiderform})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="main/login.html",
                  context={"form": form})


def update_profile(request):
    if request.method == 'POST':
        userform = ProfileUserForm(request.POST, instance=request.user)
        raiderform = Raidersform(data=request.POST, files=request.FILES, instance=request.user.raider)
        if userform.is_valid() and raiderform.is_valid():
            userform.save()
            raiderform.save()
            messages.info(request, f"You updated your profile: {request.user.username}")
            return redirect("main:profile")
        else:
            for e in userform.errors:
                messages.error(request, ("error :" + e))
    userform = ProfileUserForm(instance=request.user)
    raiderform = Raidersform(instance=request.user.raider)
    return render(request=request,
                  template_name="main/profile.html",
                  context={'userform': userform,
                           'raiderform': raiderform})


def streams(request):
    The_Fimm_Tis = list(User.objects.filter(groups__name__in=['The Fimm-Ti']))
    Berserkers = list(User.objects.filter(groups__name__in=['Berserker']))
    Huskarls = list(User.objects.filter(groups__name__in=['Huskarl']))
    Thegs = list(User.objects.filter(groups__name__in=['Theg']))
    Gesiths = list(User.objects.filter(groups__name__in=['Gesith']))
    Bondis = list(User.objects.filter(groups__name__in=['Bondi']))
    Drengs = list(User.objects.filter(groups__name__in=['Dreng']))
    Karls = list(User.objects.filter(groups__name__in=['Karl']))
    Folcs = list(User.objects.filter(groups__name__in=['Folc']))
    Honorary = list(User.objects.filter(groups__name__in=['Honorary Streamer/Raider']))
    admins = list(User.objects.filter(groups__name__in=['admin']))
    gothis = list(User.objects.filter(groups__name__in=['gothi']))
    raiders_by_rank_pages = [
        Honorary,
        admins,
        gothis,
        The_Fimm_Tis,
        Berserkers,
        Huskarls,
        Thegs,
        Gesiths,
        Bondis,
        Drengs,
        Karls,
        Folcs
    ]
    if is_live_stream('raidingpartyplusofficial', 'lco2tcyas5wk310a5fhajcsofmb9fl'):
        return render(request=request,
                      template_name="main/raid.html",)
    paginator = Paginator(raiders_by_rank_pages, 1)
    page = request.GET.get('page')
    if page is None:
        page = "1"
    pages = paginator.get_page(page)
    is_live = []
    for streamer in raiders_by_rank_pages[int(page) - 1]:
        if streamer.raider.twitch_name is None or streamer.raider.twitch_name == "None":
            continue
        live = is_live_stream(streamer.raider.twitch_name, 'lco2tcyas5wk310a5fhajcsofmb9fl')
        if live:
            is_live.append(streamer)

    if page == '1' or page == '2' or page == '3':
        return render(request=request,
                      template_name="stream/stream.html",
                      context={"pages": pages,
                               "groups": is_live})
    else:
        if is_live:
            nines = request.GET.get('nines')
            paginator2 = Paginator(is_live, 9)
            pages2 = paginator2.get_page(nines)
            if nines is None or nines == "1":
                return render(request=request,
                              template_name="stream/stream.html",
                              context={"pages": pages,
                                       "nines": pages2,
                                       "groups": is_live[0:]})
            else:
                return render(request=request,
                              template_name="stream/stream.html",
                              context={"pages": pages,
                                       "nines": pages2,
                                       "groups": is_live[9*(int(nines)-1):]})
        else:
            return render(request=request,
                          template_name="stream/stream.html",
                          context={"pages": pages,
                                   "groups": is_live})


def ranks(request):
    return render(request=request,
                  template_name="main/ranks.html")


def leaderboard(request):
    with open("/var/www/rpp/main/leaderboard.json", "r") as f:
        ranking = json.load(f)
    return render(request=request,
                  template_name="main/leaderboard.html",
                  context={"ranking": ranking["board"]})


def store(request):
    return render(request=request,
                  template_name="store/store.html")


def effect(request):
    effect_list = list(Effect.objects.all())
    effects = random.sample(effect_list, 3)
    return render(request=request,
                  template_name="main/effect.html",
                  context={"effects": effects})


def the_team(request):
    admins = list(User.objects.filter(groups__name__in=['admin']))
    gothis = list(User.objects.filter(groups__name__in=['gothi']))
    return render(request=request,
                  template_name="main/the_team.html",
                  context={"admins": admins,
                           "gothis": gothis})


def calendar(request):
    return render(request=request,
                  template_name="main/calendar.html")


def one(request):
    return render(request=request,
                  template_name="materialize_sandbox/index.html")


def two(request):
    return render(request=request,
                  template_name="materialize_sandbox/index2.html")


def auth(request):
    '''
    :param request: post from login discoed
    :return:
    username verified locale premium_type mfa_enabled id flags avatar discriminator email
    {
      "id": "number",
      "username": "name",
      "discriminator": "tag",
      "avatar": "?",
      "verified": bool,
      "email": "email"
    }
    connection of linked apps
    [{
    'verified': bool, 'name': 'name of account', 'show_activity': bool, 'friend_sync': bool,
     'type': 'the app connection', 'id': 'int_str', 'visibility': int}
    },]
    '''
    code = request.GET.get("code")
    if code:
        with open('/var/www/rpp/main/main_settings.json', 'r') as f:
            settings = json.load(f)
        API_ENDPOINT = 'https://discordapp.com/api/v6'
        clint_id = settings['Oauth']['id']
        clint_secret = settings['Oauth']['secret']
        redirect_uri = settings['Oauth']['uri']
        discord_user_payload = {
            'client_id': clint_id,
            'client_secret': clint_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'scope': 'identify email connections'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        access_token = requests.post('%s/oauth2/token' % API_ENDPOINT, discord_user_payload, headers)
        access_token.raise_for_status()
        access_token = access_token.json()
        url = API_ENDPOINT + "/users/@me"
        headers_2 = {
            'Authorization': 'Bearer {}'.format(access_token["access_token"])
        }
        discord_user_json = requests.get(url=url, headers=headers_2)
        discord_user_json = discord_user_json.json()
        discord_plus_tag = discord_user_json["username"] + "#" + discord_user_json["discriminator"]
        user = User.objects.filter(username=request.user.username).first()
        user.raider.discord_user = discord_plus_tag
        url2 = API_ENDPOINT + "/users/@me/connections"
        user_connection_json = requests.get(url=url2, headers=headers_2)
        for conn in user_connection_json.json():
            if conn['type'] == "twitter":
                user.raider.twitter_name = conn['name']
            elif conn['type'] == "twitch":
                user.raider.twitch_name = conn['name']
            elif conn['type'] == "youtube":
                user.raider.youtube_channel = conn['name']
        user.raider.save()
        messages.success(request, "linked discord")
        return redirect("main:profile")
    else:
        messages.error(request, 'did not link with discord')
        return redirect("main:homepage")


def discord_link(request):
    with open('/var/www/rpp/main/main_settings.json', 'r') as f:
        settings = json.load(f)
    clint_id = settings['Oauth']['id']
    scope = settings['Oauth']['scope']
    redirect_uri = settings['Oauth']['uri']
    discord_login_url = "https://discordapp.com/api/oauth2/authorize?client_id={}&redirect_uri={}&auth&response_type=code&scope={}".format(
        clint_id, redirect_uri, scope)
    return redirect(discord_login_url)


def rpp(request):
    return render(request=request,
                  template_name="old_site/rpp.html")


def handler404(request, exception, template_name="404.html"):
    response = render_to_response("404.html")
    response.status_code = 404
    return render(request=request,
                  template_name="404.html")


def handler500(request, exception, template_name="500.html"):
    response = render_to_response("500.html")
    response.status_code = 500
    return render(request=request,
                  template_name="500.html")


def handler400(request, exception, template_name="404.html"):
    response = render_to_response("400.html")
    response.status_code = 400
    return render(request=request,
                  template_name="400.html")


def handler403(request, exception, template_name="500.html"):
    response = render_to_response("403.html")
    response.status_code = 403
    return render(request=request,
                  template_name="403.html")


def is_live_stream(streamer_name, twitch_client_id):
    url = "https://api.twitch.tv/kraken/streams/" + streamer_name + "?client_id=" + twitch_client_id
    data = json.loads(urlopen(url, timeout=15).read().decode('utf-8'))
    return data["stream"] is not None


def maps(request):
    return render(request=request,
                  template_name="main/map.html")




