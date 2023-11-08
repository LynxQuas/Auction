from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Categories(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"
    

class Bids(models.Model):
    bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")

    def __str__(self):
        return f"{self.user}: {self.bid}"
    

class AuctionListings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length = 500)
    price = models.IntegerField()
    status = models.BooleanField(default=True)
    photo = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    bid = models.ForeignKey(Bids, on_delete=models.CASCADE, related_name="bid_lists")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="list_category")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_auction_listings")
    
    watchlists = models.ManyToManyField(User, blank=True, related_name="user_watchlist")

    def __str__(self):
        return f"TITLE: {self.title} | PRICE: {self.price} | CREATED_BY: {self.created_by}"
    

class Comments(models.Model):
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="post_comment")
    comment = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.comment_by}: {self.comment}"
    



