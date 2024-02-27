
from fastapi import HTTPException, Request
import jwt


def get_current_user(request: Request) -> dict:
  token = request.cookies.get("_pychat")  
  try:
    parsed_token = jwt.decode(token, 'secret', algorithms=['HS256'])
    print(f'parsed_token: {parsed_token}')
    return parsed_token
  except:
    print(f'unauthorized')
    raise HTTPException(status_code=401, detail="User is not authenticated")