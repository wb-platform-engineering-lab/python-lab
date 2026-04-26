"""Challenge 3 — Decorators.

Timing, logging, and retry decorators applied to pipeline functions.
Demonstrates @functools.wraps and decorator factories.
"""
import time
import functools


# --- @timed: measure execution time ---

def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start   = time.perf_counter()
        result  = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{func.__name__} took {elapsed:.1f}ms")
        return result
    return wrapper


@timed
def process_batch(orders):
    """Process a list of orders and return dispatch count."""
    return sum(1 for o in orders if o["status"] == "pending")


print("=== @timed ===")
orders = [
    {"order_id": "ORD-001", "status": "pending"},
    {"order_id": "ORD-002", "status": "pending"},
    {"order_id": "ORD-003", "status": "cancelled"},
    {"order_id": "ORD-004", "status": "pending"},
    {"order_id": "ORD-005", "status": "pending"},
]
count = process_batch(orders)
print(f"Processed {count} orders")
print(f"Function name preserved: {process_batch.__name__}")   # 'process_batch', not 'wrapper'


# --- @logged: print entry and exit ---

def logged(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        arg_str = ", ".join(
            [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        )
        print(f"→ {func.__name__}({arg_str})")
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"← {func.__name__} returned in {elapsed:.1f}ms")
        return result
    return wrapper


@logged
def dispatch_order(order_id, sku, *, quantity=1):
    """Simulate dispatching a single order."""
    return {"order_id": order_id, "sku": sku, "quantity": quantity}


print()
print("=== @logged ===")
dispatch_order("ORD-001", "TENT-3P-GRN")
dispatch_order("ORD-002", "PACK-45L-BLK", quantity=3)


# --- decorator factory: @retry(max_attempts=N) ---

def retry(max_attempts=3, exceptions=(Exception,)):
    """Decorator factory: retry the wrapped function up to max_attempts times."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 1:
                        print(f"attempt {attempt} succeeded")
                    return result
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    print(f"attempt {attempt} failed: {e} — retrying")
        return wrapper
    return decorator


attempt_tracker = {"n": 0}

@retry(max_attempts=3, exceptions=(IOError,))
def call_warehouse_api(order_id):
    """Simulate an unreliable API that fails twice before succeeding."""
    attempt_tracker["n"] += 1
    if attempt_tracker["n"] < 3:
        raise IOError("warehouse unavailable")
    return {"status": "ok", "order_id": order_id}


print()
print("=== @retry ===")
result = call_warehouse_api("ORD-001")
print(f"result: {result}")


# --- stacking decorators ---

attempt_tracker2 = {"n": 0}

@timed
@retry(max_attempts=2, exceptions=(IOError,))
def call_api(endpoint):
    attempt_tracker2["n"] += 1
    if attempt_tracker2["n"] < 2:
        raise IOError("connection error")
    return f"response from {endpoint}"


print()
print("=== stacked: @timed + @retry ===")
result = call_api("/orders")
print(f"result: {result}")
