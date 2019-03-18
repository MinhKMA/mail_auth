# Imports
from configparser import SafeConfigParser
import os.path
import re

from django.conf import settings

# WebpymailConfig class

USERCONFDIR = getattr(settings, 'USERCONFDIR')
SERVERCONFDIR = getattr(settings, 'SERVERCONFDIR')
FACTORYCONF = getattr(settings, 'FACTORYCONF')
DEFAULTCONF = getattr(settings, 'DEFAULTCONF')
SYSTEMCONF = getattr(settings, 'SYSTEMCONF')


class WebpymailConfig(SafeConfigParser):
    '''
    This is the class used to manage all the user configuration available
    in WebPyMail.
    '''

    def __init__(self, request):
        # Note that SafeConfigParser if not a new class so we have to
        # explicitly call the __init__ method
        SafeConfigParser.__init__(self)
        try:
            host = request.session['host']
            username = request.session['username']
            user_conf = os.path.join(USERCONFDIR, '%s@%s.conf' %
                                     (username, host))
            if not os.path.isfile(user_conf):  # Touch the user conf file
                open(user_conf, 'w').close()
            server_conf = os.path.join(SERVERCONFDIR, '%s.conf' % host)
            config_files = [FACTORYCONF,
                            DEFAULTCONF,
                            user_conf,
                            server_conf,
                            SYSTEMCONF]
        except KeyError:
            config_files = [FACTORYCONF,
                            DEFAULTCONF]
        self.read(config_files)

    identity_re = re.compile(r'^identity-(?P<id_number>[0-9]+)$')

    def identities(self):
        '''
        Returns a list of identities defined on the user configuration.
        @return a list of identities in dictionary form.
        '''
        identity_list = []
        for section in self.sections():
            identity_sec = self.identity_re.match(section)
            if identity_sec:
                identity = {}
                identity['id_number'] = int(identity_sec.group('id_number'))
                for option in self.options(section):
                    identity[option] = self.get(section, option)
                identity_list.append(identity)
        identity_list.sort(key=lambda identity: identity['id_number'])
        return identity_list


def server_config():
    '''
    Returns the server(s) configuration.
    '''
    config = SafeConfigParser()
    config.read(settings.SERVERCONF)
    return config


def server_list():
    '''
    Returns a list of server configurations. This is the login server, ie, the
    server against which the users authenticate.
    '''
    config = server_config()
    server_list = []
    k = 0
    for server in config.sections():
        s = {}
        s['label'] = server
        k += 1
        for option in config.options(server):
            s[option] = config.get(server, option)
        server_list.append(s)
    server_list.sort(key=lambda server: server['name'])
    return server_list