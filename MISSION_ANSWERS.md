#  Mission Answers — Day 12 Lab Submission

> **Student Name:** Phan Thị Mai Phương 
> **Student ID:** 2A202600281 
> **Date:** 17-04-2026

---

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. API key hardcode trong code
2. Không có config management
3. Print thay vì proper logging
4. Không có health check endpoint
5. Port cố định — không đọc từ environment


### Exercise 1.3: Comparison table
| Feature           | Basic                   | Advanced                      | Tại sao quan trọng?                                     |
| ----------------- | ----------------------- | ----------------------------- | ------------------------------------------------------- |
| Config            | Hardcode trong code     | Env vars (`settings`)         | Tách config khỏi code → deploy nhiều môi trường dễ dàng |
| Secrets           | Lộ API key, DB password | Không log secret, lấy từ env  | Tránh leak credentials → security critical              |
| Logging           | `print()`               | JSON structured logging       | Dễ parse, search, monitor (Datadog, Loki…)              |
| Health check      | ❌ Không có             | `/health`                     | Platform biết service còn sống để restart               |
| Readiness         | ❌ Không có             | `/ready`                      | Load balancer chỉ route khi service sẵn sàng            |
| Metrics           | ❌ Không có             | `/metrics`                    | Quan sát hệ thống (monitoring, alerting)                |
| Shutdown          | Đột ngột                | Graceful (lifespan + SIGTERM) | Không mất request đang chạy                             |
| Startup lifecycle | ❌ Không có             | `lifespan`                    | Init resource đúng cách (DB, model…)                    |
| API design        | Query param cho POST    | JSON body + validation        | API rõ ràng, chuẩn REST                                 |
| Error handling    | Không rõ ràng           | HTTPException chuẩn           | Client hiểu lỗi                                         |
| Networking        | `localhost`             | `0.0.0.0`                     | Container có thể nhận traffic từ bên ngoài              |
| Port              | Hardcode 8000           | `PORT` env var                | Tương thích cloud (Railway, Render…)                    |
| CORS              | ❌ Không có             | Configurable                  | Cho phép frontend gọi API                               |
| Debug mode        | Luôn bật                | Controlled qua env            | Tránh lỗi/perf issue production                         |
| Observability     | Gần như không có        | Logging + metrics             | Debug production nhanh hơn                              |
| Scalability       | Local-only              | Cloud-ready                   | Có thể scale nhiều instance                             |


## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image: image nền mà Docker sử dụng để xây dựng container, cung cấp môi trường ban đầu (OS + runtime), ví dụ python:3.11 đã bao gồm Python và các thư viện hệ thống cần thiết.
2. Working directory: thư mục làm việc mặc định bên trong container, tất cả các lệnh như COPY, RUN, CMD sau đó sẽ được thực thi trong thư mục này nếu không chỉ định đường dẫn khác.
3. Tại sao COPY requirements.txt trước: Để tận dụng Docker layer cache:
* Nếu requirements.txt không thay đổi → Docker không cần cài lại dependencies
* Giúp build nhanh hơn đáng kể khi chỉ thay đổi code

4. CMD vs ENTRYPOINT khác nhau thế nào: 

CMD là lệnh mặc định và có thể dễ dàng bị override khi chạy container.
Trong khi đó, ENTRYPOINT là lệnh chính cố định, thường không bị thay đổi, và các tham số truyền vào sẽ được thêm vào phía sau.


### Exercise 2.3: Image size comparison
- Develop: 1699.84 MB
- Production: 236 MB
- Difference: ~86.12%

### Exercise 2.4: Diagram
```
Client
  ↓
Nginx (80 / 443)
  ↓
Agent (FastAPI, 8000)
  ↓
├── Redis (6379)      [cache / session / rate limit]
└── Qdrant (6333)    [vector DB / RAG]
```

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- URL: https://day12-production-9100.up.railway.app
- Screenshot: 


## Part 4: API Security

### Exercise 4.1: Test results


### Exercise 4.2: Test results
```
~$ curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "student", "password": "demo123"}'
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHVkZW50Iiwicm9sZSI6InVzZXIiLCJpYXQiOjE3NzY0MzQ3MDQsImV4cCI6MTc3NjQzODMwNH0.jTd4Qk1U7JTpSuVAvJ5Y8EQLc9ERbCYsjSVGMbDxrus","token_type":"bearer","expires_in_minutes":60,"hint":"Include in header: Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."}

~$ TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHVkZW50Iiwicm9sZSI6InVzZXIiLCJpYXQiOjE3NzY0MzQ3MDQsImV4cCI6MTc3NjQzODMwNH0.jTd4Qk1U7JTpSuVAvJ5Y8EQLc9ERbCYsjSVGMbDxrus"
curl http://localhost:8000/ask -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain JWT"}'
{"question":"Explain JWT","answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic.","usage":{"requests_remaining":9,"budget_remaining_usd":2.1e-05}}
```

