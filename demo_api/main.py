from fastapi import FastAPI, Header, HTTPException
from typing import Optional

app = FastAPI(
    title="SentinelAPI Demo Banking API",
    description="Intentionally vulnerable API for SentinelAPI testing",
    version="1.0.0"
)

# -------------------------------------------------
# DEMO USERS
# -------------------------------------------------

users = {
    1: {
        "id": 1,
        "name": "Rahul Sharma",
        "email": "rahul@example.com",
        "password_hash": "demo_hash_123",
        "api_key": "DEMO_API_KEY_USER_1"
    },

    2: {
        "id": 2,
        "name": "Aman Verma",
        "email": "aman@example.com",
        "password_hash": "demo_hash_456",
        "api_key": "DEMO_API_KEY_USER_2"
    }
}


# -------------------------------------------------
# DEMO TOKENS
# -------------------------------------------------

tokens = {
    "token-user-1": 1,
    "token-user-2": 2
}


# -------------------------------------------------
# HOME
# -------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "SentinelAPI Demo Banking API",
        "status": "running"
    }


# -------------------------------------------------
# LOGIN
# -------------------------------------------------

@app.post("/login")
def login(username: str, password: str):

    # Intentionally simple demo login
    if username == "rahul" and password == "1234":
        return {
            "access_token": "token-user-1",
            "user_id": 1
        }

    if username == "aman" and password == "1234":
        return {
            "access_token": "token-user-2",
            "user_id": 2
        }

    raise HTTPException(
        status_code=401,
        detail="Invalid username or password"
    )


# -------------------------------------------------
# GET USER
# INTENTIONALLY VULNERABLE TO BOLA / IDOR
# -------------------------------------------------

@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    authorization: Optional[str] = Header(default=None)
):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    # We verify that the token is valid...
    # BUT we intentionally DO NOT verify ownership.
    # This creates a BOLA/IDOR vulnerability.

    token = authorization.replace("Bearer ", "")

    if token not in tokens:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Intentionally returning sensitive fields too.
    return users[user_id]


# -------------------------------------------------
# PROFILE
# INTENTIONALLY WEAK AUTHENTICATION
# -------------------------------------------------

@app.get("/profile")
def profile():
    return {
        "id": 1,
        "name": "Rahul Sharma",
        "email": "rahul@example.com",
        "message": "This endpoint should require authentication"
    }


# -------------------------------------------------
# ORDERS
# INTENTIONALLY VULNERABLE TO BOLA / IDOR
# -------------------------------------------------

orders = {
    101: {
        "order_id": 101,
        "user_id": 1,
        "product": "Laptop",
        "amount": 75000
    },

    102: {
        "order_id": 102,
        "user_id": 2,
        "product": "Mobile Phone",
        "amount": 25000
    }
}


@app.get("/orders/{order_id}")
def get_order(
    order_id: int,
    authorization: Optional[str] = Header(default=None)
):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    token = authorization.replace("Bearer ", "")

    if token not in tokens:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    if order_id not in orders:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    # Intentionally missing ownership validation
    return orders[order_id]


# -------------------------------------------------
# TRANSACTION
# -------------------------------------------------

@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int):

    return {
        "transaction_id": transaction_id,
        "amount": 5000,
        "status": "completed",
        "account": "DEMO-ACCOUNT-12345"
    }