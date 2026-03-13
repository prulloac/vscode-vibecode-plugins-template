# Example: Real AI Agent Implementation Workflow

Complete walkthrough of implementing a real feature: **User Authentication System**.

**File Location**: All files in `docs/features/user-authentication/`

This example shows how feature-breakdown → feature-planning → ai-agent-implementation flows in practice.

______________________________________________________________________

## Part 0: Feature Context

**Feature**: User Authentication System

**Description**: Add user registration, login, logout, and session management to web app.

**Why we're building it**: New feature, critical for security, needed for user-specific features downstream.

______________________________________________________________________

## Part 1: Feature Breakdown (What we're building)

*Output from feature-breakdown skill*

The breakdown identified 12 tasks organized into 3 areas:

1. **Backend**: Database schema, API endpoints, authentication logic
1. **Frontend**: Login/register forms, session handling
1. **Integration**: End-to-end tests, security audit

Key acceptance criteria: User can register, log in, API validates tokens, tokens expire, logout clears session.

______________________________________________________________________

## Part 2: Execution Sequence (Task Order)

*Output from feature-planning skill*

Planning analyzed dependencies and created this sequence:

**Batch 1: Backend Foundation**

- Task 1: Create users database table (schema, migrations)
- Task 2: Implement password hashing & validation
- Task 3: Create authentication API endpoints (register, login, logout)

*Why these 3*: Related, foundational for other work, can test in parallel.

**Batch 2: Frontend & Session**

- Task 4: Build login/register UI forms
- Task 5: Add session management (store tokens, refresh logic)
- Task 6: Implement logout and cleanup

*Why these 3*: Depend on Batch 1 APIs, can build in parallel, all needed for complete flow.

**Batch 3: Integration & Testing**

- Task 7: End-to-end authentication flow tests
- Task 8: Security audit (password policies, token expiration)
- Task 9: Error handling and edge cases

*Why these 3*: Depend on both Batch 1 & 2, comprehensive testing, catch issues.

**Critical Path**: Batch 1 → Batch 2 → Batch 3 (strict dependency order).

______________________________________________________________________

## Part 3: Execution - Batch 1

### Preparation

You prepare Batch 1:

```markdown
# Batch Execution: User Auth - Batch 1: Backend Foundation

**Batch**: 1
**Name**: Backend Foundation
**Status**: Ready to execute

---

## Tasks in This Batch

### Task 1: Create users database table

**Description**:
Create PostgreSQL table for users with: id, email, password_hash, created_at, updated_at.
Add indexes on email (for login lookups).
Create migration file that can be run/reverted.

**Acceptance Criteria**:
- [ ] Migration file created and versioned
- [ ] Table has all required fields
- [ ] Email field is indexed
- [ ] Migration runs without errors
- [ ] Migration can be reverted

**Integration**: Task 2 will use this schema to store hashed passwords

---

### Task 2: Implement password hashing & validation

**Description**:
Create password utility: hash(plaintext) → hash, verify(plaintext, hash) → true/false.
Use bcrypt library. Configure reasonable cost factor.
Include validation: min length, strength requirements.

**Acceptance Criteria**:
- [ ] Passwords hashed with bcrypt
- [ ] Can verify plaintext against hash
- [ ] Validation rejects weak passwords
- [ ] Cost factor prevents brute-force attacks
- [ ] Unit tests pass

**Integration**: Task 3 will call these functions when users register/login

---

### Task 3: Create authentication API endpoints

**Description**:
POST /auth/register: email, password → user object
POST /auth/login: email, password → { user, token }
POST /auth/logout: → success
GET /auth/me: → current user

**Acceptance Criteria**:
- [ ] /register creates user, hashes password, returns user object
- [ ] /login validates credentials, returns JWT token
- [ ] /logout invalidates session (or returns success)
- [ ] /me returns current user if token valid, 401 if not
- [ ] All endpoints return proper error codes (400, 401, 409 for duplicate email, etc.)
- [ ] API tests pass

**Integration**: Frontend will call these endpoints

---

## Batch Overview

**Purpose**: Build backend foundation. After this batch, backend can fully authenticate users.

**Dependencies**:
- PostgreSQL database available
- Node.js + bcrypt library installed

**Integration**: Frontend will depend on these endpoints being available

**Expected Outcome**:
- Backend can register, authenticate, and verify users
- Ready for frontend integration

---

## Agent Instructions

Execute these 3 tasks in order:
1. Task 1 creates table foundation
2. Task 2 adds password logic
3. Task 3 builds API that uses both

All acceptance criteria must pass. If Task 1 fails, Task 2 won't work.

Success = All 3 tasks complete, all tests pass, API responds correctly.
```

