from fastapi import Request
import logging
import time

async def log_requests(request: Request, call_next):
    logging.info(f"Request start {request.method} {request.url}")
    
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        # Se ocorrer um erro, re-raise a exceção para que ela seja tratada corretamente em outro lugar
        raise e
    
    process_time = (time.time() - start_time) * 1000
    logging.info(f"Request done: {request.method} {request.url} - Duration {process_time:.2f}ms")
    return response
