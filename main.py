import os
import asyncio
from fastapi import FastAPI, Request

app = FastAPI(title="Gunicorn + Uvicorn 배포 가이드")

# 모든 요청마다 실행되는 미들웨어
@app.middleware("http")
async def log_process_id(request: Request, call_next):
    # 현재 이 코드를 실행 중인 워커의 PID를 가져옵니다.
    current_pid = os.getpid()
    
    # 터미널에 먼저 어떤 워커가 일하기 시작했는지 출력
    print(f"--- [Worker PID: {current_pid}] 요청 처리 시작: {request.url.path} ---")
    
    response = await call_next(request)
    return response

@app.get("/")
async def read_root():
    return {"message": "Hello World from FastAPI Worker!"}

@app.get("/io-bound-task")
async def io_bound_task():
    # 실제 환경에서 DB 조회나 외부 API 호출로 인해 1초가 소요되는 상황을 시뮬레이션합니다.
    # await를 사용했기 때문에 이 대기 시간 동안 워커는 다른 유저의 요청을 처리할 수 있습니다.
    await asyncio.sleep(1)
    return {"status": "success", "data": "Heavy I/O operation completed."}