### Agent Executes

You send the batch to Agent A. Here's what happens:

**Agent A Session Log**:

```
[Agent A starts working on Batch 1]

Task 1: Create users database table
- Creating migration file: 001_create_users_table.js
- Adding fields: id, email, password_hash, created_at, updated_at
- Adding email index
- Testing: migration runs successfully ✅
- Testing: migration reverts successfully ✅
Task 1 COMPLETE

Task 2: Implement password hashing
- Installing bcrypt library
- Creating password utility: hash() and verify()
- Adding validation: min 8 chars, must have uppercase + number
- Writing unit tests
- All tests passing ✅
Task 2 COMPLETE

Task 3: Create authentication endpoints
- Implementing POST /auth/register
  - Testing with valid user: ✅
  - Testing with duplicate email: returns 409 ✅
  - Testing with weak password: returns 400 ✅
- Implementing POST /auth/login
  - Testing with correct credentials: returns token ✅
  - Testing with wrong password: returns 401 ✅
- Implementing GET /auth/me
  - Testing with valid token: returns user ✅
  - Testing with invalid token: returns 401 ✅
- Implementing POST /auth/logout
  - Testing: returns success ✅
All endpoint tests passing ✅
Task 3 COMPLETE

Batch 1 Summary:
- All 3 tasks complete
- All acceptance criteria met
- All tests passing
- Ready for frontend integration
```

### Verify & Document

You verify the work:

```markdown
# Session Summary: Batch 1 - [Date]

**Batch**: Backend Foundation
**Agent**: Agent A (claude-opus)
**Duration**: 2 hours

## Completed Tasks ✅

- Task 1: Database schema - ✅ Complete, migration tested
- Task 2: Password hashing - ✅ Complete, all validations working
- Task 3: API endpoints - ✅ Complete, all endpoints tested

## Issues Encountered

None - smooth execution.

## Integration Status

Backend is now ready for frontend to integrate against. Endpoints documented and tested.

## For Batch 2 (Frontend Team)

The backend provides:
- POST /auth/register → returns { id, email, created_at }
- POST /auth/login → returns { user: {...}, token: "jwt..." }
- POST /auth/logout → returns { success: true }
- GET /auth/me → returns { id, email } (requires token in header)

Use token in Authorization header: `Authorization: Bearer {token}`

All endpoints reject invalid input with descriptive errors.
```

And update implementation-progress.md:

```markdown
# Execution Progress: User Authentication System

**Overall Progress**: 25% complete (3 of 12 tasks done)

---

## Status Summary

| Status | Count | Tasks |
|--------|-------|-------|
| ✅ Complete | 3 | Task 1, 2, 3 |
| 🔄 In Progress | 0 | - |
| ⏭️ Ready to Start | 3 | Task 4, 5, 6 |
| 🔴 Blocked | 0 | - |
| ⚠️ Rework Needed | 0 | - |

---

## Completed Batches ✅

### Batch 1: Backend Foundation
- **Completed**: [Date]
- **Tasks**: Task 1, 2, 3
- **Status**: ✅ All tasks complete, all tests passing
- **Issues**: None
- **Integration**: Backend ready for frontend integration
- **Handoff**: Frontend can now call /auth/* endpoints with documented API format

---

## Ready to Start ⏭️

### Batch 2: Frontend & Session
- **Dependencies**: Batch 1 complete ✅
- **Blockers**: None
- **Tasks**: Task 4, 5, 6
- **Expected Start**: [Next agent session]
```

______________________________________________________________________

## Part 4: Execution - Batch 2

### Preparation

Now you prepare Batch 2, having learned from Batch 1:

