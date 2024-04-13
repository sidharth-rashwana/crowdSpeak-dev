from app.server.database.collections import Collections
import app.server.database.core_data as model_service
from app.server.utils.date_utils import get_current_timestamp
from app.server.utils.email import email_sending
from app.server.utils.otp import generate_otp
from app.server.utils import token as token_utils
from app.server.utils.password import get_password_hash
from app.server.logger.custom_logger import logger
from app.server.model.token import Token
from app.server.utils.token import authenticate_user
# to find parent 'app' folder Path
import os

SECRET_KEY = os.environ.get('SECRET_KEY', os.getenv("JWT_SECRET_KEY"))
ALGORITHM = os.environ.get('JWT_ALGORITHM', os.getenv("JWT_ALGORITHM"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.environ.get(
        'JWT_ACCESS_TOKEN_EXPIRE_MINUTES',
        os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")))


async def create_account(data):
    try:
        is_username = await model_service.read_one(Collections.ACCOUNTS, {'username': data.username, 'isVerified': True})
        logger.debug('if username does not exist then only create account')
        if is_username['status'] == 404:
            logger.debug('Generating OTP')
            otp = generate_otp()
            logger.debug('Generating OTP complete')
            logger.debug('Sending OTP onto email')
            response = email_sending(data.email, otp)
            logger.debug('Sending OTP onto email is complete')
            if response['status'] == 200:
                logger.debug(
                    'Checking if account already exist with given email')
                already_exist = await model_service.read_one(Collections.ACCOUNTS, {'email': data.email})
                logger.debug('Checking if account already exist is complete')
                data = dict(data)
                data['hashed_password'] = get_password_hash(
                    otp)  # encrypt the password in request body
                data['isVerified'] = False
                data['isDisabled'] = False
                print(already_exist)
                # account is not created before
                if already_exist['status'] == 404:
                    logger.debug('Creating a new account')
                    inserted_document = await model_service.create_one(Collections.ACCOUNTS, data)
                    logger.debug('Creating a new account is complete')
                    return inserted_document
                # account is there but not verified
                elif already_exist['status'] == 200 and already_exist['isVerified'] == False:
                    logger.debug(
                        'Deleting account as it exists but not verified')
                    deleted_user = await model_service.delete_one(Collections.ACCOUNTS, {'email': data['email']})
                    print(deleted_user)
                    logger.debug('Deleting account is complete')
                    # if user is successfully deleted then only allow to create
                    # new user with same email
                    if deleted_user['acknowledge']:
                        logger.debug(
                            'Creating a new account after deleting non-verified account')
                        account_insert = await model_service.create_one(Collections.ACCOUNTS, data)
                        logger.debug('Creating a new account is complete')
                        return account_insert
                else:
                    raise Exception('User already has an account.')
            else:
                raise Exception('Not able to deliver the email.')
        else:
            raise Exception(
                'Username already exists , please provide another username for account creation.')
    except Exception as e:
        return {'message': str(e)}


async def token(form_data) -> Token:
    try:
        logger.debug('Getting details about entered email.')
        user = await authenticate_user(form_data.username, form_data.password)

        logger.debug('Checking if account is verified')
        if not user.isVerified:
            # change to update by '_id' in future
            update_account = await model_service.update_one(Collections.ACCOUNTS, {'email': user.email}, {"$set":
                                                                                                          {'isVerified': True,
                                                                                                           'createdAt': get_current_timestamp(),
                                                                                                           'isDeleted': False}})
            logger.debug('Verification of the account is complete')
        access_token_expires = await token_utils.create_login_access_token(user)
        return access_token_expires
    except Exception as e:
        return Token(access_token='', token_type='')
