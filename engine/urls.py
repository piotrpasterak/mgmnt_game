from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from .views import *

urlpatterns = [
    path('init/', InitGame.as_view(), name='api-init-game'),
    path('round/', InitRound.as_view(), name='api-init-round'),
    path('submit/', RoundSubmit.as_view(), name='api-submit-round'),
    path('img/project/<int:round_id>/<int:project_id>.png', ProjectImage, name='api-image-project'),
    path('img/map/<int:round_id>/<str:projects_list>-map.png', WalletImage, name='api-image-wallet'),
    path('project/', ProjectView.as_view(), name='api-show-project'),
    path('wallet/', WalletAnalysisView.as_view(), name='api-show-wallet'),
    path('calculations/', WalletCalculations.as_view(), name='api-calculate-wallet'),
]