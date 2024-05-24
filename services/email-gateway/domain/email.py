from framework.serialization import Serializable


class Request:
    def validate(self):
        pass

    def to_dict(self):
        return self.__dict__


class EmailRecipient:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class EmailRequest:
    def __init__(self, recipient: EmailRecipient, subject: str, content: str):
        self.recipient = recipient
        self.subject = subject
        self.content = content

    def get_request(self):
        return {
            'to': [
                {
                    'email': self.recipient.email,
                    'name': self.recipient.name
                }
            ],
            'sender': {
                'id': 2
            },
            'htmlContent': self.content,
            'subject': self.subject
        }


class SendEmailRequest(Request):
    def __init__(self, data):
        self.recipient = data.get('recipient')
        self.subject = data.get('subject')
        self.body = data.get('body')
        self.title = data.get('title')

    def validate(self):
        for value in [self.recipient,
                      self.subject,
                      self.body]:

            if value is None:
                return False
        return True


class SendDataTableEmailRequest(Request):
    def __init__(self, data):
        self.recipient = data.get('recipient')
        self.subject = data.get('subject')
        self.table = data.get('table')
        self.style = data.get('style')

    def validate(self):
        for value in [self.recipient,
                      self.subject]:

            if value is None:
                return False
        return True


class SendDataJsonEmailRequest(Request):
    def __init__(self, data):
        self.recipient = data.get('recipient')
        self.subject = data.get('subject')
        self.json = data.get('json')
        self.style = data.get('style')

    def validate(self):
        for value in [self.recipient,
                      self.subject,
                      self.json]:

            if value is None:
                return False
        return True


class SendEmailResponse(Serializable):
    def __init__(
        self,
        response: dict,
        content: dict
    ):
        self.response = response
        self.content = content


class GetStyleOptionsResponse(Serializable):
    def __init__(
        self,
        table_styles: list,
        json_styles: list
    ):
        self.table_styles = table_styles
        self.json_styles = json_styles
