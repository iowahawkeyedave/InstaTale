# Tasks: AI-Powered Instagram Content Creator

**Feature**: 001-build-me-an | **Date**: 2025-09-13
**Input**: Design documents from `/specs/001-build-me-an/`
**Prerequisites**: plan.md (✅), research.md (✅), data-model.md (✅), contracts/ (✅), quickstart.md (✅)

## Execution Flow (main)
```
1. Load plan.md from feature directory ✅
   → Tech stack: Python 3.11/FastAPI + TypeScript/React 18
   → Libraries: OpenAI GPT-4V, OpenRouter, LM Studio, PostgreSQL, S3
   → Structure: Web app (backend/ + frontend/)
2. Load design documents ✅
   → data-model.md: 4 entities (ProcessingSession, ImageUpload, ImageAnalysis, GeneratedContent)
   → contracts/: 5 API endpoints across 2 files
   → research.md: All NEEDS CLARIFICATION resolved
   → quickstart.md: 6 test scenarios mapped
3. Generate tasks by category ✅
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, API endpoints
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules ✅
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001-T060) ✅
6. Generate dependency graph ✅
7. Create parallel execution examples ✅
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Web app structure**: `backend/src/`, `frontend/src/`
- Tests: `backend/tests/`, `frontend/tests/`

---

## Phase 3.1: Setup (T001-T005)
- [ ] T001 Create project structure: backend/ and frontend/ directories with src/ and tests/ subdirectories
- [ ] T002 Initialize Python backend with FastAPI, SQLAlchemy, pytest dependencies in backend/requirements.txt
- [ ] T003 [P] Initialize React frontend with TypeScript, TailwindCSS, Jest dependencies in frontend/package.json
- [ ] T004 [P] Configure backend linting: black, flake8, mypy in backend/pyproject.toml
- [ ] T005 [P] Configure frontend linting: ESLint, Prettier, TypeScript strict mode in frontend/.eslintrc.json and tsconfig.json

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**

### Contract Tests [P] (T006-T010)
- [ ] T006 [P] Contract test POST /v1/sessions in backend/tests/contract/test_sessions_post.py
- [ ] T007 [P] Contract test POST /v1/sessions/{id}/upload in backend/tests/contract/test_upload_post.py
- [ ] T008 [P] Contract test GET /v1/sessions/{id}/status in backend/tests/contract/test_status_get.py
- [ ] T009 [P] Contract test GET /v1/sessions/{id}/content in backend/tests/contract/test_content_get.py
- [ ] T010 [P] Contract test POST /v1/sessions/{id}/regenerate in backend/tests/contract/test_regenerate_post.py

### Integration Tests [P] (T011-T016)
- [ ] T011 [P] Integration test complete happy path workflow in backend/tests/integration/test_happy_path.py
- [ ] T012 [P] Integration test content regeneration flow in backend/tests/integration/test_regeneration.py
- [ ] T013 [P] Integration test file validation and error handling in backend/tests/integration/test_validation.py
- [ ] T014 [P] Integration test content moderation and policy violations in backend/tests/integration/test_moderation.py
- [ ] T015 [P] Integration test session expiration and cleanup in backend/tests/integration/test_sessions.py
- [ ] T016 [P] Integration test concurrent user scaling in backend/tests/integration/test_performance.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)

### Data Models [P] (T017-T020)
- [ ] T017 [P] ProcessingSession model with UUID, timestamps, status enum in backend/src/models/session.py
- [ ] T018 [P] ImageUpload model with file metadata, S3 key, validation rules in backend/src/models/upload.py
- [ ] T019 [P] ImageAnalysis model with JSON fields for objects, colors, mood in backend/src/models/analysis.py
- [ ] T020 [P] GeneratedContent model with caption, hashtags, style enum in backend/src/models/content.py

### Database Setup (T021-T022)
- [ ] T021 PostgreSQL connection, SQLAlchemy engine, database URL configuration in backend/src/database/connection.py
- [ ] T022 Alembic migrations for all models, relationships, indexes in backend/alembic/versions/001_initial_schema.py

### Backend Services [P] (T023-T030)
- [ ] T023 [P] Session management service: create, retrieve, expire sessions in backend/src/services/session_service.py
- [ ] T024 [P] File upload service: S3 upload, validation, virus scanning in backend/src/services/upload_service.py
- [ ] T025 [P] OpenAI Vision API service: image analysis, error handling, rate limiting in backend/src/services/openai_service.py
- [ ] T026 [P] OpenRouter API service: alternative AI provider integration in backend/src/services/openrouter_service.py
- [ ] T027 [P] LM Studio service: local model inference integration in backend/src/services/lmstudio_service.py
- [ ] T028 [P] Content generation service: LLM failover cascade, hashtag validation in backend/src/services/content_service.py
- [ ] T029 [P] Content moderation service: policy violation detection in backend/src/services/moderation_service.py
- [ ] T030 [P] Background job service: async processing, session cleanup in backend/src/services/job_service.py

### API Endpoints (T031-T035)
- [ ] T031 POST /v1/sessions endpoint: create session, return session_id and upload_url in backend/src/api/sessions.py
- [ ] T032 POST /v1/sessions/{id}/upload endpoint: handle multipart upload, start processing in backend/src/api/upload.py
- [ ] T033 GET /v1/sessions/{id}/status endpoint: return processing status and progress in backend/src/api/status.py
- [ ] T034 GET /v1/sessions/{id}/content endpoint: return generated caption and hashtags in backend/src/api/content.py
- [ ] T035 POST /v1/sessions/{id}/regenerate endpoint: regenerate content with style options in backend/src/api/regenerate.py

### Middleware and Error Handling (T036-T038)
- [ ] T036 Rate limiting middleware: IP-based limits, OpenAI quota protection in backend/src/middleware/rate_limiter.py
- [ ] T037 CORS middleware: frontend origin, security headers in backend/src/middleware/cors.py
- [ ] T038 Global error handling: structured logging, error responses in backend/src/middleware/error_handler.py

### Frontend Core Components [P] (T039-T046)
- [ ] T039 [P] API client service: typed HTTP client, error handling in frontend/src/services/api-client.ts
- [ ] T040 [P] Image uploader component: drag-drop, progress bar, validation in frontend/src/components/ImageUploader.tsx
- [ ] T041 [P] Processing status component: progress animation, estimated time in frontend/src/components/ProcessingStatus.tsx
- [ ] T042 [P] Content display component: caption, hashtags, copy buttons in frontend/src/components/ContentDisplay.tsx
- [ ] T043 [P] Copyable text component: clipboard integration, success feedback in frontend/src/components/CopyableText.tsx
- [ ] T044 [P] Style selector component: regeneration options, loading states in frontend/src/components/StyleSelector.tsx
- [ ] T045 [P] Error display component: user-friendly messages, retry actions in frontend/src/components/ErrorDisplay.tsx
- [ ] T046 [P] Main application page: component orchestration, state management in frontend/src/pages/HomePage.tsx

### State Management and Routing (T047-T048)
- [ ] T047 React Context for application state: session, upload, content state in frontend/src/context/AppContext.tsx
- [ ] T048 Application routing and layout: responsive design, mobile optimization in frontend/src/App.tsx

## Phase 3.4: Integration (T049-T054)

### Backend Integration (T049-T052)
- [ ] T049 FastAPI application setup: route registration, middleware chain in backend/src/main.py
- [ ] T050 Database connection pooling: async connections, health checks in backend/src/database/pool.py
- [ ] T051 S3 bucket configuration: lifecycle policies, CORS settings in backend/src/storage/s3_config.py
- [ ] T052 Background job scheduler: session cleanup, file deletion in backend/src/jobs/scheduler.py

### Frontend Integration (T053-T054)
- [ ] T053 API client integration: environment configuration, base URLs in frontend/src/config/api.ts
- [ ] T054 Build configuration: TypeScript compilation, asset optimization in frontend/webpack.config.js and frontend/public/index.html

## Phase 3.5: Polish (T055-T060)

### Testing [P] (T055-T057)
- [ ] T055 [P] Backend unit tests: service layer, model validation in backend/tests/unit/test_services.py
- [ ] T056 [P] Frontend unit tests: component rendering, user interactions in frontend/tests/unit/components.test.tsx
- [ ] T057 [P] End-to-end tests: complete user workflows using Playwright in frontend/tests/e2e/user-workflows.spec.ts

### Documentation and Performance [P] (T058-T060)
- [ ] T058 [P] API documentation: OpenAPI spec serving, endpoint examples in backend/src/docs/openapi.py
- [ ] T059 [P] Performance optimization: image compression, lazy loading in frontend/src/utils/performance.ts and backend/src/utils/image_processing.py
- [ ] T060 [P] Production configuration: Docker containers, environment variables in Dockerfile and docker-compose.yml

---

## Dependencies

### Critical Path Dependencies
- **Setup (T001-T005)** before all other phases
- **Tests (T006-T016)** must FAIL before **Core Implementation (T017-T048)**
- **Database (T021-T022)** blocks all service tasks (T023-T030)
- **Services (T023-T030)** block **API Endpoints (T031-T035)**
- **API Client (T039)** blocks **Frontend Components (T040-T046)**
- **Core Implementation (T017-T048)** before **Integration (T049-T054)**
- **Integration (T049-T054)** before **Polish (T055-T060)**

### Specific Dependencies
- T021 blocks T023-T030 (services need database)
- T023-T030 block T031-T035 (endpoints need services)
- T039 blocks T040-T046 (components need API client)
- T031-T035 block T049 (app setup needs endpoints)
- T040-T046 block T047-T048 (state management needs components)

---

## Parallel Execution Examples

### Phase 1: Setup Tasks
```bash
# Launch T003-T005 together (different projects):
Task: "Initialize React frontend with TypeScript, TailwindCSS, Jest dependencies in frontend/package.json"
Task: "Configure backend linting: black, flake8, mypy in backend/pyproject.toml"
Task: "Configure frontend linting: ESLint, Prettier, TypeScript strict mode in frontend/.eslintrc.json and tsconfig.json"
```

### Phase 2: Contract Tests (Most Important Parallel Group)
```bash
# Launch T006-T010 together (different test files):
Task: "Contract test POST /v1/sessions in backend/tests/contract/test_sessions_post.py"
Task: "Contract test POST /v1/sessions/{id}/upload in backend/tests/contract/test_upload_post.py"
Task: "Contract test GET /v1/sessions/{id}/status in backend/tests/contract/test_status_get.py"
Task: "Contract test GET /v1/sessions/{id}/content in backend/tests/contract/test_content_get.py"
Task: "Contract test POST /v1/sessions/{id}/regenerate in backend/tests/contract/test_regenerate_post.py"
```

### Phase 3: Integration Tests
```bash
# Launch T011-T016 together (different integration scenarios):
Task: "Integration test complete happy path workflow in backend/tests/integration/test_happy_path.py"
Task: "Integration test content regeneration flow in backend/tests/integration/test_regeneration.py"
Task: "Integration test file validation and error handling in backend/tests/integration/test_validation.py"
Task: "Integration test content moderation and policy violations in backend/tests/integration/test_moderation.py"
Task: "Integration test session expiration and cleanup in backend/tests/integration/test_sessions.py"
Task: "Integration test concurrent user scaling in backend/tests/integration/test_performance.py"
```

### Phase 4: Data Models
```bash
# Launch T017-T020 together (different model files):
Task: "ProcessingSession model with UUID, timestamps, status enum in backend/src/models/session.py"
Task: "ImageUpload model with file metadata, S3 key, validation rules in backend/src/models/upload.py"
Task: "ImageAnalysis model with JSON fields for objects, colors, mood in backend/src/models/analysis.py"
Task: "GeneratedContent model with caption, hashtags, style enum in backend/src/models/content.py"
```

### Phase 5: Backend Services
```bash
# Launch T023-T030 together (different service files):
Task: "Session management service: create, retrieve, expire sessions in backend/src/services/session_service.py"
Task: "File upload service: S3 upload, validation, virus scanning in backend/src/services/upload_service.py"
Task: "OpenAI Vision API service: image analysis, error handling, rate limiting in backend/src/services/openai_service.py"
Task: "OpenRouter API service: alternative AI provider integration in backend/src/services/openrouter_service.py"
Task: "LM Studio service: local model inference integration in backend/src/services/lmstudio_service.py"
Task: "Content generation service: LLM failover cascade, hashtag validation in backend/src/services/content_service.py"
Task: "Content moderation service: policy violation detection in backend/src/services/moderation_service.py"
Task: "Background job service: async processing, session cleanup in backend/src/services/job_service.py"
```

### Phase 6: Frontend Components
```bash
# Launch T040-T046 together (different component files):
Task: "Image uploader component: drag-drop, progress bar, validation in frontend/src/components/ImageUploader.tsx"
Task: "Processing status component: progress animation, estimated time in frontend/src/components/ProcessingStatus.tsx"
Task: "Content display component: caption, hashtags, copy buttons in frontend/src/components/ContentDisplay.tsx"
Task: "Copyable text component: clipboard integration, success feedback in frontend/src/components/CopyableText.tsx"
Task: "Style selector component: regeneration options, loading states in frontend/src/components/StyleSelector.tsx"
Task: "Error display component: user-friendly messages, retry actions in frontend/src/components/ErrorDisplay.tsx"
Task: "Main application page: component orchestration, state management in frontend/src/pages/HomePage.tsx"
```

### Phase 7: Polish Tasks
```bash
# Launch T055-T060 together (different polish areas):
Task: "Backend unit tests: service layer, model validation in backend/tests/unit/test_services.py"
Task: "Frontend unit tests: component rendering, user interactions in frontend/tests/unit/components.test.tsx"
Task: "End-to-end tests: complete user workflows using Playwright in frontend/tests/e2e/user-workflows.spec.ts"
Task: "API documentation: OpenAPI spec serving, endpoint examples in backend/src/docs/openapi.py"
Task: "Performance optimization: image compression, lazy loading in frontend/src/utils/performance.ts and backend/src/utils/image_processing.py"
Task: "Production configuration: Docker containers, environment variables in Dockerfile and docker-compose.yml"
```

---

## Validation Checklist
*GATE: Checked before execution*

- [x] All contracts (5 endpoints) have corresponding tests (T006-T010)
- [x] All entities (4 models) have model tasks (T017-T020)
- [x] All tests (T006-T016) come before implementation (T017+)
- [x] Parallel tasks ([P]) truly independent (different files/no shared dependencies)
- [x] Each task specifies exact file path for implementation
- [x] No task modifies same file as another [P] task
- [x] TDD cycle enforced: RED (failing tests) before GREEN (implementation)
- [x] Core dependencies respected: DB → Services → Endpoints → Integration

## Task Generation Summary

**Total Tasks**: 60 numbered tasks (T001-T060)
**Parallel Tasks**: 38 tasks marked [P] for concurrent execution
**Critical Path**: Setup → Tests (must fail) → Models → Services → Endpoints → Integration → Polish
**Maximum Parallelism**: Up to 8 tasks can run concurrently in optimal phases

**Key Features Implemented**:
- ✅ 5 REST API endpoints with full OpenAPI spec
- ✅ 4 data models with PostgreSQL persistence
- ✅ AI service integration (OpenAI + OpenRouter + LM Studio)
- ✅ React frontend with TypeScript and TailwindCSS
- ✅ Comprehensive test coverage (contract, integration, unit, E2E)
- ✅ Production-ready configuration with Docker

**Constitutional Compliance**:
- ✅ Library-first architecture maintained
- ✅ Test-first development enforced
- ✅ Simplicity principles followed
- ✅ No unnecessary abstractions introduced

---

**Task Generation Status**: ✅ COMPLETE - Ready for execution via task runner or manual implementation

*Generated from Constitutional Planning System v2.1.1 - See `/memory/constitution.md`*