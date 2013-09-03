#    coding: UTF-8
#    User: haku
#    Date: 13-6-12
#    Time: 下午4:32
#    使用imaplib再度包装的易于提取文本的连接器

import imaplib
from __xmessage import XMessage

class XEmail:
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.M.close()
        self.M.logout()

    def login(self, host, use_ssl=False, port=143, username='', password=''):
        if use_ssl:
            self.M = imaplib.IMAP4_SSL(host, port)

            self.M.debug = 1
        else:
            self.M = imaplib.IMAP4(host, port)
        typ, dat = self.M.login(username, password)
        pass

    def getMailbox(self, mailbox):
        code, data = self.M.list()
        if code == 'OK':
            for box in data:
                if mailbox in box:
                    box = box.split()
                    return box[-1]
        return 'INBOX'

    def getCountUnseen(self):
        return self.M.status('INBOX', '(UNSEEN)')[1][0].split()[-1][:-1]

    def getHeader(self, mail_id, mailbox='Inbox'):
        self.M.select(self.getMailbox(mailbox))
        data = XMessage(self.M.fetch(mail_id, '(BODY[HEADER.FIELDS (SUBJECT FROM DATE)])')[1][0][1])
        return data

    def searchBox(self, mailbox='Inbox', filters='ALL'):
        # print self.getMailbox(mailbox)
        self.M.select(self.getMailbox(mailbox))
        # self.M.select(mailbox)
        # print self.M.status('INBOX', '(MESSAGES UNSEEN)')
        typ, data = self.M.search(None, filters)
        ids = (data[0].split())
        return ids

    def getMessage(self, mail_id):
        typ, data = self.M.fetch(mail_id, '(RFC822)')
        # print data[0][1]
        return XMessage(data[0][1])

    def delMessage(self, mail_id):
        self.M.copy(unicode(mail_id), self.getMailbox('Trash'))
        self.M.store(mail_id, '+FLAGS', '\\Deleted')
