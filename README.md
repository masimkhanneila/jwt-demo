# JWT with FastAPI

JWT is a signed text token. A server gives one to a user after login. The user
sends it with later requests to prove who they are.

## Run

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

Open <http://127.0.0.1:8000/docs>.

1. Call `POST /login` with:

   ```json
   {"username": "student", "password": "python"}
   ```

2. Copy the `access_token` from the response.
3. Click **Authorize**, paste the token, and call `GET /me`.

The important part is in `main.py`:

- `jwt.encode(...)` creates a signed token.
- `jwt.decode(...)` checks the signature and expiration time.
- `Authorization: Bearer ...` sends the token to the protected endpoint.

The secret and password are hard-coded only to keep this example small. A real
app stores secrets safely and checks users in a database.

## Exercises

Start with [exercises/exercise_claims](exercises/exercise_claims), then continue
with the other exercises in that folder.
