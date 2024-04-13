from app.server.service import websocket as websocket_service
# JWT Implementation
from app.server.utils.token import get_current_user
from fastapi import (
    APIRouter,
    status,
    WebSocket
)
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import os
# Get the path to the templates directory
templates_dir = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)),
    "../templates")

# Create an instance of Jinja2Templates
templates = Jinja2Templates(directory=templates_dir)

router = APIRouter()


@router.websocket("/message-broadcast")
async def message_broadcast(websocket: WebSocket):
    await websocket.accept()  # Accept the WebSocket connection
    token = websocket.headers.get('Authorization')
    if not token:
        """
        The unauthorized connection is handled by sending a close frame with a status code of status.
        WS_1008_POLICY_VIOLATION and a reason explaining the issue.
        """
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Token is missing or invalid.")
        return
    response = await get_current_user(token)
    websocket = await websocket_service.message_broadcast(websocket, response.username)
    return JSONResponse({'status': status.HTTP_200_OK, 'response': websocket})
