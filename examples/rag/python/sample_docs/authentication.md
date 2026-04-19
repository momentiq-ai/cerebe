# Authentication

Every Cerebe API request is authenticated with an API key sent as the `X-API-Key` header. Keys are created in the [Cerebe Dashboard](https://cerebe.ai/dashboard/keys).

## Key formats

Cerebe issues two key variants:

- `ck_live_…` — production keys. These bill the org's production workspace and can read/write live data.
- `ck_test_…` — test keys. These target the sandbox environment. Use test keys in CI and local development.

Both variants have the same request shape — only the key prefix and backing environment differ.

## Sending the key

Every HTTPS request must include the header `X-API-Key: ck_live_your_key`. There is no query-string variant and no basic-auth fallback.

```bash
curl https://api.cerebe.ai/api/v1/memory/search \
  -H "X-API-Key: ck_live_your_key" \
  -H "Content-Type: application/json" \
  -d '{"query": "user preferences", "entity_id": "user_123"}'
```

The Python and TypeScript SDKs accept the key via constructor:

```python
from cerebe import Cerebe
client = Cerebe(api_key="ck_live_...")
```

## Rotation and scoping

Keys can be revoked and rotated from the dashboard at any time. A revoked key returns `401 Unauthorized` on the next request. Best practice is to scope a distinct key per deployment (one for production, one for staging, one per CI job) so that rotating one does not affect others.

## Handling auth errors

A request with an invalid, missing, or revoked key returns HTTP 401 with a JSON body describing the cause. A request with a valid key that lacks the required scope returns HTTP 403 with an `insufficient_scope` error and the name of the missing scope. Applications should surface a concrete next step ("check your `CEREBE_API_KEY` environment variable", "grant `rag:read` to your key in the dashboard") rather than exposing the raw server error to end users.
