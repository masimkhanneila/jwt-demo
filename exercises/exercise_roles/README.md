# Exercise: add role based access

Use the `role` claim from the previous exercise to protect an endpoint.

Add `GET /teacher`. It should return a short message only for a user with the
`teacher` role.

Requirements:

- A valid token is required.
- A teacher receives `200`.
- A student receives `403`.
- A missing or invalid token is rejected.
- Read the role from the verified JWT. Do not accept it from a query parameter
  or request body.

Test the endpoint with tokens for both demo users. This shows the difference
between authentication, proving who the user is, and authorization, checking
what that user may do.

## Tips

1. Start the endpoint with the same `HTTPBearer` dependency used by `/me`.
2. Decode the bearer token with the same secret and algorithm, and return `401`
   when decoding raises `jwt.InvalidTokenError`.
3. Check the verified payload's `role`; return `403` unless it is `teacher`.
