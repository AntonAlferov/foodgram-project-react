from django.contrib import admin

from .models import (CountIngredient, Favorited, Follow, Ingredient, Recipe,
                     ShoppingCart, Tag)


class CountIngredientInline(admin.TabularInline):

    model = CountIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (CountIngredientInline,)
    list_display = ('name', 'author', 'in_favored')
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('in_favored',)

    def in_favored(self, obj):
        return obj.FavoritedIsRecipe.count()
    in_favored.short_description = 'Количество в избранных'


class IngredientAdmin(admin.ModelAdmin):
    inlines = (CountIngredientInline,)
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    fields = ('name', 'color', 'slug')


class FavoritedAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_favorited')
    list_filter = ('user', 'is_favorited')


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_in_shopping_cart')
    list_filter = ('user', 'is_in_shopping_cart')


class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_in_shopping_cart')
    list_filter = ('user', 'is_in_shopping_cart')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user_follower', 'author_following')
    list_filter = ('user_follower', 'author_following')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorited, FavoritedAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Follow, FollowAdmin)


admin.site.site_header = 'Администратор Продуктовый Помощник'
