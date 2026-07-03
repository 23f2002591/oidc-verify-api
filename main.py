from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import jwt
from jwt import InvalidTokenError

app = FastAPI()

ISSUER = "https://idp.exam.local"
AUDIENCE = "tds-ostny57q.apps.exam.local"

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2okOHspNjgA+2rTLbeuY
cxiP/hG8C6Sb9iwg3yiLAA4HCnpITcbWCSelbvbYGuc3EbNy4xFyf5Cbj5DHJMID
EkryOgyd2giIIIBOUBj8S63uGcnRpOBh9NFatfNwheKuzsPuVNldu6A9cNteNpXc
WyJjG2axVfmq7i6SuKr1JoWYG7xTTAvKPujSl4OtsQfO3h5NepzdfXpr28oNnzfW
ed+zclR6BcmNNo/WVfJ4xyCLSf0BCOgdTgW6PdaChd1l9VDetJZVEgC5tkyvXsfI
SI6iyrYbKR0NEBSqq4XkadEjsCs4F1RncsS4LlgniT7GlkL9Mce3b0wGLs9/7ZIX
dQIDAQAB
-----END PUBLIC KEY-----"""


class TokenRequest(BaseModel):
    token: str


@app.post("/verify")
async def verify(body: TokenRequest):
    try:
        claims = jwt.decode(
            body.token,
            key=PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=AUDIENCE,
            options={
                "require": ["exp", "iss", "aud"],
                "verify_signature": True,
                "verify_exp": True,
                "verify_iss": True,
                "verify_aud": True,
            },
        )
    except InvalidTokenError:
        return JSONResponse(status_code=401, content={"valid": False})
    except Exception:
        return JSONResponse(status_code=401, content={"valid": False})

    return JSONResponse(
        status_code=200,
        content={
            "valid": True,
            "email": claims.get("email"),
            "sub": claims.get("sub"),
            "aud": claims.get("aud"),
        },
    )


@app.get("/")
async def root():
    return {"status": "ok", "service": "oidc-token-verification-service"}
