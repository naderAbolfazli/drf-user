import enum

from django.conf import settings
from kavenegar import KavenegarAPI

KAVENEGAR_API_KEY = getattr(settings, "KAVENEGAR_API_KEY", None)
KAVENEGAR_OTP_SENDER_NUMBER = getattr(settings, "KAVENEGAR_OTP_SENDER_NUMBER", None)

FIRST_ENTRY = 0


class KavenegarMessageType(enum.Enum):
    SMS = 'sms'
    CALL = 'call'


class KavenegarTemplates:
    verification_message = "verification-code"
    portfolio_diversion_alert = "portfolio-diversion-alert"
    new_analysis_alert = "new-analysis-alert"


class KaveNegarSms:
    api = KavenegarAPI(KAVENEGAR_API_KEY)

    def send_custom(self, receptor, message):
        params = {
            'sender': KAVENEGAR_OTP_SENDER_NUMBER,  # optional
            'receptor': receptor,  # multiple mobile number, split by comma
            'message': message,
        }
        response = self.api.sms_send(params)
        return response[FIRST_ENTRY]['messageid']

    def send_template(self, receptor: str, template: KavenegarTemplates,
                      kavenegar_message_type: KavenegarMessageType = KavenegarMessageType.SMS,
                      **template_params):
        params = {
            'receptor': receptor,
            'template': template,
            'token': template_params.get('token'),
            'token2': template_params.get('token2'),
            'token3': template_params.get('token3'),
            'type': kavenegar_message_type,  # sms vs call
        }
        response = self.api.verify_lookup(params)
        return response[FIRST_ENTRY]['messageid']

    def send_bulk(self, sender: list, receptor: list, message: list):
        params = {
            'sender': sender,  # array of string as json
            'receptor': receptor,  # array of string as json
            'message': message,  # array of string as json
        }
        return self.api.sms_sendarray(params)
