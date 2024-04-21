
from user_dao import UserDAO
from dto.user_request import UserRequest
import logging
logging.basicConfig(filename="users.log", encoding='utf-8', filemode='a', level=logging.INFO)
logger = logging.getLogger(__name__)
class UserService:
    def create_user(self, user_request:UserRequest):
        try:
            user_dao = UserDAO()
            return user_dao.create_user(user_request)
        except Exception as e:
            logger.error(f"Unable to create user in UserService {e}",e)
            raise Exception("Unable to create user")

