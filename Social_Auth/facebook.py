import facebook


class Facebook:
    @staticmethod
    def validate(auth_token):
        try:
            token = facebook.GraphAPI(auth_token)
            user_info = token.request('/me?fields=name,email')
            return user_info
        except Exception:
            return 'Token Invalid or Expired'
