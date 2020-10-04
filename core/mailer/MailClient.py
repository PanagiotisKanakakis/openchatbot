import json
import smtplib
import ssl


class MailClient:

    def __init__(self, config):
        self.port = config.get('mail-service', 'port')
        self.smtp_server = config.get('mail-service', 'smtp_server')
        self.password = config.get('mail-service', 'password')
        self.sender_account = config.get('mail-service', 'sender_account')
        self.schoolAccounts = json.loads(config.get("mail-service", "school_account"))
        self.selfieExperts = json.loads(config.get("mail-service", "selfie_experts"))
        self.context = ssl.create_default_context()

    def sendMails(self):
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=self.context) as server:
            server.login(self.sender_account, self.password)
            for schoolAccount in self.schoolAccounts:
                message = """\
                    Subject: Hi there

                    This message is sent from Python."""
                server.sendmail(self.sender_account, schoolAccount, message)
            for selfieExpert in self.selfieExperts:
                message = ""
                server.sendmail(self.sender_account, selfieExpert, message)
