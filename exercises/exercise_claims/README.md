# Exercise: users and JWT claims

Complete the exercise in two parts.

## Part 1: add a `USERS` dictionary

Replace the single hard-coded login check with a dictionary of users. Store
each role with its user on the server. The client does not choose its own role.

```python
USERS = {
    "student": {"password": "python", "role": "student"},
    "teacher": {"password": "fastapi", "role": "teacher"},
}
```

Use these demo credentials:

| Username | Password | Role |
| --- | --- | --- |
| `student` | `python` | `student` |
| `teacher` | `fastapi` | `teacher` |

For this part:

1. `/login` accepts both users.
2. Wrong credentials return `401`.
3. The existing `/me` endpoint still works.

The `role` value is stored with the user, but it is not a JWT claim yet. Keep
the token payload unchanged for now.

## Part 2: add the `role` claim

Now put the matching user's role into the JWT.

For example, a teacher's decoded token should contain `sub: "teacher"` and
`role: "teacher"` alongside `exp`.

For this part:

1. The token contains `sub` with the username and `role` with the user's role.
2. `/me` returns the username and role from the verified token.
3. The student token has `role: "student"` and the teacher token has
   `role: "teacher"`.

Try logging in as both users. Decode the token at [jwt.io](https://jwt.io/) and
find the claims. Do not enter a real secret or password there.

## Tips

1. Part 1: set `user = USERS.get(data.username)` and reject the request if
   `user` is missing or its password does not match.
2. Part 2: pass `user["role"]` to `create_token()` and add it to the payload
   next to `sub`.
3. Part 2: read `sub` and `role` from the verified payload in `/me`, then return
   both values.
