from pydantic import BaseModel
from typing import Literal, List


class ReviewRequest(BaseModel):
    description: str
    github_repo_url: str
    candidate_level: Literal['Junior', 'Middle', 'Senior']


class ReviewResponse(BaseModel):
    found_files: List[str]
    downsides: str
    rating: str
    conclusion: str
    candidate_level: Literal['Junior', 'Middle', 'Senior']
    github_repo_url: str

    def __str__(self):
        found_files_str = "1. **Files Found:**\n" + '\n'.join(f"   - {file}" for file in self.found_files)

        return (f"[GITHUB REPOSITORY]: {self.github_repo_url}\n\n"
                f"{found_files_str}\n\n"
                f"2. **Downsides and Improvements:**\n   {self.downsides}\n\n"
                f"3. **Rating:** \n   {self.rating}/5 (for {self.candidate_level})\n\n"
                f"4. **Conclusion:**\n   {self.conclusion}.")
