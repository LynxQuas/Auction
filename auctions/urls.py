from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("listings/<int:list_id>", views.listings, name="listings"),
    path("categories", views.categories, name="categories"),

    path("watchlists", views.watchlists, name="watchlists"),
    path("addWatchlist/<int:list_id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist<int:list_id>", views.remove_watchlist, name="remove_watchlist"),
    path("addBid/<int:list_id>", views.add_bid, name="add_bid"),
    path("closeAuction/<int:list_id>", views.close_auction, name="close_auction"),
]
