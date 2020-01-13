from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from .views import *

urlpatterns = [
    path('init/', InitGame.as_view(), name='api-init-game'),
    path('round/', InitRound.as_view(), name='api-init-round'),
    path('submit/', RoundSubmit.as_view(), name='api-submit-round'),
    path('project/', ProjectView.as_view(), name='api-show-project'),
    path('wallet/', WalletAnalysisView.as_view(), name='api-show-wallet'),
]