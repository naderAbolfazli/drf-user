from sms_api.kavenegar_api import KaveNegarSms, KavenegarTemplates


class SendOtpSMS:
    kavenegar_sms = KaveNegarSms()

    def send_verification_sms(self, code, phnum):
        sent = {'success': False, 'message': None}
        try:
            self.kavenegar_sms.send_template(phnum, KavenegarTemplates.verification_message, token=code)
        except Exception as e:
            sent['message'] = 'Message sending failed!' + str(e.args)
            sent['success'] = False
        else:
            sent['message'] = 'Message sent successfully!'
            sent['success'] = True
        return sent

