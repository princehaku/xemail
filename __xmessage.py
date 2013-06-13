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

    # 得到发送人email地址 TODO
    def getFrom(self):
        subject = self.msg.get('From', '')
        s = email.header.decode_header(subject)
        print self._splitAddrList(s)

    def _splitAddrList(self, s):
        #split an address list into list of tuples of (name,address)
        if not s:
            return []
        outQ = True
        cut = -1
        res = []
        for i in range(len(s)):
            if s[i] == '"':
                outQ = not outQ
        if outQ and s[i] == ',':
            res.append(email.utils.parseaddr(s[cut + 1:i]))
        cut = i
        res.append(email.utils.parseaddr(s[cut + 1:i + 1]))
        return res


    def getContentText(self):
        return self._parseMessagePart(self.msg)


    def _parseMessagePart(self, msg):
        if msg.is_multipart():
            parts = []
            for msg_part in msg.walk():
                if re.compile('text').search(msg_part.get_content_type()):
                    body = msg_part.get_payload(decode=True)
                    if body:
                        parts.append(body)
            return parts
        else:
            if re.compile('text').search(msg.get_content_type()):
                return msg.get_payload(decode=True)
            return None


    def _getMessageCharset(self, msg):
        s = re.compile(r"""charset=['"]?(.*?)['">;\n]""").search(msg.get('Content-Type', ''), 2)
        charset = 'utf8'
        if s:
            charset = s.group(1)
        return charset