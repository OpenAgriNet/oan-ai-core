from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from agents.moderation import moderation_agent

app = FastAPI(title="Moderation Microservice")

class ModerationRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=5000)

@app.post("/moderate")
async def check_moderation(request: ModerationRequest):
    try:
        # Run the agent
        result = await moderation_agent.run(request.query)
        # Return the structured data directly
        return result.data
    except Exception as e:
        print(f"Error processing moderation request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)