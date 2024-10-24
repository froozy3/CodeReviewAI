import cohere, httpx, logging
from models import ReviewResponse, ReviewRequest

GITHUB_TOKEN = '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'
COHERE_API_KEY = 'AZN0mxbYzr80h7vuY9mmKJZYjmLoHItR2ejlDznd'

co = cohere.AsyncClientV2(COHERE_API_KEY)


# returns content repository
async def get_directory_contents(repo_url: str):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
    }
    try:
        owner, repo = repo_url.split('/')[-2], repo_url.split('/')[-1]
    except ValueError:
        raise ValueError('Invalid GitHub repository URL format.')

    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    async with httpx.AsyncClient() as client:
        logging.info("Fetching repository content from GitHub.")
        response = await client.get(api_url, headers=headers)
        response.raise_for_status()

        return response.json()


# returns content code from directory
async def get_code_from_directory(repo_url: str):
    directory_contents = await get_directory_contents(repo_url)
    code_files = []
    async with httpx.AsyncClient() as client:
        for item in directory_contents:
            if item['type'] == 'file' and item['name'].endswith(('.py', '.java', '.js', '.html', '.css')):
                response = await client.get(item['download_url'])
                response.raise_for_status()
                code_content = response.text
                code_files.append({item['name']: code_content})

        return code_files


async def analyze_code(review_request: ReviewRequest):
    code = await get_code_from_directory(review_request.github_repo_url)
    prompt = f"""
  Imagine you are an IT professional and your task is to review the code as honestly as possible.

### Additional Description:

{review_request.description}

### Code Repository:
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
        messages=[
            {
                "role": "user",
                "content": f"{prompt}"
            }
        ],
    )
    analysis_result = response.message.content[0].text

    found_files = []
    downsides = parse_text(analysis_result, "2. **Downsides and Improvements:**", "3. **Rating:**")
    rating = parse_text(analysis_result, "3. **Rating:**", "4. **Conclusion:**")
    conclusion = parse_text(analysis_result, "**Conclusion:**")
    # parsing list files
    for files in code:
        for k, v in files.items():
            found_files.append(k)
    return ReviewResponse(found_files=found_files, downsides=downsides, rating=rating, conclusion=conclusion,
                          candidate_level=review_request.candidate_level,
                          github_repo_url=review_request.github_repo_url)


def parse_text(text, start_word, end_word=None):
    try:
        start_index = text.index(start_word) + len(start_word)

        if end_word:
            end_index = text.index(end_word)
            return text[start_index:end_index].strip()
        else:
            return text[start_index:-1].strip()
    except ValueError as ve:
        return f"Error: {ve}"
    except Exception as e:
        return f"Error: {e}"


async def main():
    url = 'https://github.com/froozy3/Web-Resume'
    content_directory = await get_directory_contents(url)
    print(content_directory)
    # codes = await get_code_from_directory(url)
    # print(codes)
    request = ReviewRequest(description="Analyze code", github_repo_url=url, candidate_level='Junior',
                            )
    response = await analyze_code(request)
    print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
