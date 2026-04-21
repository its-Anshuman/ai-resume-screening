import pandas as pd
from src.ingestion import fetch_candidates
from src.parser import extract_text_from_pdf
from src.llm_evaluator import evaluate_resume
from src.scoring import compute_similarity, final_score
from download_resume import download_resume
from config import OUTPUT_FILE

def run_pipeline(jd):

    df = fetch_candidates()
    results = []

    for _, row in df.iterrows():
        name = row['Name']
        drive_link = row['Resume Upload']
        
        # Download the resume first
        try:
            resume_path = download_resume(drive_link, name)
        except Exception as e:
            print(f"Failed to download resume for {name}: {e}")
            continue
        
        text = extract_text_from_pdf(resume_path)

        llm_result = evaluate_resume(jd, text)

        similarity = compute_similarity(jd, text)
        score = final_score(llm_result["score"], similarity)

        results.append({
            "Name": name,
            "Score": round(score, 2),
            "Category": llm_result["category"],
            "Strengths": llm_result["strengths"],
            "Weaknesses": llm_result["weaknesses"],
            "Reasoning": llm_result["reasoning"]
        })

    result_df = pd.DataFrame(results)
    result_df = result_df.sort_values(by="Score", ascending=False)

    result_df.to_csv(OUTPUT_FILE, index=False)

    return result_df