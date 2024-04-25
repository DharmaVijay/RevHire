
from user_dao import UserDAO
from dto.user_request import UserRequest
from dto.login_credentials import Login
import logging
logging.basicConfig(filename="users.log", encoding='utf-8', filemode='a', level=logging.INFO)
user_logger = logging.getLogger(__name__)
class UserService:
    def create_user(self, user_request:UserRequest):
        try:
            user_dao = UserDAO()
            return user_dao.create_user(user_request)
        except Exception as e:
            user_logger.error(f"Unable to create user in UserService {e}",e)
            raise Exception("Unable to create user")
        
    def check_user(self, login: Login):
        try:
            user_dao = UserDAO()
            print(f"&&&&&&&&&&&&&&& {user_dao.check_user(login)}, {type(
                
            )}")
            return user_dao.check_user(login)
        except Exception as e:
            user_logger.error(f"User credentials not found {e}")
            raise Exception(" Unable to find user")
            
