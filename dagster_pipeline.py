from pdf_parser import parse_all_resumes
from dagster import job, op
from ranker import rank_resumes

@op
def get_job_description():
    with open("/Users/pavitrakamleshkumarmodi/Documents/resume-ranking-engine/job_description_folder/job_description.txt", "r") as f:
        return f.read()

@op
def parse(folder: str):
    return parse_all_resumes(folder)

@op
def rank(resumes, job_description):
    return rank_resumes(resumes, job_description)

@job
def resume_pipeline():
    folder = "/Users/pavitrakamleshkumarmodi/Documents/resume-ranking-engine/resumes/"
    rank(parse(folder), get_job_description())