import time
import logging
import traceback

from fastapi import Request
from fastapi.responses import JSONResponse

async def logging_middleware(request: Request, call_next):
    """Automatically captures application errors,
    records route performance metrics, and structures logs for future ingestion"""
    
    start_time = time.time()
    payload = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "method": request.method,
        "path": request.url.path,
        "client_host": request.client.host if request.client else "unknown",
        "status_code": 500,        # Default fallback
        "latency_seconds": 0.0,
        "severity": "INFO",
        "exception": None,
        "traceback": None
    }
    
    try:
        response = await call_next(request)
        
        latency = time.time() - start_time
        payload["latency_seconds"] = round(latency, 4)
        payload["status_code"] = response.status_code
        
        if response.status_code >= 500:
            payload["severity"] = "ERROR"
        elif response.status_code >= 400:
            payload["severity"] = "WARNING"
        
        logging.log(
            logging.INFO if payload["severity"] == "INFO" else logging.ERROR,
            f"HTTP {payload['method']} {payload['path']} processed in {payload['latency_seconds']}s with status {payload['status_code']}"
        )
        
        # implement Azure Log Analytics Data Ingestion API endpoint delivery logic
        
        return response

    except Exception as exc:
        latency = time.time() - start_time
        payload["latency_seconds"] = round(latency, 4)
        payload["status_code"] = 500
        payload["severity"] = "CRITICAL"
        payload["exception"] = f"{type(exc).__name__}: {str(exc)}"
        payload["traceback"] = traceback.format_exc()
        
        logging.critical(
            f"CRITICAL EXCEPTION: HTTP {payload['method']} {payload['path']} failed after {payload['latency_seconds']}s. "
            f"Details: {payload['exception']}\n{payload['traceback']}"
        )
        
        # implement Azure Log Analytics Data Ingestion API endpoint delivery logic
        
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "detail": "An internal server error occurred while executing this data operation."
            }
        )