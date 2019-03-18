import imaplib
import email
import email.header
import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

from mail_box import utils
from mail_box.forms import ComposeForm


@login_required
def index(request):
    # print('username la {} \npassword la {}'.format(request.session['username'],
    #                                                request.session['password']))
    all_messages_seen = utils.get_mailbox(imap_server=request.session['host'],
                                          username=request.session['username'],
                                          password=request.session['password'],
                                          email_folder='INBOX', flag='SEEN')
    all_messages_unseen = utils.get_mailbox(imap_server=request.session['host'],
                                            username=request.session[
                                                'username'],
                                            password=request.session[
                                                'password'],
                                            email_folder='INBOX', flag='UNSEEN')
    all_messages = all_messages_seen + all_messages_unseen
    all_messages = sorted(all_messages, key=lambda k: k.get('time', 0),
                          reverse=True)
    context = {'messages': all_messages,
               'total_messages': len(all_messages)}
    return render(request, 'mail_box/index.html', context)


@login_required
def sent(request):
    # print('username la {} \npassword la {}'.format(request.session['username'],
    #                                                request.session['password']))
    all_messages = utils.get_mailbox(imap_server=request.session['host'],
                                     username=request.session['username'],
                                     password=request.session['password'],
                                     email_folder='Sent', flag='ALL')
    all_messages = sorted(all_messages, key=lambda k: k.get('time', 0),
                          reverse=True)
    context = {'messages': all_messages,
               'total_messages_sent': len(all_messages)}
    return render(request, 'mail_box/sent.html', context)


@login_required
def drafts(request):
    all_messages = utils.get_mailbox(imap_server=request.session['host'],
                                     username=request.session['username'],
                                     password=request.session['password'],
                                     email_folder='Drafts', flag='ALL')
    all_messages = sorted(all_messages, key=lambda k: k.get('time', 0),
                          reverse=True)
    context = {'messages': all_messages,
               'total_messages_draft': len(all_messages)}
    return render(request, 'mail_box/drafts.html', context)


@login_required
def junk(request):
    all_messages = utils.get_mailbox(imap_server=request.session['host'],
                                     username=request.session['username'],
                                     password=request.session['password'],
                                     email_folder='Junk', flag='ALL')
    all_messages = sorted(all_messages, key=lambda k: k.get('time', 0),
                          reverse=True)
    context = {'messages': all_messages,
               'total_messages_junk': len(all_messages)}
    return render(request, 'mail_box/junk.html', context)


@login_required
def trash(request):
    all_messages = utils.get_mailbox(imap_server=request.session['host'],
                                     username=request.session['username'],
                                     password=request.session['password'],
                                     email_folder='Trash', flag='ALL')
    context = {'messages': all_messages,
               'total_messages_trash': len(all_messages)}
    return render(request, 'mail_box/trash.html', context)


@login_required
def read_mail(request, uuid):
    print(uuid)
    M = imaplib.IMAP4_SSL(host=request.session['host'], port=993)
    M.login(request.session['username'],
            request.session['password'])
    M.select('INBOX')
    rv, data = M.fetch(uuid, '(RFC822)')
    mess_info = {}
    if rv != 'OK':
        print("ERROR getting message", uuid)
        return
    msg = email.message_from_bytes(data[0][1])
    print("day la msg", msg)
    if msg['Subject']:
        hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        subject = str(hdr)
    else:
        subject = None
    mess_info['id'] = uuid
    mess_info['subject'] = subject
    # print('Message %s: %s' % (num, subject))
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            body = part.get_payload(decode=True)
            # print(body.decode('utf-8').strip())
            mess_info['body'] = body.decode('utf-8').strip()
    mess_info['raw_date'] = msg['Date']
    # print('Raw Date:', msg['Date'])
    # Now convert to local date-time
    date_tuple = email.utils.parsedate_tz(msg['Date'])
    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(
            email.utils.mktime_tz(date_tuple))
        mess_info['time'] = local_date
        mess_info['local_date'] = local_date.strftime("%a, %d %b %Y %H:%M:%S")
    if msg['from']:
        user_from = email.header.decode_header(msg['from'])
        if user_from[0][1] == 'utf-8':
            mess_info['from'] = user_from[0][0].decode('utf8')
        elif user_from[0][1] == None:
            mess_info['from'] = user_from[0][0]
    else:
        mess_info['from'] = None
    if msg['to']:
        user_to = email.header.decode_header(msg['to'])
        if user_to[0][1] == 'utf-8':
            mess_info['to'] = user_to[0][0].decode('utf8')
        elif user_to[0][1] == None:
            mess_info['to'] = user_to[0][0]
    else:
        mess_info['to'] = None
    print('------------ \n',mess_info)
    return render(request, 'mail_box/read_mail.html', {'message' : mess_info})


@login_required
def compose(request):
    return render(request, 'mail_box/compose.html')


@login_required
def send_mail_test(request):
    print(request.method)
    if request.method == "POST":
        form = ComposeForm(request.POST, request.FILES)
        if form.is_valid():
            print('minhkma')
            email_to = form.cleaned_data['to']
            email_subject = form.cleaned_data['subject']
            email_body = form.cleaned_data['body']
            document = request.FILES.getlist('document')
            print(email_to, email_subject, email_body, document)
    return HttpResponseRedirect(reverse('index'))