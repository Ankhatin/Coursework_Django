from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

from blogs.apps import BlogsConfig
from blogs.views import BlogListView, BlogDetailView

app_name = BlogsConfig.name


urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>', BlogDetailView.as_view(), name="blog"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)