from models.models import ReviewRequest
from services.github_service import *
from services.cohere_service import *

async def main():
    url = 'https://github.com/froozy3/CodeReviewAI'
    content_directory = await get_directory_contents(url,'tests')
    print(content_directory)
    codes = await get_file_contents(url,'tests')
    print(codes)
    request = ReviewRequest(description="Analyze code", github_repo_url=url, candidate_level='Junior',
                            )
    # response = await analyze_code(request)
    # print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
