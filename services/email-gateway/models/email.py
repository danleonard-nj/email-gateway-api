from framework.utilities.pinq import any


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
        return not any([
            self.recipient,
            self.subject,
            self.body], lambda x: x is None
        )


class SendDataTableEmailRequest(Request):
    def __init__(self, data):
        self.recipient = data.get('recipient')
        self.subject = data.get('subject')
        self.table = data.get('table')
        self.style = data.get('style')

    def validate(self):
        return not any([
            self.recipient,
            self.subject
        ], lambda x: x is None)


class SendDataJsonEmailRequest(Request):
    def __init__(self, data):
        self.recipient = data.get('recipient')
        self.subject = data.get('subject')
        self.json = data.get('json')
        self.style = data.get('style')

    def validate(self):
        return not any([
            self.recipient,
            self.subject,
            self.json
        ], lambda x: x is None)
