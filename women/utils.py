from django.core.cache import cache
from django.db.models import Count

from .models import *

menu = [{'title': 'About website', 'url_name': 'about'},
        {'title': 'Add article', 'url_name': 'addpage'},
        {'title': 'Feedback', 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 3  # define the number of elements on one page (we use Paginator's class)

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('women'))  # we did it because we have to get count of women's objects
            cache.set('cats', cats, 60)
        context['cats'] = cats
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        context['menu'] = user_menu
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
