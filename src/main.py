from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, Gauge, Summary
from user_dao import UserDAO
import logging
import jwt
from user_service import UserService
from jobposts_service import JobPostsService
from jobstatus_service import JobStatusService
from dto.user_request import UserRequest
from dto.user_response import UserResponse
from dto.login_credentials import Login
from dto.create_jobrequest import JobPosts
from dto.apply_jobrequest import ApplyJobRequest
from dto.change_jobstatus import ChangeJobStatus
from dotenv import load_dotenv
import os


load_dotenv() #searches for .env file and loads env variables

# from dto.job_response import JobPosts 

logging.basicConfig(filename="user_controller.log", encoding='utf-8', filemode='a', level=logging.INFO)

logger=logging.getLogger(__name__)

app = FastAPI()

graphs = {}

graphs["users_counter"] = Counter('users','Counter for signup_request method')
graphs['users_histogram'] = Histogram('/signup','get_users_duration_seconds',buckers={1,2,3,5,6,float('inf')})
@app.get("/users")
def get_users(user_jwt:str):
    try:
        user_info = jwt.decode(user_jwt, os.getenv('secret') , algorithms=["HS256"])
        print("*****************",user_info)
        logger.info("User data retreived")
        return 0
    
    except Exception as e:
        logger.error(e)
        print("Error")

@app.post("/signup")
def create_user(user_request:UserRequest):
    try:
        user_service = UserService()
        user_service.create_user(user_request)
        logger.info("User Created")
        return "user created"
    except Exception as e:
        logger.error("failed to create user")
        raise HTTPException(status_code=500, detail="failed to create user")

@app.post("/login")
def login(login:Login):
    try:
        user_service = UserService()
        user_data = user_service.check_user(login)
        (user_id,name,email,password,role) = user_data
        return jwt.encode({"email": email,"role": role,"user_id":user_id}, os.getenv('secret'), algorithm="HS256") # payload,key,alg
    except Exception as e:
        logger.error("failed to login")
        return HTTPException(status_code=404, detailed="failed to login")
    
@app.post("/createjobpost")
def createjobpost(create_jobrequest:JobPosts, user_jwt: str):
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
        return HTTPException(status_code=500, detailed="unable to fetch job posts")

@app.get('/allposts/{user_id}')
def fetchalljobposts_employer(user_id : int):
    try:
        jobpost = JobPostsService()
        return jobpost.fetchall_jobposts_employer(user_id)
    except Exception as e:
        logger.error("")
        return HTTPException(status_code=500, detailed="unable to fetch jobposts of employer")

@app.post('/applyjob')
def applyjob(apply_jobrequest: ApplyJobRequest):
    try:
        jobstatus_service = JobStatusService()
        jobstatus_service.apply_jobpost(apply_jobrequest)
        logger.info("Applied for job post")
        return "applied for job post"
    except Exception as e:
        logger.error("failed to apply for jobpost")
        return HTTPException(status_code=404, detailed="failed to apply for job post")
    
@app.patch('/changejobstatus')
def changestatus(change_jobstatus: ChangeJobStatus):
    try:
        jobstatus_service = JobStatusService()
        jobstatus_service.change_jobstatus(change_jobstatus)
        logger.info("Job status updated")
        return "job status updated"
    except Exception as e:
        logger.error("failed in updating job status")
        return HTTPException(status_code=404, detailed="failed to update job status")

        














