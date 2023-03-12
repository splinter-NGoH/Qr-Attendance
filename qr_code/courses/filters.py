import django_filters as filters

from sett_elkol.meal.models import Meal


class MealFilter(filters.FilterSet):
    chef_user = filters.CharFilter(
        field_name="chef_user__first_name", lookup_expr="icontains"
    )
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    tags = filters.CharFilter(
        field_name="tags", method="get_article_tags", lookup_expr="iexact"
    )
    created_at = filters.IsoDateTimeFilter(field_name="created_at")
    updated_at = filters.IsoDateTimeFilter(field_name="updated_at")

    class Meta:
        model = Meal
        fields = ["chef_user", "title", "tags", "created_at", "updated_at"]

    def get_article_tags(self, queryset, tags, value):
        tag_values = value.replace(" ", "").split(",")
        return queryset.filter(tags__tag__in=tag_values).distinct()
