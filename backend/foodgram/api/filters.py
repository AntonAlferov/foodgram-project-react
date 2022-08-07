from django_filters import rest_framework as filters


class FilterRecipe(filters.FilterSet):
    is_favorited = filters.NumberFilter(
        method='is_favorited_filter',
        label="Показывать только рецепты, находящиеся в списке избранного"
    )
    is_in_shopping_cart = filters.NumberFilter(
        method='is_in_shopping_cart_filter',
        label="Показывать только рецепты, находящиеся в списке покупок."
    )
    author = filters.CharFilter(field_name='author')
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')

    def is_favorited_filter(self, queryset, name, value):
        if value == 1:
            return queryset.filter(FavoritedIsRecipe__user=self.request.user)
        return queryset.exclude(FavoritedIsRecipe__user=self.request.user)

    def is_in_shopping_cart_filter(self, queryset, name, value):
        if value == 1:
            return queryset.filter(ShoppingCartRecipe__user=self.request.user)
        return queryset.exclude(ShoppingCartRecipe__user=self.request.user)
