#    coding: UTF-8
#    User: haku
#    Date: 13-6-12
#    Time: 下午5:54
#    包装Message的解码工作
import email
import re


class XMessage:
    def __init__(self, msg_str):
        self.msg = email.message_from_string(msg_str)

    def getMsg(self):
        return self.msg

    # 得到主题
    def getSubject(self):
        subject = self.msg.get('Subject', '')
        s = email.Header.decode_header(subject)
        subject = s[0][0]
        if s[0][1]:
            subject = subject.decode(s[0][1])
        return subject

    # 得到发送人email地址
    def getFrom(self):
        frm = self.msg.get('From', '').split()
        res = ''
        for f in frm:
            s = email.header.decode_header(f)
            if s[0][1]:
                p = s[0][0].decode(s[0][1])
                res += ' ' + p
            else:
                res += ' ' + s[0][0]
        return res

    def getDate(self):
        return self.msg.get('Date', '')

    def getContentText(self):
        return self._parseMessagePart(self.msg)

    def _parseMessagePart(self, msg):
        if msg.is_multipart():
            parts = []
            for msg_part in msg.walk():
                if re.compile('text').search(msg_part.get_content_type()):
                    body = msg_part.get_payload(decode=True)
                    if body:
                        charset = msg_part.get_content_charset()
                        body = unicode(body, charset)
                        parts.append(body)
            return parts
        else:
            if re.compile('text').search(msg.get_content_type()):
                charset = msg.get_content_charset()
                if charset:
                    return unicode(msg.get_payload(decode=True), charset)
                else:
                    unicode(msg.get_payload(decode=True))

            return None
