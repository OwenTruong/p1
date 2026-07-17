import logging

from fastapi import Request, HTTPException
from requests import request

from src.data.authorization import Authorization
from src.utils.config import get_config

async def decode_and_verify_token(access_token):
  url = get_config().backend_url + '/api/auth/token'
  resp = request('POST', url, cookies={
    "access_token": access_token
  })

  if resp.status_code >= 400:
    raise HTTPException(status_code=resp.status_code, detail=resp.text)

  return resp.json()


async def check_auth_status(request: Request, call_next):
  access_token = request.cookies.get('access_token', None)
  if (access_token):
    access_token = access_token.split(' ')[1]
    try:
      decoded_dict = await decode_and_verify_token(access_token)
      logging.info("Successfully decoded and verified token")
      username = decoded_dict['sub']
      request.state.authorization = Authorization(is_authenticated=True, username=username)
    except HTTPException as exc:
      logging.info(f"Failed to decode and verify token. Reason: {exc.detail}")
      request.state.authorization = Authorization(error_message=exc.detail)
    except Exception as exc:
      logging.info(f"Unexpected error")
      logging.debug(exc)
      request.state.authorization = Authorization(error_message="Internal Server Error")
  else:
    # potentially a security concern with how there is a difference in response latency when access_token is provided?
    logging.info("No access token provided. Skipping authentication...")
    request.state.authorization = Authorization()

  response = await call_next(request)
  return response