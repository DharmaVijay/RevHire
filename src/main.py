from fastapi import FastAPI, HTTPException
from user_dao import UserDAO
import logging
import jwt
from user_service import UserService
from jobposts_service import JobPostsService
from dto.user_request import UserRequest
from dto.user_response import UserResponse
from dto.login_credentials import Login
from dto.create_jobrequest import JobPosts
# from dto.job_response import JobPosts 

logging.basicConfig(filename="user_controller.log", encoding='utf-8', filemode='a', level=logging.INFO)

logger=logging.getLogger(__name__)

app = FastAPI()


user_service = UserService()
@app.get("/users")
def get_users(user_jwt:str):
    try:
        user_info = jwt.decode(user_jwt, "secret", algorithms=["HS256"])
        print(user_info)
        id=0
        logger.info("User data retreived")
        return 0
    
    except Exception as e:
        logger.error(e)
        print("Error")

@app.post("/signup")
def create_user(user_request:UserRequest):
    try:
        user_service.create_user(user_request)
        logger.info("User Created")
        return "user created"
    except Exception as e:
        logger.error("failed to create user")
        raise HTTPException(status_code=500, detail="failed to create user")

@app.post("/login")
def login(login:Login):
    try:
        return jwt.encode({"email": login.email}, "secret", algorithm="HS256") # payload,key,alg
    except Exception as e:
        logger.error("failed to login")
        return HTTPException(status_code=404, detailed="failed to login")
    
@app.post("/createjobpost")
def createjobpost(create_jobrequest:JobPosts):
    try:
        logger.info(f"job details {create_jobrequest}")
        jobpost = JobPostsService()
        jobpost.create_jobpost(create_jobrequest)
        logger.info("Job post Created")
        return "job post created"
    except Exception as e:
        logger.error("failed to create job post")
        return HTTPException(status_code=404, detailed="failed to create job post")
    
@app.get('/allposts')
def fetchalljobposts():
    try:
        jobpost = JobPostsService()
        return jobpost.fetchall_jobposts()
    except Exception as e:
        logger.error("")

@app.get('/allposts/{user_id}')
def fetchalljobposts_employer(user_id : int):
    try:
        jobpost = JobPostsService()
        return jobpost.fetchall_jobposts_employer(user_id)
    except Exception as e:
        logger.error("")













