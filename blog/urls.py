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
    path('mygroup_list/',views.MygroupListView.as_view(),name = 'mygrouplist'),
    path('<slug:pk>/join_group/',views.join_group,name = 'joingroup'),
    path('<slug:pk>/leave_group/',views.leave_group,name = 'leavegroup'),
    path('<slug:pk>/mygroup/',views.MygroupDetailView.as_view(),name='group'),
    path('<slug:pk>/mygroup_delete/',views.delete_group,name='groupdelete'),
    path('<slug:pk>/mygroup/remove/<slug:sk>/',views.delete_member,name='remove_member'),
]
      