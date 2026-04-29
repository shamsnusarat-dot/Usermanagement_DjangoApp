import msal
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.models import User


def get_msal_app():
    return msal.ConfidentialClientApplication(
        settings.AZURE_CLIENT_ID,
        authority=settings.AZURE_AUTHORITY,
        client_credential=settings.AZURE_CLIENT_SECRET,
    )


def ms_login(request):
    if request.session.get('user'):
        return redirect('user-list-template')
    auth_url = get_msal_app().get_authorization_request_url(
        settings.AZURE_SCOPE,
        redirect_uri=settings.AZURE_REDIRECT_URI,
        state=request.session.session_key or 'state',
    )
    return render(request, 'users/login.html', {'auth_url': auth_url})


def ms_callback(request):
    code = request.GET.get('code')
    if not code:
        return render(request, 'users/login.html', {'error': 'Authentication failed. No code returned.'})

    result = get_msal_app().acquire_token_by_authorization_code(
        code,
        scopes=settings.AZURE_SCOPE,
        redirect_uri=settings.AZURE_REDIRECT_URI,
    )

    if 'error' in result:
        return render(request, 'users/login.html', {'error': result.get('error_description', 'Authentication failed.')})

    id_token_claims = result.get('id_token_claims', {})
    email = id_token_claims.get('preferred_username') or id_token_claims.get('email', '')
    name = id_token_claims.get('name', email)

    if not email:
        return render(request, 'users/login.html', {'error': 'Could not retrieve email from Microsoft account.'})

    # Only allow users whose email exists in Microsoft Entra ID (already validated by token)
    # Get or create Django user mapped to the Entra ID account
    user, _ = User.objects.get_or_create(username=email, defaults={'email': email, 'first_name': name})
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    request.session['user'] = {'name': name, 'email': email}
    return redirect('user-list-template')


def ms_logout(request):
    logout(request)
    request.session.flush()
    ms_logout_url = (
        f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}/oauth2/v2.0/logout"
        f"?post_logout_redirect_uri={settings.LOGOUT_REDIRECT_URL}"
    )
    return redirect(ms_logout_url)