```markdown
# Batch Execution: User Auth - Batch 2: Frontend & Session

**Batch**: 2
**Name**: Frontend & Session
**Status**: Ready to execute

---

## Prerequisites

Batch 1 is complete. The backend APIs are available:
- POST /auth/register
- POST /auth/login
- POST /auth/logout
- GET /auth/me

All return proper errors (400, 401, 409) and success responses. See Batch 1 handoff for details.

---

## Tasks in This Batch

### Task 4: Build login/register UI forms

**Description**:
Create React components: `<RegisterForm>` and `<LoginForm>`
Forms capture email and password, display validation errors.
Include "I have an account" link between forms.

**Acceptance Criteria**:
- [ ] Register form: email + password inputs + validation
- [ ] Login form: email + password inputs + validation
- [ ] Forms show error messages on invalid input
- [ ] Forms disable submit while submitting
- [ ] Can switch between login/register views
- [ ] Forms are accessible (labels, focus, keyboard nav)

**Integration**: Task 5 will add submission logic to these forms

---

### Task 5: Add session management (store tokens, refresh logic)

**Description**:
Create session utility:
- store(token): Save JWT token to localStorage
- get(): Retrieve token from localStorage
- clear(): Remove token
- refresh(): Handle token expiration, use refresh token

Create context or state management to provide current user globally.

**Acceptance Criteria**:
- [ ] Token stored securely in localStorage
- [ ] Can retrieve token across page reloads
- [ ] Token cleared on logout
- [ ] User context available throughout app
- [ ] Handles token expiration (redirect to login)
- [ ] Unit tests pass

**Integration**: Task 4 forms will call store() after login, Task 6 will call clear() on logout

---

### Task 6: Implement logout and cleanup

**Description**:
Create logout flow:
- Logout button calls backend /auth/logout
- Session token cleared from storage
- User context reset
- Redirect to login page
- All user-specific state cleared (carts, preferences, etc.)

**Acceptance Criteria**:
- [ ] Logout button visible when logged in
- [ ] Calls /auth/logout endpoint
- [ ] Token removed from storage
- [ ] Redirects to login page
- [ ] User-specific state cleared
- [ ] Can immediately log back in after logout

**Integration**: Uses session management from Task 5

---

## Batch Overview

**Purpose**:
Build frontend UI and session management. After this batch, users can:
1. Register → create account
2. Log in → get token, stay logged in
3. Log out → clear session, return to login

**Dependencies**:
All met - Batch 1 backend is complete and running

**Integration**:
- Forms call /auth/register and /auth/login endpoints (Task 4 → backend)
- Session management stores token and provides to app (Task 5 used by Task 4 & 6)
- Logout clears session and redirects (Task 6 uses Task 5)

---

## Agent Instructions

Execute tasks in order:
1. Task 4: Build forms (UI only)
2. Task 5: Add session management (state/context)
3. Task 6: Wire up logout (uses forms + session)

Acceptance criteria must pass. Forms look good, session persists across reloads, logout works cleanly.

**Key integration point**: After Task 4, forms won't actually submit yet (no hooks wired). After Task 5, can test full auth flow (register → log in → token saved). After Task 6, can test logout.
```

### Agent Executes

You send to Agent B:

**Agent B Session Log**:

```
Task 4: Build login/register UI forms
- Creating RegisterForm component
  - Email input with validation regex
  - Password input (masked)
  - Submit button
  - Error messages display
  - Accessibility: labels, ARIA, keyboard nav
- Creating LoginForm component (similar)
- Forms work, display properly ✅
- Forms handle invalid input ✅
Task 4 COMPLETE

Task 5: Add session management
- Creating sessionStorage utility
  - store(token): saves to localStorage
  - get(): retrieves token
  - clear(): removes token
- Creating UserContext for app-wide access
- Adding useUser() hook
- Testing: token persists after page reload ✅
- Testing: token cleared when clear() called ✅
Task 5 COMPLETE

Task 6: Implement logout
- Adding Logout button to Header
- Wiring submit handlers to forms (Task 4)
  - RegisterForm calls POST /auth/register
  - LoginForm calls POST /auth/login
  - On success: store(token) from Task 5, redirect home
  - On error: display error message
- Logout button calls POST /auth/logout
  - On success: clear() from Task 5, redirect to /login
- Testing: Full auth flow works ✅
  - Register: form → backend → token saved → redirect home
  - Login: form → backend → token saved → redirect home
  - Logout: clear token → redirect login
Task 6 COMPLETE
```

### Verify & Document

Session summary shows one issue:

```markdown
# Session Summary: Batch 2 - [Date]

**Batch**: Frontend & Session
**Agent**: Agent B
**Duration**: 3 hours

## Completed Tasks ✅

- Task 4: Login/register forms - ✅ Complete
- Task 5: Session management - ✅ Complete
- Task 6: Logout - ✅ Complete

## Issues Encountered 🔄

**Issue 1**: Form validation didn't match backend validation
- Problem: Frontend required password ≥ 8 chars, backend required ≥ 8 + uppercase + number
- Status: FIXED - Updated frontend regex to match backend
- Resolution: Agent added uppercase/number requirement to RegisterForm validation

## Integration Status

- Backend integration: ✅ Forms call APIs correctly
- Session persistence: ✅ Token saved/retrieved/cleared
- Logout flow: ✅ Complete

## For Batch 3 (Integration Tests)

Frontend is now fully functional:
- Users can register
- Users can log in (token saved automatically)
- Users can log out (clears session)
- User context available throughout app for conditionally rendering user-specific UI

Batch 3 should test full flows end-to-end and verify edge cases.
```

