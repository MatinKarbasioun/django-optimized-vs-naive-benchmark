from django.urls import path

from AnchorTrader.API import AnchorAlgorithm

urlpatterns = [
    path('', AnchorAlgorithm.as_view(), name='anchor_algorithm')
]
