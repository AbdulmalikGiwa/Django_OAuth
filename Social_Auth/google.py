from google.oauth2 import id_token
from google.auth.transport.requests import Request

request = Request()


class Google:
    @staticmethod
    def validate(auth_token):
        try:
            validate_id = id_token.verify_oauth2_token(auth_token, request, )
            if 'accounts.google.com' in validate_id['iss']:
                return validate_id
        except:
            return "Token Invalid or Expired"
