from django.urls import path, re_path

from api.resources import v1


app_name = 'api'

tenant_url = 'tenants/<str:domain>/'
tenant_user_url = 'tenants/<str:domain>/users/<int:tenant_user_id>/'


urlpatterns = [
  path('token/', v1.CustomTokenObtainPairView.as_view(), name='token'),
  path('token/refresh/',
       v1.CustomTokenRefreshView.as_view(),
       name='token_refresh'),
  path('token/verify/', v1.CustomTokenVerifyView.as_view(), name='token_verify'),
  path('token/revoke/', v1.TokenRevokeView.as_view(), name='token_revoke'),
  path('users/', v1.UserListView.as_view(), name='users'),
  path('users/<int:user_id>/', v1.UserView.as_view(), name='user'),
  path('users/<int:user_id>/password/',
       v1.UserPasswordView.as_view(), name='user_password'),
  path('users/<int:user_id>/tenants/',
       v1.UserTenantListView.as_view(), name='user_tenants'),
  path('email/signup/verification/',
       v1.EmailVerificationCodeView.as_view(), name='email_signup_verification'),
  path('password/reset-code/',
       v1.PasswordResetCodeView.as_view(), name='password_reset_code'),
  path('password/reset/', v1.PasswordResetView.as_view(), name='password_reset'),
  path('tenants/', v1.TenantListView.as_view(), name='tenants'),
  path('tenants/invited/', v1.InvitedTenantView.as_view(), name='tenant_invited'),
  path(tenant_url, v1.TenantView.as_view(), name='tenant'),
  path(tenant_url + 'users/',
       v1.TenantUserListView.as_view(), name='tenant_users'),
  path(tenant_user_url, v1.TenantUserView.as_view(), name='tenant_user'),
  path(tenant_url + 'invitation-codes/',
       v1.TenantInvitationCodeListView.as_view(), name='tenant_invitation_codes'),
]
