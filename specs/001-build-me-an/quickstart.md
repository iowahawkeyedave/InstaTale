# Quickstart Test Scenarios: AI Instagram Content Creator

**Feature**: 001-build-me-an | **Date**: 2025-09-12

## Overview

This document provides executable test scenarios to validate the AI Instagram Content Creator functionality. Each scenario maps directly to acceptance criteria from the feature specification and can be run manually or automated.

## Prerequisites

**Test Environment Setup**:
- Backend API running on `http://localhost:8000`
- Frontend application running on `http://localhost:3000`
- Test image files available in `/test-assets/`
- Valid OpenAI API key configured
- PostgreSQL database with test data

**Test Image Assets Required**:
- `beach-sunset.jpg` (10MB, landscape photo)
- `food-platter.png` (5MB, food photography)
- `portrait-person.heic` (15MB, portrait photo)
- `invalid-file.txt` (text file for negative testing)
- `oversized-image.jpg` (60MB, exceeds size limit)

---

## Scenario 1: Happy Path - Complete Content Generation

**User Story**: Content creator uploads a photo and receives AI-generated caption with hashtags

### Test Steps

1. **Create Session**
   ```bash
   curl -X POST http://localhost:8000/v1/sessions \
     -H "Content-Type: application/json"
   ```
   **Expected**: 201 Created with session_id, expires_at (24 hours future)

2. **Upload Valid Image**
   ```bash
   curl -X POST http://localhost:8000/v1/sessions/{session_id}/upload \
     -F "image=@test-assets/beach-sunset.jpg"
   ```
   **Expected**: 202 Accepted with upload_id, status=PROCESSING

3. **Poll Processing Status**
   ```bash
   # Repeat every 2 seconds until status=COMPLETED
   curl -X GET http://localhost:8000/v1/sessions/{session_id}/status
   ```
   **Expected**: Progress from 0→100%, status transitions UPLOADING→PROCESSING→COMPLETED
   **Timeout**: Must complete within 10 seconds

4. **Retrieve Generated Content**
   ```bash
   curl -X GET http://localhost:8000/v1/sessions/{session_id}/content
   ```
   **Expected**:
   - Caption text (50-300 characters)
   - 10-30 hashtags in format #word
   - Image analysis with objects, colors, mood
   - Confidence score 0.7-1.0

### Frontend UI Validation

1. **Visit** `http://localhost:3000`
2. **Upload** beach-sunset.jpg via drag-and-drop
3. **Observe** upload progress bar and processing animation
4. **Verify** content displays with copy-to-clipboard buttons
5. **Test** clipboard functionality works on caption and hashtags

**Success Criteria**:
- ✅ Complete flow takes <10 seconds
- ✅ Caption is contextually relevant to beach/sunset
- ✅ Hashtags include #beach, #sunset, #nature variations
- ✅ Copy buttons work on all browsers
- ✅ No errors in browser console

---

## Scenario 2: Content Regeneration

**User Story**: Content creator requests different caption styles for same image

### Prerequisites
- Complete Scenario 1 first to have processed image

### Test Steps

1. **Request Casual Style**
   ```bash
   curl -X POST http://localhost:8000/v1/sessions/{session_id}/regenerate \
     -H "Content-Type: application/json" \
     -d '{"style": "casual"}'
   ```
   **Expected**: 202 Accepted with regeneration_id

2. **Poll for New Content**
   ```bash
   curl -X GET http://localhost:8000/v1/sessions/{session_id}/content
   ```
   **Expected**: New caption with casual tone, same hashtag categories

3. **Request Professional Style**
   ```bash
   curl -X POST http://localhost:8000/v1/sessions/{session_id}/regenerate \
     -H "Content-Type: application/json" \
     -d '{"style": "professional"}'
   ```
   **Expected**: More formal caption tone

### Frontend Validation

1. **Click** "Regenerate" button with style selector
2. **Verify** loading state during regeneration
3. **Compare** different style outputs side-by-side
4. **Test** multiple regenerations (should work 5+ times)

**Success Criteria**:
- ✅ Caption tone changes appropriately per style
- ✅ Hashtags remain relevant but may vary
- ✅ Regeneration completes within 5 seconds
- ✅ Previous content accessible until new content loads

---

## Scenario 3: File Upload Validation

**User Story**: System validates uploaded files and provides clear error messages

### Test Steps

1. **Upload Unsupported Format**
   ```bash
   curl -X POST http://localhost:8000/v1/sessions/{session_id}/upload \
     -F "image=@test-assets/invalid-file.txt"
   ```
   **Expected**: 400 Bad Request with "Unsupported file format" message

2. **Upload Oversized File**
   ```bash
   curl -X POST http://localhost:8000/v1/sessions/{session_id}/upload \
     -F "image=@test-assets/oversized-image.jpg"
   ```
   **Expected**: 400 Bad Request with "File too large (max 50MB)" message

3. **Upload Corrupted Image**
   ```bash
   # Create corrupted file: truncate valid image
   head -c 100 test-assets/beach-sunset.jpg > corrupted.jpg
   curl -X POST http://localhost:8000/v1/sessions/{session_id}/upload \
     -F "image=@corrupted.jpg"
   ```
   **Expected**: 400 Bad Request with "Invalid image file" message

### Frontend Validation

1. **Drag** .txt file into upload area
2. **Verify** immediate error message before upload
3. **Try** pasting non-image from clipboard
4. **Test** browser file picker only shows image files

