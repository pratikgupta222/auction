from django.urls import path

from biddings import views

urlpatterns = [
    path('auctions', views.AuctionList.as_view()),
    path('auctions/<int:pk>/', views.AuctionDetails.as_view()),
    path('bids', views.BidList.as_view()),
    path('bids/<int:pk>/', views.BidDetails.as_view()),
]