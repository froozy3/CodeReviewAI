import cohere
from models.models import *
from services.github_service import *
from utilits.parsing import *

CO_API_KEY = os.getenv('CO_API_KEY')

co = cohere.AsyncClientV2(CO_API_KEY)


async def analyze_code(review_request: ReviewRequest):
    code = await get_repo_code_files(review_request.github_repo_url)
    prompt = f"""
    Imagine you are an IT professional and your task is to review the code as honestly as possible.

    Additional Description:
    
    {review_request.description}
    
    Code Repository:
    Review the code found in the repository at {code}. Record your observations in the blocks listed below.
    
    1. **Files Found:**
    - [List the files here]
    
    2. **Downsides and Improvements:**
    - [List the concerns here]
    
    3. **Rating:**
    - Give an overall rating of the candidate's level {review_request.candidate_level} from 1 to 5. (only a number from 1 to 5(just integer))
    
    4. **Conclusion:**
    - Include a final conclusion summarizing your findings based on the analysis. """

    response = await co.chat(
        model='command-r-plus-08-2024',
        messages=[{"role": "user", "content": f"{prompt}"}])
    analysis_result = response.message.content[0].text

    found_files = []
    downsides = parse_text(analysis_result, "2. **Downsides and Improvements:**", "3. **Rating:**")
    rating = parse_text(analysis_result, "3. **Rating:**", "4. **Conclusion:**")
    conclusion = parse_text(analysis_result, "**Conclusion:**")
    # parsing list files
    for files in code:
        for k in files.keys():
            found_files.append(k)
    # print(analysis_result)
    return ReviewResponse(found_files=found_files, downsides=downsides, rating=rating, conclusion=conclusion,
                          candidate_level=review_request.candidate_level,
                          github_repo_url=review_request.github_repo_url)
