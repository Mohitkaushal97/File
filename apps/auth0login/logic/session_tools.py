#!/usr/bin/python3


class SessionTools:
    @staticmethod
    def extract_user_info(request):
        # request = self.request
        user = request.user
        auth0_uid, auth0_first_name, auth0_last_name, auth0user_email = None, None, None, None
        if user.is_authenticated:
            auth0user = user.social_auth.get(provider='auth0')
            auth0_uid = auth0user.uid
            # auth0_first_name = auth0user.user.first_name
            auth0_first_name = user.first_name
            auth0_last_name = user.last_name
            auth0user_email = user.email

        return auth0_uid, auth0_first_name, auth0_last_name, auth0user_email

