from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'admin_user'

urlpatterns = [
    path('', views.SignIn.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/profile/edit/', views.ProfileUpdateView.as_view(), name='edit_details'),

    # Reset password
    path('admin/password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('admin/password_reset_confirm/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),

    # path('admin/password_reset/password_reset_email_confirm/',
    #      TemplateView.as_view(template_name="profile/reset_status.html"), name='password_reset_done'),
    # path('admin/password_reset_complete/',
    #      TemplateView.as_view(template_name="profile/reset_status.html"), name='password_reset_complete'),
    path('admin/password_change',
         auth_views.PasswordChangeView.as_view(template_name="profile/password_change.html",
                                               success_url='/dashboard'), name='password_change'),

    # User dashboard
    path('admin/user_list', views.UserListView.as_view(), name='user_list'),
    path('admin/user_list_data', views.user_ajax_list, name='user_list_data'),
    path('admin/user_export', views.UserExportView.as_view(), name='user_export'),
    path('admin/user_detail_view/<int:pk>', views.UserDetailView.as_view(), name='user_detail_view'),
    path('admin/user_create_view', views.UserCreateView.as_view(), name='user_create_view'),
    path('admin/user_update_view/<int:pk>', views.UserUpdateView.as_view(), name='user_update_view'),
    path('admin/user_delete_view/<int:pk>', views.UserDeleteView.as_view(), name='user_delete_view'),

]
