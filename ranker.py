import dask.dataframe
import pandas
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def rank_resumes(resumes, job_description):
    job_description_embeddings = model.encode(job_description, convert_to_tensor=True)

    for r in resumes:
        r["embedding"] = model.encode(r["content"], convert_to_tensor=True)
        r["score"] = float(util.cos_sim(job_description_embeddings, r["embedding"]).item())

        df = pandas.DataFrame([{"filename":r["filename"], "resume_to_job_description_match_score": round(r["score"], 3)}])

        dask_df = dask.dataframe(df, npartitions=1)
        dask_df = dask_df.nlargest(5, "score")
        return dask_df.compute().to_dict(orient="records")

