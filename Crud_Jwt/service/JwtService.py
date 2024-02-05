from datetime import datetime,timedelta
from typing import Optional
from jose import jwt
import os
class JwtService():
    __secret_key = os.getenv('SECRET_KEY')
    __jwt_algorithm= os.getenv('ALGORITHM')
    
    @classmethod
    def generate_token(cls,data:dict , exp_time:Optional[timedelta]=None):
        to_encode = data.copy()
        if exp_time:
            expire = datetime.now()+exp_time
        else:
            expire = datetime.now()+timedelta(minutes=15)
        to_encode.update({'exp':expire})
        
        
        encoded_jwt = jwt.encode(to_encode,cls.__secret_key,algorithm=cls.__jwt_algorithm)
        
        return encoded_jwt
    
    @classmethod
    def decode_token(cls,jwt_token : str):
        try:
            decoded_token = jwt.decode(jwt_token,cls.__secret_key,cls.__jwt_algorithm)
            return decoded_token if decoded_token.get('exp')>= datetime.time() else None
        except:
            return {}