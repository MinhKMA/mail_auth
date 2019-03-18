import sys
import imaplib
import email
import email.header
import datetime
from django.http import Http404

# def get_info_mess():
#     mess_info = {}
#     mess_info['uuid'] = num.decode('utf8')
#     rv, data = M.fetch(num, '(RFC822)')
#     if rv != 'OK':
#         print("ERROR getting message", num)
#         return
#     msg = email.message_from_bytes(data[0][1])
#     # print(msg.get('Message-ID'))
#     if msg['Subject']:
#         hdr = email.header.make_header(
#             email.header.decode_header(msg['Subject']))
#         subject = str(hdr)
#     else:
#         subject = None
#     mess_info['id'] = num
#     mess_info['subject'] = subject
#     # print('Message %s: %s' % (num, subject))
#     for part in msg.walk():
#         if part.get_content_type() == "text/plain":
#             body = part.get_payload(decode=True)
#             # print(body.decode('utf-8').strip())
#             mess_info['body'] = body.decode('utf-8').strip()
#     mess_info['raw_date'] = msg['Date']
#     # print('Raw Date:', msg['Date'])
#     # Now convert to local date-time
#     date_tuple = email.utils.parsedate_tz(msg['Date'])
#     if date_tuple:
#         local_date = datetime.datetime.fromtimestamp(
#             email.utils.mktime_tz(date_tuple))
#         mess_info['time'] = local_date
#         mess_info['local_date'] = local_date.strftime("%a, %d %b %Y %H:%M:%S")
#     if msg['from']:
#         user_from = email.header.decode_header(msg['from'])
#         if user_from[0][1] == 'utf-8':
#             mess_info['from'] = user_from[0][0].decode('utf8')
#         elif user_from[0][1] == None:
#             mess_info['from'] = user_from[0][0]
#     else:
#         mess_info['from'] = None
#     if msg['to']:
#         user_to = email.header.decode_header(msg['to'])
#         if user_to[0][1] == 'utf-8':
#             mess_info['to'] = user_to[0][0].decode('utf8')
#         elif user_to[0][1] == None:
#             mess_info['to'] = user_to[0][0]
#     else:
#         mess_info['to'] = None
#     if flag == 'UNSEEN':
#         mess_info['seen'] = 0
#         M.store(num, '-FLAGS', '\\Seen')
#     else:
#         mess_info['seen'] = 1
#     all_messages.append(mess_info)



def process_mailbox(M, flag):
    """
    Do something with emails messages in the folder.
    For the sake of this example, print some headers.
    """

    # rv, data = M.search(None, "UNSEEN")
    rv, data = M.search(None, flag)
    # print('data nhoc:', data)
    if rv != 'OK':
        print("No messages found!")
        return
    all_messages = []
    for num in data[0].split():
        mess_info = {}
        mess_info['uuid'] = num.decode('utf8')
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return
        msg = email.message_from_bytes(data[0][1])
        # print(msg.get('Message-ID'))
        if msg['Subject']:
            hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
            subject = str(hdr)
        else:
            subject = None
        mess_info['id'] = num
        mess_info['subject'] = subject
        # print('Message %s: %s' % (num, subject))
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
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
        if flag == 'UNSEEN':
            mess_info['seen'] = 0
            M.store(num, '-FLAGS','\\Seen')
        else:
            mess_info['seen'] = 1
        all_messages.append(mess_info)
    return all_messages


def get_mailbox(imap_server, username, password, email_folder, flag):
    M = imaplib.IMAP4_SSL(host=imap_server, port=993)

    try:
        rv, data = M.login(username, password)
    except imaplib.IMAP4.error:
        print ("LOGIN FAILED!!! ")
        sys.exit(1)

    rv, data = M.select(email_folder)
    if rv == 'OK':
        print("Processing mailbox...\n")
        all_messages = process_mailbox(M, flag)
        M.close()
        return all_messages
    else:
        print("ERROR: Unable to open mailbox ", rv)
