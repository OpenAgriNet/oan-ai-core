from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from agents.moderation import get_moderation_agent
from helpers.utils import get_logger

app = FastAPI(title="Moderation Microservice")
logger = get_logger(__name__)

class ModerationRequest(BaseModel):
    """Request model for moderation endpoint."""
    query: str = Field(..., min_length=1, max_length=5000)

@app.post("/moderate")
async def check_moderation(request: ModerationRequest):
    """
    Moderate and validate a user query for appropriateness.
    
    Args:
        request: ModerationRequest containing the query to moderate
        
    Returns:
        dict: Moderation result with category and action
        
    Raises:
        HTTPException: 400 for validation errors, 500 for server errors
    """
    try:
        agent = get_moderation_agent()
        result = await agent.run(request.query)
        return result.data
    except ValueError as e:
        logger.warning(f"Invalid input: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Moderation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)