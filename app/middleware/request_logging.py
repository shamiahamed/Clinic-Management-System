import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Setup logging to a file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("clinic_management.log"), # This creates the file
        logging.StreamHandler() # This still shows logs in your terminal
    ]
)
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log the incoming request
        logger.info(f"Incoming request: {request.method} {request.url.path}")

        response = await call_next(request)

        process_time = time.time() - start_time
        
        # Log the outgoing response status
        logger.info(
            f"Completed request: {request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Duration: {process_time:.2f}s"
        )
        
        return response