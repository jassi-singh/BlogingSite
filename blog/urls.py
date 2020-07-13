from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('post_list/',views.PostListView.as_view(),name = 'postlist'),
    path('post_detail/<slug:pk>/',views.PostDetailView.as_view(),name = 'postdetail'),
    path('post_create/',views.PostCreateView.as_view(),name='postcreate'),
    path('<slug:pk>/post_update/',views.PostUpdateView.as_view(),name='postupdate'),
    path('<slug:pk>/post_delete/',views.PostDeleteView.as_view(),name='postdelete'),
    path('drafts/',views.Drafts.as_view(),name='drafts'),
    path('<slug:pk>/publish/',views.publish,name='publish'),
    path('<slug:pk>/comment_approve/',views.comment_approve,name='approve_comment'),
    path('<slug:pk>/comment_remove/',views.comment_remove,name='commentremove'), 
    # path('<slug:pk>/comment_form',require_POST(views.MyFormView.as_view()),name='commentform'),
    # path('<slug:pk>/add_comment/',views.PostDetailView.add_comment_to_post,name='addcomment'),
    # path('<slug:pk>/add_comment/',views.add_comment_to_post,name='addcomment'),
]
      