### Exercise 4.3: Test results
```
{"question":"Test 1","answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé.","usage":{"requests_remaining":9,"budget_remaining_usd":3.7e-05}}
{"question":"Test 2","answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé.","usage":{"requests_remaining":8,"budget_remaining_usd":5.3e-05}}
{"question":"Test 3","answer":"Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã được nhận.","usage":{"requests_remaining":7,"budget_remaining_usd":7.2e-05}}
{"question":"Test 4","answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic.","usage":{"requests_remaining":6,"budget_remaining_usd":9.3e-05}}
{"question":"Test 5","answer":"Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã được nhận.","usage":{"requests_remaining":5,"budget_remaining_usd":0.000112}}
{"question":"Test 6","answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé.","usage":{"requests_remaining":4,"budget_remaining_usd":0.000128}}
{"question":"Test 7","answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic.","usage":{"requests_remaining":3,"budget_remaining_usd":0.000149}}
{"question":"Test 8","answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé.","usage":{"requests_remaining":2,"budget_remaining_usd":0.000165}}
{"question":"Test 9","answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic.","usage":{"requests_remaining":1,"budget_remaining_usd":0.000186}}
{"question":"Test 10","answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé.","usage":{"requests_remaining":0,"budget_remaining_usd":0.000202}}
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":59}}
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":59}}
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":59}}
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":59}}
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":59}}
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":59}}
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":59}}
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":59}}
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":59}}
{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":59}}
```

### Exercise 4.4: Cost guard implementation
```
import redis
from datetime import datetime

# Kết nối Redis
r = redis.Redis(host="localhost", port=6379, db=0)

MONTHLY_BUDGET = 10.0  # $10 / tháng


def get_month_key(user_id: str) -> str:
    now = datetime.utcnow()
    return f"cost:{user_id}:{now.year}-{now.month}"


def check_budget(user_id: str, estimated_cost: float) -> bool:
    """
    Return True nếu còn budget, False nếu vượt.
    """

    key = get_month_key(user_id)

    # Lấy current spending
    current = r.get(key)
    current_spent = float(current) if current else 0.0

    # Check nếu vượt
    if current_spent + estimated_cost > MONTHLY_BUDGET:
        return False

    return True
```
	
Lý do:

- `**cost:{user}:{year-month}**` - không overwrite data cũ, dễ query và debug
- `**estimate_cost**` trước LLM: để check trước khi tốn thêm chi phí call LLM
- Redis: bởi so với in-memory, Redis có dữ liệu persisitent, scale được và multi-instance. Nhất là khi với system nhiều agent container có thể shared state

## Part 5: Scaling & Reliability

### Exercise 5.1: 
```
@app.get("/health")
def health():
    return {"status": "ok"}
	
@app.get("/ready")
def ready():
    try:
        # Check Redis
        if r.ping():
            return {"status": "ready"}

        raise Exception("Redis ping failed")

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not ready",
                "error": str(e)
            }
        )
```    

### Exercise 5.2: 
Kết quả:
```
$ INFO:     Shutting down
INFO:     Waiting for application shutdown.
2026-04-18 00:39:31,451 INFO 🔄 Graceful shutdown initiated...
2026-04-18 00:39:31,451 INFO ✅ Shutdown complete
INFO:     Application shutdown complete.
INFO:     Finished server process [13443]
2026-04-18 00:39:31,452 INFO Received signal 15 — uvicorn will handle graceful shutdown

[1]+  Done                    python app.py
```

- Nghĩa là app đã shutdown đúng chuẩn (graceful shutdown):
  - Nhận lệnh dừng (SIGTERM)
  - Dừng từ từ, không crash
  - Đóng sạch tài nguyên (server, request, v.v.)
  - Không mất dữ liệu giữa chừng

### Exercise 5.3-5.4: 
```
~$ for i in {1..10}; do
  curl http://localhost:8080/ask -X POST \
    -H "Content-Type: application/json" \
    -d '{"question": "Request '$i'"}'
done
{"answer":"Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã được nhận."}{"answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic."}{"answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic."}{"answer":"Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã được nhận."}{"answer":"Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã được nhận."}{"answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic."}{"answer":"Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã được nhận."}{"answer":"Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã được nhận."}{"answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic."}{"answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic."}
```

* Kết quả cho thấy:
  * Khi deploy (Docker / Kubernetes / Railway / Render)
  * Khi scale down (giảm số container)
  * Khi restart service
  * Khi load balancer thay instance

=> hệ thống sẽ KHÔNG “kill đột ngột”
mà sẽ: 
  * Nhận tín hiệu SIGTERM
  * Ngừng nhận request mới
  * Chờ request đang chạy xong
  * Đóng app sạch sẽ
  * Thoát process
  
### Exercise 5.5: 