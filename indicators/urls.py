from django.contrib import admin
from django.urls import path
from . import views

#import dash functions here
# from indicators.dash_apps.finished_apps import simpleexample
# from indicators.deneme import django_dash
# from .dash_apps.finished_apps import simpleexample
#end dash functions

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.homeView, name="home"),

    path('crypto', views.cryptoView, name="crypto"),

    path('candlestick/', views.candlestick, name='indicators-candlestick'),
    path('bbands/', views.bbands, name='indicators-bbands'),
    path('rsi/', views.rsi, name='indicators-rsi'),
    path('supertrend/', views.supertrend, name='indicators-supertrend'),
    path('macd/', views.macd, name='indicators-macd'),
    path('williams_r_percent/', views.williams_r_percentage, name='indicators-williams_r_percent'),
    path('sma/', views.sma, name='indicators-sma'),
    path('stochastic/', views.stochastic, name='indicators-stochastic'),
    path('cci/', views.cci, name='indicators-cci'),
    path('adx/', views.adx, name='indicators-adx'),
    path('aroon/', views.aroon, name='indicators-aroon'),
    path('kc/', views.kc, name='indicators-kc'),
    path('tsi/', views.tsi, name='indicators-tsi'),
    path('ao/', views.ao, name='indicators-ao'),
    path('coppock/', views.coppock, name='indicators-coppock'),
    path('kst/', views.kst, name='indicators-kst'),

    path('history/', views.history, name='indicators-hist'),
]
