import time
from collections import deque
from fastapi import HTTPException, Request

class SlidingWindowRateLimiter:
    def __init__(self, requests_limit: int, window_seconds: int):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self.user_requests = {}

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        
        if client_id not in self.user_requests:
            self.user_requests[client_id] = deque()
            
        requests = self.user_requests[client_id]
        
        # Remove expired timestamps
        while requests and now - requests[0] > self.window_seconds:
            requests.popleft()
            
        if len(requests) < self.requests_limit:
            requests.append(now)
            return True
        return False

    def get_retry_after(self, client_id: str) -> int:
        if client_id not in self.user_requests or not self.user_requests[client_id]:
            return 0
        
        # The next available slot is when the oldest timestamp in the current window expires
        oldest_ts = self.user_requests[client_id][0]
        retry_at = oldest_ts + self.window_seconds
        return max(1, int(retry_at - time.time()))

# Global instance for 5 requests per minute
market_limiter = SlidingWindowRateLimiter(requests_limit=5, window_seconds=60)

async def check_rate_limit(request: Request):
    client_ip = request.client.host
    if not market_limiter.is_allowed(client_ip):
        retry_after = market_limiter.get_retry_after(client_ip)
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Too Many Requests",
                "message": f"Rate limit exceeded. Try again in {retry_after} seconds.",
                "retry_after": retry_after
            },
            headers={"Retry-After": str(retry_after)}
        )