Update progress:

```markdown
# Execution Progress: User Authentication System

**Overall Progress**: 50% complete (6 of 12 tasks done)

---

## Status Summary

| Status | Count | Tasks |
|--------|-------|-------|
| ✅ Complete | 6 | Task 1, 2, 3, 4, 5, 6 |
| 🔄 In Progress | 0 | - |
| ⏭️ Ready to Start | 3 | Task 7, 8, 9 |
| 🔴 Blocked | 0 | - |
| ⚠️ Rework Needed | 0 | - |

---

## Completed Batches ✅

### Batch 1: Backend Foundation
- **Status**: ✅ Complete
- **Tasks**: Task 1, 2, 3

### Batch 2: Frontend & Session
- **Status**: ✅ Complete (1 minor issue fixed)
- **Tasks**: Task 4, 5, 6
- **Issues**: Frontend validation ≠ backend validation (fixed)

---

## Ready to Start ⏭️

### Batch 3: Integration & Testing
- **Dependencies**: Batch 1 & 2 both complete ✅
- **Blockers**: None
- **Tasks**: Task 7, 8, 9
```

______________________________________________________________________

## Part 5: Execution - Batch 3 (with blocker)

### Preparation

Prepare final batch:

```markdown
# Batch Execution: User Auth - Batch 3: Integration & Testing

**Batch**: 3
**Name**: Integration & Testing
**Status**: Ready

---

## Tasks

### Task 7: End-to-end authentication flow tests

**Acceptance Criteria**:
- [ ] Test: Register → user created, token returned
- [ ] Test: Login → token returned, session started
- [ ] Test: Logged-in user can access /auth/me
- [ ] Test: Logged-out user gets 401 on /auth/me
- [ ] Test: After logout, token doesn't work
- [ ] All scenarios covered by tests
- [ ] Tests run in CI/CD

...

### Task 8: Security audit

**Acceptance Criteria**:
- [ ] Passwords meet minimum complexity
- [ ] Tokens expire after N minutes
- [ ] Refresh tokens work correctly
- [ ] No sensitive data in logs
- [ ] No XSS vulnerabilities in forms
- [ ] CSRF protection in place
- [ ] Security checklist passed

...

### Task 9: Error handling and edge cases

**Acceptance Criteria**:
- [ ] Duplicate registration rejected (409)
- [ ] Case-insensitive email lookup (john@example.com = John@example.com)
- [ ] Concurrent login attempts handled
- [ ] Network errors gracefully handled
- [ ] Expired tokens trigger refresh or re-login
- [ ] All error scenarios tested
```

### Agent Executes

You send to Agent C:

**Agent C Session Log**:

```
Task 7: End-to-end tests
- Writing test: Register new user
  ✅ User created, token returned
- Writing test: Login existing user
  ✅ Token returned, valid
- Writing test: Access protected endpoint with token
  ✅ Returns user data
- Writing test: Access with invalid token
  ✅ Returns 401
- Writing test: After logout, token invalid
  ✅ Returns 401
All tests passing ✅
Task 7 COMPLETE

Task 8: Security audit
- Checking password requirements: ✅ 8+ chars, uppercase, number
- Checking token expiration: ✅ 1 hour
- Checking refresh token flow: 🔴 BLOCKER!
  - Token expiration implemented, but refresh token logic not implemented
  - Backend generates JWT but doesn't have refresh token endpoint
  - Frontend doesn't have refresh token logic

BLOCKED on Task 8 - Refresh token flow not implemented
```

### Identify Blocker

Agent reports blocker. You triage:

```markdown
### Blocker: Refresh token flow not implemented

**Type**: Design (requirements gap)

**Severity**: High (security feature missing)

**Affected Tasks**: Task 8

**Description**:
Feature supports token expiration (good), but no refresh token flow.
After token expires, user forced to log in again (not ideal).
Refresh token flow would let user stay logged in longer.

**Cause**:
Original spec didn't clarify refresh token requirement.
We implemented basic token expiration but didn't include refresh mechanism.

**Impact**:
Security audit fails (token expiration without refresh not production-ready).
Users have poor experience (logged out frequently).

**Resolution**:
We have 2 options:
1. Add refresh token flow (backend endpoint + frontend logic) - more work, better UX
2. Increase token expiration to longer (e.g., 24 hours) - simpler, acceptable for MVP

Decision: Option 2 (MVP approach). Change token expiration to 24 hours, document that refresh tokens are future work.
```

