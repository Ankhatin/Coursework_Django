from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import IndexView, NewsletterListView, NewsletterCreateView, NewsletterDetailView, \
    NewsletterUpdateView, NewsletterDeleteView, MessageListView, MessageDetailView, MessageCreateView, \
    MessageUpdateView, MessageDeleteView, ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, \
    ClientCreateView, ReportView

app_name = MailingConfig.name


urlpatterns = [
    path('',IndexView.as_view(), name='index'),
    path('mailings/', NewsletterListView.as_view(), name='newsletter_list'),
    path('mailings/report', ReportView.as_view(), name='report'),
    path('newsletter/<int:pk>', NewsletterDetailView.as_view(), name='newsletter'),
    path('create/', NewsletterCreateView.as_view(), name='create'),
    path('edit/<int:pk>', NewsletterUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', NewsletterDeleteView.as_view(), name='delete'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/message/<int:pk>', MessageDetailView.as_view(), name='message'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/edit/<int:pk>', MessageUpdateView.as_view(), name='message_edit'),
    path('messages/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/client/<int:pk>', ClientDetailView.as_view(), name='client'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/edit/<int:pk>', ClientUpdateView.as_view(), name='client_edit'),
    path('clients/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)