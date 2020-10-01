#!/usr/bin/python3
from .chargebee.crb_utils import ChargebeeManager
from .auth0_logic.auth_logic import Auth0Manager

import logging
logger = logging.getLogger('payments')

class AuthPaymentsManager:
    def __init__(self):
        pass

    @staticmethod
    def get_or_create_crb_user(auth0_uid, auth0user_email, create_if_dont_exist=True):
        logger.info(f"get_or_create_crb_user:: getting crb_user_id for auth0_uid [{auth0_uid}]")
        crb_userid, crb_site = Auth0Manager().get_metadata_crb_userid(auth0_uid)
        logger.info(f"retrieved crb_userid [{crb_userid}] crb_site[{crb_site}]")

        if crb_userid is None and create_if_dont_exist:
            crb_customer = ChargebeeManager().create_customer_v3(email=auth0user_email, auth0_uid=auth0_uid)
            logger.info("created customer: [%s]" % (str(crb_customer)))
            crb_userid = crb_customer.id
            crb_site = ChargebeeManager().get_site()
            Auth0Manager().update_metadata(auth0_user_id=auth0_uid, crb_userid=crb_userid, crb_site=crb_site)
            logger.warning(f"updated auth0_uid [{auth0_uid}] with crb_userid [{crb_userid}]")

        return crb_userid, crb_site
