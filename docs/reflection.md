# Reflection: Module 14 BREAD Calculator

## What I Implemented

I implemented full BREAD functionality for authenticated calculations in both backend and frontend:
- Browse all user-specific calculations
- Read a specific calculation by ID
- Add new calculations with operation and operands
- Edit calculations (inputs and operation type) with recomputation
- Delete calculations safely without affecting other users

I also expanded end-to-end coverage with Playwright tests for positive and negative scenarios.

## Key Challenges

1. Keeping API and UI behavior aligned

The API already supported core BREAD, but the frontend needed stricter validation to prevent partially valid input from being silently accepted.

2. Test reliability

I updated E2E tests to use full register/login flows and unique user data so tests are isolated and repeatable.

3. Dependency compatibility

`aioredis` can break in newer Python environments. I replaced it with `redis.asyncio` and added in-memory fallback logic so blacklist checks still work when Redis is unavailable.

## What I Learned

- End-to-end tests are most useful when they mimic real user behavior from authentication through CRUD lifecycle.
- Input validation should happen both client-side and server-side.
- CI/CD and dependency updates should be done together to avoid environment drift.

## What I Would Improve Next

- Add pagination/filtering for larger calculation histories.
- Add API rate limiting and audit logs for security hardening.
- Add visual snapshot tests for frontend regression detection.
