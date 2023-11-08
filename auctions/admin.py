from django.contrib import admin
from .models import *
# Register your models here.

class AuctionListingsAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "created_by", )

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("category", )

class BidsAdmin(admin.ModelAdmin):
    list_display = ("user", "bid")

class CommentsAdmin(admin.ModelAdmin):
    list_display = ("comment_by", "comment",)

class UserAdmin(admin.ModelAdmin):
    list_display =("username", )


admin.site.register(AuctionListings, AuctionListingsAdmin )
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Comments, CommentsAdmin )
admin.site.register(User, UserAdmin )
admin.site.register(Bids, BidsAdmin )