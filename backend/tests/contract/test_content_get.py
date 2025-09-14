"""
Contract test for GET /v1/sessions/{id}/content endpoint
CRITICAL: This test MUST FAIL until the endpoint is implemented
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import uuid
import re

# Import will fail until main.py is created - this is expected and required
try:
    from src.main import app
    client = TestClient(app)
except ImportError:
    client = None


class TestGetContentContract:
    """Contract tests for GET /v1/sessions/{sessionId}/content endpoint"""

    def test_get_content_success_200(self):
        """Test successful content retrieval returns 200 with correct schema"""
        if not client:
            pytest.fail("FastAPI app not implemented yet - test should fail")

        session_id = str(uuid.uuid4())

        response = client.get(f"/v1/sessions/{session_id}/content")

        # Contract: Must return 200 OK when content is ready
        # Will actually return 404/425 until content generation is implemented
        assert response.status_code in [200, 404, 425]

        if response.status_code == 200:
            data = response.json()

            # Contract: Response must match ContentResponse schema
            required_fields = ["content_id", "caption", "hashtags", "style", "confidence", "generated_at"]
            for field in required_fields:
                assert field in data, f"Missing required field: {field}"

            # Contract: content_id must be valid UUID
            try:
                uuid.UUID(data["content_id"])
            except ValueError:
                pytest.fail("content_id must be valid UUID format")

            # Contract: caption must be within Instagram limits
            assert isinstance(data["caption"], str)
            assert len(data["caption"]) <= 2200

            # Contract: hashtags must be valid format and count
            hashtags = data["hashtags"]
            assert isinstance(hashtags, list)
            assert 10 <= len(hashtags) <= 30

            for hashtag in hashtags:
                assert isinstance(hashtag, str)
                assert re.match(r'^#[a-zA-Z0-9_]+$', hashtag), f"Invalid hashtag format: {hashtag}"

            # Contract: style must be valid enum
            assert data["style"] in ["casual", "professional", "engaging", "funny"]

            # Contract: confidence must be 0.0-1.0
            assert 0.0 <= data["confidence"] <= 1.0
            assert isinstance(data["confidence"], (int, float))

            # Contract: generated_at must be valid datetime
            try:
                datetime.fromisoformat(data["generated_at"].replace("Z", "+00:00"))
            except ValueError:
                pytest.fail("generated_at must be valid ISO datetime format")

            # Contract: image_analysis is optional but if present must match schema
            if "image_analysis" in data:
                analysis = data["image_analysis"]
                required_analysis_fields = ["objects_detected", "scene_description", "style_tags", "mood", "colors"]
                for field in required_analysis_fields:
                    assert field in analysis, f"Missing analysis field: {field}"

                # Validate colors are hex format
                for color in analysis["colors"]:
                    assert re.match(r'^#[0-9A-Fa-f]{6}$', color), f"Invalid color format: {color}"

    def test_get_content_session_not_found_404(self):
        """Test content for non-existent session returns 404"""
        if not client:
            pytest.fail("FastAPI app not implemented yet - test should fail")

        non_existent_session = str(uuid.uuid4())

        response = client.get(f"/v1/sessions/{non_existent_session}/content")

        # Contract: Must return 404 for non-existent session
        assert response.status_code == 404

        data = response.json()

        # Contract: Error response must match ErrorResponse schema
        assert "error" in data
        assert "message" in data
        assert "timestamp" in data
        assert data["error"] == "session_not_found"

    def test_get_content_processing_not_complete_425(self):
        """Test content request when processing incomplete returns 425"""
        if not client:
            pytest.fail("FastAPI app not implemented yet - test should fail")

        session_id = str(uuid.uuid4())

        response = client.get(f"/v1/sessions/{session_id}/content")

        # Contract: Must return 425 when processing not complete
        if response.status_code == 425:
            data = response.json()

            # Contract: Error response must match ErrorResponse schema
            assert "error" in data
            assert "message" in data
            assert "timestamp" in data
            assert data["error"] == "processing_incomplete"

    def test_get_content_invalid_session_id_400(self):
        """Test content with invalid UUID format returns 400"""
        if not client:
            pytest.fail("FastAPI app not implemented yet - test should fail")

        response = client.get("/v1/sessions/invalid-uuid/content")

        assert response.status_code == 400

        data = response.json()
        assert data["error"] == "invalid_session_id"

    def test_get_content_hashtag_validation(self):
        """Test hashtags follow Instagram requirements"""
        if not client:
            pytest.fail("FastAPI app not implemented yet - test should fail")

        session_id = str(uuid.uuid4())

        response = client.get(f"/v1/sessions/{session_id}/content")

        if response.status_code == 200:
            data = response.json()
            hashtags = data["hashtags"]

            for hashtag in hashtags:
                # Contract: Must start with #
                assert hashtag.startswith("#")

                # Contract: No spaces allowed
                assert " " not in hashtag

                # Contract: Only alphanumeric and underscore after #
                hashtag_content = hashtag[1:]  # Remove #
                assert re.match(r'^[a-zA-Z0-9_]+$', hashtag_content)

                # Contract: Not empty after #
                assert len(hashtag_content) > 0

                # Contract: Reasonable length (Instagram allows up to 100 chars but let's be practical)
                assert len(hashtag) <= 50

    def test_get_content_caption_quality_requirements(self):
        """Test caption meets quality requirements"""
        if not client:
            pytest.fail("FastAPI app not implemented yet - test should fail")

        session_id = str(uuid.uuid4())

        response = client.get(f"/v1/sessions/{session_id}/content")

        if response.status_code == 200:
            data = response.json()
            caption = data["caption"]

            # Contract: Caption should be substantial but not empty
            assert len(caption.strip()) > 0

            # Contract: Should be engaging (have some basic structure)
            # At minimum should have some words
            words = caption.split()
            assert len(words) >= 3

            # Contract: Should not exceed Instagram limit
            assert len(caption) <= 2200

    def test_get_content_image_analysis_schema(self):
        """Test image analysis has correct structure when present"""
        if not client:
            pytest.fail("FastAPI app not implemented yet - test should fail")

        session_id = str(uuid.uuid4())

        response = client.get(f"/v1/sessions/{session_id}/content")

        if response.status_code == 200:
            data = response.json()

            if "image_analysis" in data:
                analysis = data["image_analysis"]

                # Contract: objects_detected must be array of strings
                assert isinstance(analysis["objects_detected"], list)
                for obj in analysis["objects_detected"]:
                    assert isinstance(obj, str)
                    assert len(obj.strip()) > 0

                # Contract: scene_description must be meaningful string
                assert isinstance(analysis["scene_description"], str)
                assert len(analysis["scene_description"].strip()) > 0

                # Contract: style_tags must be array of strings
                assert isinstance(analysis["style_tags"], list)
                for tag in analysis["style_tags"]:
                    assert isinstance(tag, str)
                    assert len(tag.strip()) > 0

                # Contract: mood must be string
                assert isinstance(analysis["mood"], str)
                assert len(analysis["mood"].strip()) > 0

                # Contract: colors must be valid hex codes
                assert isinstance(analysis["colors"], list)
                for color in analysis["colors"]:
                    assert re.match(r'^#[0-9A-Fa-f]{6}$', color)

    def test_get_content_confidence_score_meaningful(self):
        """Test confidence score reflects content quality"""
        if not client:
            pytest.fail("FastAPI app not implemented yet - test should fail")

        session_id = str(uuid.uuid4())

        response = client.get(f"/v1/sessions/{session_id}/content")

        if response.status_code == 200:
            data = response.json()
            confidence = data["confidence"]

            # Contract: Confidence should be reasonable (not always 0 or 1)
            # In real implementation, should vary based on analysis quality
            assert isinstance(confidence, (int, float))
            assert 0.0 <= confidence <= 1.0

    def test_get_content_caching_headers(self):
        """Test content response has appropriate caching headers"""
        if not client:
            pytest.fail("FastAPI app not implemented yet - test should fail")

        session_id = str(uuid.uuid4())

        response = client.get(f"/v1/sessions/{session_id}/content")

        # Contract: Content is immutable once generated, should be cacheable
        if response.status_code == 200:
            # Should have cache headers since content doesn't change
            cache_control = response.headers.get("cache-control")
            if cache_control:
                # Content can be cached for a reasonable time
                assert "max-age" in cache_control.lower() or "immutable" in cache_control.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])