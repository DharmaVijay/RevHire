from jobposts_dao import JobPostsDAO
from dto.create_jobrequest import JobPosts
import logging
logging.basicConfig(filename="job_posts.log", encoding='utf-8', filemode='a', level=logging.INFO)
logger_jobpostservice = logging.getLogger(__name__)
class JobPostsService:
    def create_jobpost(self, jobpost: JobPosts):
        try:
            jobpost_dao = JobPostsDAO()
            return jobpost_dao.create_jobpost(jobpost)
        except Exception as e:
            logger_jobpostservice.error(f"Unable to create jobpost {e}",e)
            raise Exception("Unable to create jobpost")
        
    def fetchall_jobposts(self):
        try:
            jobpost_dao = JobPostsDAO()
            return jobpost_dao.fetchall_jobposts()
        except Exception as e:
            logger_jobpostservice.error(f"Unable to fetch all jobposts {e}",e)
            raise Exception("Unable to fetch all jobposts")
        
    def fetchall_jobposts_employer(self, jobseeker_id):
        try:
            jobpost_dao = JobPostsDAO()
            return jobpost_dao.fetchall_jobposts_employer(jobseeker_id)
        except Exception as e:
            logger_jobpostservice.error(f"Unable to fetch all jobposts of employer {e}",e)
            raise Exception("Unable to fetch all jobposts of employer")
    