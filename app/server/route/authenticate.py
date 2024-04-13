from typing import Any
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.server.model.login import SignUp
from typing import Annotated
from app.server.service import authenticate
from app.server.model.token import Token

router = APIRouter()

######################################### SIGNUP  ########################


@router.post('/create-account', summary='To allow user to create an account')
async def signUp(data: SignUp = Body(...)) -> dict[str, Any]:
    """signup a user/admin account

    Returns:
        dict[str, Any]: response
    """
    create_account = await authenticate.create_account(data)
    return JSONResponse({'status': status.HTTP_200_OK,
                         'response': 'Your account is created successfully.'})

########################################################## SIGN-IN #######


@router.post('/login',
             summary='To generate token for login',
             response_model=Token)
async def token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """Login to Account

    Returns:
        dict[str, Any]: response
    """
    login_data = await authenticate.token(form_data)
    return login_data