**Success Criteria**:
- ✅ Client-side validation prevents invalid uploads
- ✅ Server-side validation provides specific error messages
- ✅ Error messages are user-friendly, not technical
- ✅ Users can recover and try different files

---

## Scenario 4: Content Moderation

**User Story**: System refuses to generate content for inappropriate images

### Test Steps

1. **Upload Inappropriate Content**
   ```bash
   # Use test image flagged by content moderation
   curl -X POST http://localhost:8000/v1/sessions/{session_id}/upload \
     -F "image=@test-assets/inappropriate-content.jpg"
   ```
   **Expected**: Processing completes but content generation fails

2. **Check Status**
   ```bash
   curl -X GET http://localhost:8000/v1/sessions/{session_id}/status
   ```
   **Expected**: status=FAILED, error_message="Content policy violation"

3. **Attempt Content Retrieval**
   ```bash
   curl -X GET http://localhost:8000/v1/sessions/{session_id}/content
   ```
   **Expected**: 404 Not Found with policy violation explanation

### Frontend Validation

1. **Upload** inappropriate test image
2. **Observe** processing completes normally
3. **See** appropriate error message instead of content
4. **Verify** error doesn't expose technical details

**Success Criteria**:
- ✅ Content moderation works before caption generation
- ✅ Error messages explain policy without being judgmental
- ✅ Users can upload different image after policy violation
- ✅ No inappropriate content ever reaches users

---

## Scenario 5: Session Management

**User Story**: Sessions expire after 24 hours and handle concurrent access

### Test Steps

1. **Create Multiple Sessions**
   ```bash
   # Create 5 concurrent sessions
   for i in {1..5}; do
     curl -X POST http://localhost:8000/v1/sessions &
   done
   wait
   ```
   **Expected**: All sessions created successfully with unique IDs

2. **Use Expired Session** (simulated)
   ```bash
   # Mock expired session by setting database timestamp
   curl -X GET http://localhost:8000/v1/sessions/expired-session-id/status
   ```
   **Expected**: 404 Not Found with "Session expired" message

3. **Test Session Cleanup**
   ```bash
   # Verify old sessions are cleaned up (requires test helper)
   curl -X GET http://localhost:8000/v1/admin/cleanup-test
   ```
   **Expected**: Old sessions marked expired, files deleted from S3

### Frontend Validation

1. **Open** multiple browser tabs with different sessions
2. **Upload** images in parallel
3. **Verify** each session independent
4. **Test** browser refresh preserves session (if within 24h)

**Success Criteria**:
- ✅ Multiple concurrent sessions work without interference
- ✅ Expired sessions are handled gracefully
- ✅ Cleanup processes don't affect active sessions
- ✅ Frontend handles session expiration gracefully

---

## Scenario 6: Performance and Scale Testing

**User Story**: System handles expected load with acceptable performance

### Test Steps

1. **Load Test - Sequential**
   ```bash
   # Process 100 images sequentially
   for i in {1..100}; do
     echo "Processing image $i"
     ./scripts/single-upload-test.sh
   done
   ```
   **Expected**: Average processing time <10 seconds each

2. **Load Test - Concurrent**
   ```bash
   # Process 50 images concurrently (simulate viral traffic)
   for i in {1..50}; do
     ./scripts/single-upload-test.sh &
   done
   wait
   ```
   **Expected**: All complete within 30 seconds, no failures

3. **Rate Limiting Test**
   ```bash
   # Exceed rate limits
   for i in {1..1000}; do
     curl -X POST http://localhost:8000/v1/sessions &
   done
   ```
   **Expected**: Some 429 Rate Limit responses after threshold

### Monitoring Validation

1. **Check** database connection pool usage
2. **Monitor** OpenAI API quota consumption
3. **Verify** S3 upload bandwidth doesn't spike
4. **Review** error logs for any failures

**Success Criteria**:
- ✅ 95th percentile response time <10 seconds
- ✅ No database deadlocks or connection issues
- ✅ Rate limiting prevents quota exhaustion
- ✅ System recovers gracefully from high load

---

## Integration Test Automation

### Test Runner Script

```bash
#!/bin/bash
# run-quickstart-tests.sh

echo "Starting InstaTale Quickstart Tests..."

# Run scenarios in order
./tests/scenario-1-happy-path.sh
./tests/scenario-2-regeneration.sh
./tests/scenario-3-validation.sh
./tests/scenario-4-moderation.sh
./tests/scenario-5-sessions.sh
./tests/scenario-6-performance.sh

echo "All tests completed. Check logs for detailed results."
```

### Continuous Integration

```yaml
# .github/workflows/integration-tests.yml
name: Integration Tests
on: [push, pull_request]
jobs:
  quickstart-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v3
      - name: Run Quickstart Tests
        run: |
          ./scripts/setup-test-env.sh
          ./scripts/run-quickstart-tests.sh
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

## Success Metrics

**Functional Requirements**:
- ✅ All 6 scenarios pass without manual intervention
- ✅ Error handling works for all edge cases
- ✅ Content quality meets Instagram standards

**Performance Requirements**:
- ✅ 95th percentile processing time <10 seconds
- ✅ 1000+ concurrent sessions supported
- ✅ Zero data loss during normal operations

**User Experience Requirements**:
- ✅ Frontend responsive on mobile and desktop
- ✅ Copy-to-clipboard works across browsers
- ✅ Error messages help users resolve issues

---

**Test Status**: ⏳ READY FOR IMPLEMENTATION
**Dependencies**: Backend API, Frontend UI, Test image assets, CI/CD pipeline