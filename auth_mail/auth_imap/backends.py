import imaplib

from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


def generatePassword(password_len=40):
    """
    Generates a password password_len characters in lenght.

    @param password_len: lenght of the generated password
    @type password_len: int
    """
    VALID_CHARS = '1234567890qwertyuiopasdfghjklzxcvbnm,.-\'' \
                  '+!"#$%&/()=?QWERTYUIOP*ASDFGHJKL^ZXCVBNM;:_'
    from random import choice
    return ''.join([choice(VALID_CHARS) for i in range(password_len)])


class ImapAuthenBackend(ModelBackend):
    """Authenticate using IMAP
    """

    def authenticate(self, request, username=None, password=None, host=None, port=143,
                     ssl=False):
        try:
            print('da den backend login mail')
            if ssl:
                M = imaplib.IMAP4_SSL(host, port)
            else:
                M = imaplib.IMAP4(host, port)
            M.login(username, password)
            M.logout()
            valid = True
        except:
            valid = False

        if valid:
            print(valid)
            try:
                user = User.objects.get(username=('%s@%s' %
                                                  (username, host))[:30])
            except User.DoesNotExist:
                # Create a new user
                password = generatePassword()
                user = User(username=('%s@%s' % (username, host))[:30],
                            password=password)
                user.is_staff = False
                user.is_superuser = False
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
