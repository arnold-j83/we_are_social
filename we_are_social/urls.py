from django.conf.urls import url, include
from django.contrib import admin
from home import views as home_views
from accounts import views as accounts_views
from paypal.standard.ipn import urls as paypal_urls
from paypal_store import views as paypal_views
from products import views as product_views
from magazines import views as magazines_views
from threads import views as forum_views
from polls import api_views
from threads import api_views as thread_api_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_views.get_index, name='index'),
    url(r'^register/$', accounts_views.register, name='register'),
    url(r'^profile/$', accounts_views.profile, name='profile'),
    url(r'^login/$', accounts_views.login, name='login'),
    url(r'^logout/$', accounts_views.logout, name='logout'),
    url(r'^cancel_subscription/$', accounts_views.cancel_subscription, name='cancel_subscription'),
    #url(r'^subscriptions_webhook/$', accounts_views.subscriptions_webhook, name='subscriptions_webhook'),
    url(r'^a-very-hard-to-guess-url/', include(paypal_urls)),

    url(r'^paypal-return/$', paypal_views.paypal_return),
    url(r'^paypal-cancel/$', paypal_views.paypal_cancel),
    url(r'^products/$', product_views.all_products, name='products'),
    url(r'^magazines/$', magazines_views.all_magazines, name='magazines'),
    url(r'^forum/$', forum_views.forum, name='forum'),
    url(r'^threads/(?P<subject_id>\d+)/$', forum_views.threads, name='threads'),
    url(r'^new_thread/(?P<subject_id>\d+)/$', forum_views.new_thread, name='new_thread'),
    url(r'^thread/(?P<thread_id>\d+)/$', forum_views.thread, name='thread'),
    url(r'^post/new/(?P<thread_id>\d+)/$', forum_views.new_post, name='new_post'),
    url(r'^post/edit/(?P<thread_id>\d+)/(?P<post_id>\d+)/$',forum_views.edit_post, name='edit_post'),
    url(r'^post/delete/(?P<thread_id>\d+)/(?P<post_id>\d+)/$', forum_views.delete_post, name='delete_post'),
    url(r'^thread/vote/(?P<thread_id>\d+)/(?P<subject_id>\d+)/$', forum_views.thread_vote, name='cast_vote'),
    url(r'^threads/polls/$', api_views.PollViewSet.as_view(), name='threads_poll_api1'),
    url(r'^threads/polls/(?P<pk>[\d]+)$', api_views.PollInstanceView.as_view(), name='poll-instance'),
    url(r'^threads/polls/vote/(?P<thread_id>\d+)/$', api_views.VoteCreateView.as_view(), name='create_vote'),
    url(r'^threads/threads/$', api_views.ThreadViewSet.as_view(), name='threads_threads'),
    url(r'^threads/post/update/(?P<pk>[\d+]+)/$', thread_api_views.PostUpdateView.as_view(),
        name="update-poll"),
    url(r'^threads/post/delete/(?P<pk>[\d]+)/$', thread_api_views.PostDeleteView.as_view(), name='delete-poll'),

]
