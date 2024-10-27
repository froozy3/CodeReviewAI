import logging

from services.cohere_service import *
from fastapi import FastAPI, APIRouter,HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

router = APIRouter()


@router.post("/analyze-code", response_model=ReviewResponse)
async def analyze_code_rout(review_request: ReviewRequest):
    try:
        logging.info(f"Received request: {review_request}")
        response = await analyze_code(review_request)
        response_json = jsonable_encoder(response)
        logging.info(f"Response: {response_json}")
        return JSONResponse(content=response_json)
    except Exception as e:
        logging.error(f"Error occurred during code analysis {e}")
        raise HTTPException(status_code=500,detail="An error occurred during code analysis")


app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
