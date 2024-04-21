import sqlite3

from model.user import User
from dto.user_request import UserRequest
from dto.user_response import UserResponse
import logging

logging.basicConfig(filename="users.log", encoding='utf-8', filemode='a', level=logging.INFO)
logger = logging.getLogger(__name__)

class UserDAO:
    con = sqlite3.connect("revhire.db", check_same_thread=False)
    cursor = con.cursor()

    def create_user(self, user_request:UserRequest):
        logging.info(f"user details {user_request}")
        try:
            self.cursor.execute(
                """INSERT INTO USER(name, email, password,role) VALUES(?, ?, ?,?)""",
                (user_request.name, user_request.email, user_request.password,user_request.role ),
            )
            self.con.commit()
            logging.info("User created")
            return "created"
        except Exception as e:
            logging.error(f"Error in creating new user : {e}")
            raise Exception("unable to insert user information")

    
    def get_users(self):
        res = self.cursor.execute(
            """SELECT * from USER"""
        )
        self.con.commit()
        return res.fetchall()
    
    def update_user(self, user_request:UserRequest, id:int):
        self.cursor.execute(
            """UPDATE USER SET name = ?, email = ?, password = ? WHERE id = ?""",(
                user_request.name,user_request.email,user_request.password, id )
        )

        res = self.cursor.execute(
            """SELECT * FROM USER WHERE id = ?""", (id)
        )

        user = res.fetchone()
        self.con.commit()

        user_response = UserResponse(user.id, user.name, user.email, user.role)
        return user_response

    def delete_user(self, id):
        self.cursor.execute("""DELETE FROM USER WHERE id = ?""", (id))
        self.con.commit()
        return "User deleted"

    
