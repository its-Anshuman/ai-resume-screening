from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
from config import HF_TOKEN
from transformers import logging as transformers_logging

# Set Hugging Face token for faster downloads
if HF_TOKEN and HF_TOKEN != "your_huggingface_token_here":
    os.environ["HF_TOKEN"] = HF_TOKEN

# Silence the non-actionable “UNEXPECTED” weights warning from Transformers
transformers_logging.set_verbosity_error()

model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_similarity(jd, resume):
    jd_emb = model.encode([jd])
    res_emb = model.encode([resume])

    return cosine_similarity(jd_emb, res_emb)[0][0]


def final_score(llm_score, similarity):
    return 0.7 * llm_score + 0.3 * (similarity * 10)