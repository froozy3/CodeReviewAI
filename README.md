# CodeReviewAI

CodeReviewAI is an asynchronous backend tool designed to analyze code repositories and provide insightful feedback on code quality. It integrates with GitHub to fetch repository contents and uses AI to generate comprehensive code reviews, highlighting strengths, weaknesses, and overall ratings.

## Features

- **Asynchronous Code Analysis**: Efficiently fetch and analyze code files from GitHub repositories.
- **AI-Powered Reviews**: Utilizes AI to provide detailed code reviews, including observations, improvements, and ratings.
- **Flexible Input**: Accepts GitHub repository URLs and candidate levels for personalized feedback.
- **Easy Integration**: Simple RESTful API endpoints for analyzing code.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Poetry for dependency management
- Access to the Cohere API for AI analysis
- Access to the GitHub API for fetching repository contents

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/froozy3/CodeReviewAI.git
   cd CodeReviewAI

2. Install dependencies using Poetry:

   ```bash
   poetry install
   
3. Set up environment variables for your API keys in a .env file:
   ```plaintext
   CO_API_KEY=your_cohere_api_key
   GITHUB_TOKEN=your_github_token

4. Running the Application 
To start the FastAPI application, use the following command:
    
   ```bash
   poetry run uvicorn main:app --host 0.0.0.0 --port 8000

Your API will be available at http://localhost:8000.


## API ENDPOINTS

### Analyze Code
- **POST** `/analyze-code`

  **Request Body:**
    ```json
    {
      "description": "Your code review description.",
      "github_repo_url": "https://github.com/user/repo",
      "candidate_level": "Junior"
    }
    ```

  **Response:**
    ```json
    {
        "found_files": [
            "main.py",
            "__init__.py",
            "models.py",
            "cohere_service.py",
            "github_service.py",
            "test_review.py",
            "parsing.py"
        ],
        "downsides": "- The code structure is generally good, with clear separation of concerns and modularity. However, there are some areas for improvement:\n     - Error Handling: The error handling in the `analyze_code_rout` function could be more robust. Currently, it catches a generic `Exception` and raises an HTTP 500 error. It would be better to catch specific exceptions related to the code analysis process and provide more detailed error messages. For example, you could catch exceptions related to the Cohere API or parsing errors and provide more context in the error response.\n     - Logging: While logging is used in various parts of the code, it could be more consistent and informative. For instance, in the `get_repo_code_files` function, logging the number of files retrieved or any errors encountered during the process would be helpful.\n     - Input Validation: The code could benefit from more rigorous input validation. For instance, in the `get_repo_contents` function, you could validate the `repo_url` format before making the API call to avoid potential errors.",
        "rating": "3/5",
        "conclusion": "The code demonstrates a well-structured and organized approach to analyzing GitHub repositories and providing code reviews. It utilizes the Cohere API effectively for natural language processing and integrates various components like FastAPI, Pydantic, and GitHub API seamlessly. However, improvements in error handling, logging, and input validation would enhance the overall robustness and user experience of the application.",
        "candidate_level": "Junior",
        "github_repo_url": "https://github.com/user/repo"
    }
    ```