### Resolution

You update task acceptance criteria:

```markdown
### Task 8: Security audit (UPDATED)

**Acceptance Criteria**:
- [ ] Passwords meet minimum complexity (8+, uppercase, number)
- [ ] Tokens expire after 24 hours ← UPDATED (was: N minutes)
- [ ] ~~Refresh tokens work correctly~~ ← DEFER to future work
- [ ] No sensitive data in logs
- [ ] No XSS vulnerabilities in forms
- [ ] CSRF protection in place
- [ ] Security checklist passed
```

Agent redoes Task 8:

```
Task 8: Security audit (UPDATED)
- Password requirements: ✅
- Token expiration: Check backend...
  - Current: 1 hour expiration ❌
  - Need: 24 hour expiration
  - Updating: Changed JWT expiration to 24 hours ✅
- XSS check in forms: ✅ No unsanitized inputs
- CSRF: ✅ Tokens validated
- Security checklist: ✅ All items passed
Task 8 COMPLETE

Task 9: Error handling
- Duplicate email: ✅ Returns 409
- Case-insensitive email: ✅ john@example.com = John@example.com
- Concurrent logins: ✅ Each gets separate token
- Network errors: ✅ Gracefully handled
- Expired token behavior: ✅ Returns 401, frontend redirects to login
All edge cases covered ✅
Task 9 COMPLETE
```

### Final Documentation

```markdown
# Session Summary: Batch 3 - [Date]

**Batch**: Integration & Testing
**Agent**: Agent C
**Duration**: 4 hours

## Completed Tasks ✅

- Task 7: End-to-end tests - ✅ Complete, all tests passing
- Task 8: Security audit - ✅ Complete (refresh tokens deferred)
- Task 9: Error handling - ✅ Complete, all edge cases handled

## Blockers Encountered 🔄 → ✅ RESOLVED

**Blocker**: Refresh token flow not implemented
- **Type**: Design (requirements gap)
- **Resolution**: Deferred to Phase 2. MVP uses 24-hour token expiration.
- **Impact**: Low - MVP acceptable with longer token lifetime
- **Time to resolve**: 30 minutes (updated requirements + re-tested)

## Integration Status

- Backend: ✅ All security measures in place
- Frontend: ✅ Handles expiration gracefully
- Tests: ✅ Full coverage of auth flows

## Feature Complete ✅

User Authentication System fully implemented and tested.
Users can register, log in, maintain sessions, and log out.
```

______________________________________________________________________

## Summary: The Complete Flow

```
Feature Spec (Input)
    ↓
Breakdown skill (WHAT)
    → Output: 12 tasks with acceptance criteria
    ↓
Planning skill (ORDER)
    → Output: 3 batches, strict dependency order
    ↓
Batch 1 → Agent A (2 hours)
    → Output: Backend foundation complete
    ↓
Batch 2 → Agent B (3 hours, 1 minor fix)
    → Output: Frontend complete
    ↓
Batch 3 → Agent C (4 hours, 1 blocker resolved)
    → Output: Integration & testing complete
    ↓
Feature Complete ✅
```

**Total effort**: 9 hours + 1.5 hours blocker resolution = ~10 hours
**Batches**: 3 agent sessions, each focused and manageable
**Issues**: 1 minor validation mismatch, 1 design blocker (both resolved quickly)
**Result**: Complete, tested, production-ready authentication system

______________________________________________________________________

## Key Lessons from Example

1. **Batching works**: 3 batches of 1-3 tasks each = focused sessions, clear handoffs
1. **Blockers happen**: When they do, triage fast (30 min vs 4 hours saved)
1. **Integration matters**: Verify between batches (Task 4/5/6 form + session + logout all needed together)
1. **Document everything**: Session summaries help next agent understand what happened
1. **Flexibility wins**: When blocker found, quick design decision (defer refresh tokens) kept progress moving
1. **Validation alignment**: Minor issue (form validation ≠ backend) caught in Batch 2, fixed in 30 min

______________________________________________________________________

## See Also

- `SKILL.md`: Core execution workflow
- `batch-execution-template.md`: Template to prepare batches
- `blocker-triage-guide.md`: How to handle blockers like the refresh token one
- `implementation-progress.md` example: Live tracking format
