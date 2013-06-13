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
        else:
            self.M = imaplib.IMAP4(host, port)
        self.M.login(username, password)
        pass

    def searchBox(self, mailbox='INBOX', filters='ALL'):
        self.M.select(mailbox)
        typ, data = self.M.search(None, filters)
        ids = (data[0].split())
        return ids;

    def getMessage(self, mail_id):
        typ, data = self.M.fetch(mail_id, '(RFC822)')
        return XMessage(data[0][1])

