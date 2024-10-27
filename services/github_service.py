import os, httpx, logging
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
httpx_client = httpx.AsyncClient()


# returns content repository
async def get_repo_contents(repo_url: str, path: str = None):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else {None},
    }
    try:
        owner, repo = repo_url.split('/')[-2], repo_url.split('/')[-1]
    except ValueError:
        raise ValueError('Invalid GitHub repository URL format.')

    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    logging.info("Fetching repository content from GitHub.")

    if path:
        api_url += f"/{path}"

    response = await httpx_client.get(api_url, headers=headers)
    response.raise_for_status()

    return response.json()


# returns content code from directory
async def get_repo_code_files(repo_url: str, path: str = None):
    directory_contents = await get_repo_contents(repo_url, path)
    code_files = []

    for item in directory_contents:
        if item['type'] == 'file' and item['name'].endswith(('.py', '.java', '.js', '.html', '.css')):
            response = await httpx_client.get(item['download_url'])
            response.raise_for_status()
            code_files.append({item['name']: response.text})
        elif item['type'] == 'dir':
            subdirectory_files = await get_repo_code_files(repo_url, path=item['path'])
            code_files.extend(subdirectory_files)

    return code_files
