from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newListing", views.newListing, name="newListing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/betweenWatchList", views.betweenWatchList, name="betweenWatchList"),
    path("bidding", views.bidding, name="bidding"),
    path("listing/<int:listing_id>/close", views.close, name="close"),
    path("<int:listing_id>/add_comment", views.add_comment, name="add_comment"),
    path("watchLister", views.watchLister, name="watchLister"),
    path("categories", views.categories, name="categories"),
    path("<int:listing_cat>/listingCategory", views.listingCategory, name="listingCategory")
    # path("<int:listing_id>/bidding", views.bidding, name="bidding")
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

