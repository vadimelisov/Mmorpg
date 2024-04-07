from django.urls import path

from board.views import PostsList, PostDetail, PostCreate, ReplyAdd, PostEdit, Replies, delete_reply, delete_post, \
   allow_reply, news_send

urlpatterns = [
   path('', PostsList.as_view(), name='posts'),
   path('<int:pk>', PostDetail.as_view(), name='post'),
   path('create/', PostCreate.as_view(), name='postcreate'),
   path('<int:pk>/reply/add', ReplyAdd.as_view(), name='reply_add'),
   path('<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
   path('replies/', Replies.as_view(), name='replies'),
   path('delete/<int:pk>', delete_reply, name='delete_reply'),
   path('<int:pk>/delete', delete_post, name='delete_post'),
   path('<int:pk>/allow', allow_reply, name='allow_reply'),
   path('send_mails/', news_send, name='send_mails'),
]
