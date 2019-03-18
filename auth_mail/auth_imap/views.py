"""Authentication views to use with the IMAP auth backend
"""

# Global imports:
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse

# Local imports:
from django.shortcuts import render
from auth_imap.forms import LoginForm
from utils.config import server_config, WebpymailConfig
from utils.config import server_list

@csrf_protect
@never_cache
def loginView(request):
    """Login the user on the system
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            next = form.cleaned_data['next']
            try:
                server = form.cleaned_data['host']
                config = server_config()
                host = config.get(server, 'host')
                port = config.getint(server, 'port')
                ssl = config.getboolean(server, 'ssl')
            except:
                return render(request, 'auth_imap/login.html',
                              {'form': form,
                               # 'imap_server_list': imap_server_list,
                               'error_message': _('Invalid server. '
                                                  'Please try again.')})
            try:
                # print(username, password, host, port, ssl)
                user = authenticate(request=request,
                                    username=username[:30],
                                    password=password, host=host,
                                    port=port, ssl=ssl)
                # print(user)
            except ValueError:
                return render(request, 'auth_imap/login.html',
                              {'form': form,
                               # 'imap_server_list': imap_server_list,
                               'error_message': _('Invalid login. '
                                                  'Please try again.')})
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    print('xac thuc thanh cong')
                    # Not an imap user:
                    if (request.session['_auth_user_backend'] ==
                            'django.contrib.auth.backends.ModelBackend'):
                        return render(request, 'auth_imap/login.html',
                                      {'form': form,
                                       # 'imap_server_list': imap_server_list,
                                       'error_message': _('This is not an IMAP'
                                                          ' valid account. '
                                                          'Please try '
                                                          'again.')})

                    request.session['username'] = username
                    request.session['password'] = password
                    request.session['host'] = host
                    request.session['port'] = port
                    request.session['ssl'] = ssl

                    return HttpResponseRedirect(reverse('index'))
                # Disabled account:
                else:
                    return render(request, 'auth_imap/login.html',
                                  {'form': form,
                                   # 'imap_server_list' : imap_server_list,
                                   'error_message': _('Sorry, disabled '
                                                      'account.')})
            # Invalid user:
            else:
                return render(request, 'auth_imap/login.html',
                              {'form': form,
                               # 'imap_server_list': imap_server_list,
                               'error_message': _('Invalid login. Please '
                                                  'try again.')})
        # Invalid form:
        else:
            return render(request, 'auth_imap/login.html',
                          {'form': form,
                           # 'imap_server_list': imap_server_list
                           })
    # Display the empty form:
    else:
        data = {'next': request.GET.get('next', '')}
        form = LoginForm(data)
        return render(request, 'auth_imap/login.html', {'form': form,
                                                        # 'imap_server_list': imap_server_list,
                                                        })


def logoutView(request):
    # Get the user config
    try:
        config = WebpymailConfig(request)
        logout_page = config.get('general', 'logout_page')
    except KeyError:
        logout_page = '/'
    # Do the actual logout
    request.session.modified = True
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect(logout_page)

