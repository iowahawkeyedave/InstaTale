# Data Model: AI-Powered Instagram Content Creator

**Feature**: 001-build-me-an | **Date**: 2025-09-12

## Core Entities

### ProcessingSession
Represents a user's image processing session with generated content.

**Fields**:
- `session_id` (UUID, Primary Key): Unique identifier for the session
- `created_at` (DateTime): When session was created
- `expires_at` (DateTime): When session expires (24 hours from creation)
- `status` (Enum): Current processing status
- `error_message` (String, Optional): Error details if processing failed

**Status Values**:
- `UPLOADING`: Image being uploaded
- `PROCESSING`: AI analysis in progress
- `COMPLETED`: Caption and hashtags generated
- `FAILED`: Processing failed
- `EXPIRED`: Session past 24-hour limit

**Relationships**:
- One-to-one with ImageUpload
- One-to-many with GeneratedContent (allows regeneration)

### ImageUpload
Represents the uploaded image file and metadata.

**Fields**:
- `upload_id` (UUID, Primary Key): Unique identifier for upload
- `session_id` (UUID, Foreign Key): Links to ProcessingSession
- `original_filename` (String): User's original filename
- `file_size_bytes` (Integer): Size of uploaded file
- `content_type` (String): MIME type (image/jpeg, image/png, etc.)
- `s3_key` (String): Storage location identifier
- `uploaded_at` (DateTime): Upload timestamp
- `analyzed_at` (DateTime, Optional): When AI analysis completed

**Validation Rules**:
- `file_size_bytes` <= 50MB (52,428,800 bytes)
- `content_type` in ['image/jpeg', 'image/png', 'image/heic', 'image/webp']
- `s3_key` follows pattern: `uploads/{session_id}/{upload_id}.{ext}`

**Relationships**:
- Belongs to ProcessingSession
- One-to-one with ImageAnalysis

### ImageAnalysis
Stores AI-generated analysis of the uploaded image.

**Fields**:
- `analysis_id` (UUID, Primary Key): Unique identifier
- `upload_id` (UUID, Foreign Key): Links to ImageUpload
- `objects_detected` (JSON Array): List of objects/subjects identified
- `scene_description` (Text): Overall scene description
- `style_tags` (JSON Array): Visual style characteristics
- `mood_analysis` (String): Emotional tone of image
- `color_palette` (JSON Array): Dominant colors identified
- `content_warnings` (JSON Array): Any moderation flags
- `ai_confidence` (Float): Confidence score 0.0-1.0
- `processing_duration_ms` (Integer): Time taken for analysis

**JSON Schema Examples**:
```json
{
  "objects_detected": ["person", "beach", "sunset", "ocean"],
  "style_tags": ["golden_hour", "natural_lighting", "portrait"],
  "color_palette": ["#FF6B35", "#F7941D", "#FFD23F", "#06D6A0"],
  "content_warnings": []
}
```

**Relationships**:
- Belongs to ImageUpload
- One-to-many with GeneratedContent

### GeneratedContent
Stores AI-generated captions and hashtags for an image.

**Fields**:
- `content_id` (UUID, Primary Key): Unique identifier
- `analysis_id` (UUID, Foreign Key): Links to ImageAnalysis
- `session_id` (UUID, Foreign Key): Links to ProcessingSession
- `caption_text` (Text): Generated Instagram caption
- `hashtags` (JSON Array): Array of hashtag strings
- `style_applied` (String): Caption style used (engaging, professional, casual)
- `generation_prompt` (Text): Prompt sent to AI for generation
- `ai_model_used` (String): AI model identifier
- `generated_at` (DateTime): Generation timestamp
- `is_active` (Boolean): Whether this is current content for session

**Validation Rules**:
- `caption_text` length <= 2200 characters (Instagram limit)
- `hashtags` array length between 10-30 items
- Each hashtag matches Instagram format: alphanumeric + underscores only

**JSON Schema Example**:
```json
{
  "hashtags": [
    "#sunset", "#beach", "#goldenhour", "#portrait",
    "#ocean", "#peaceful", "#naturallight", "#photography",
    "#instadaily", "#beautiful", "#nature", "#coastline"
  ]
}
```

**Relationships**:
- Belongs to ImageAnalysis and ProcessingSession

## Entity Relationships

```
ProcessingSession (1) ←→ (1) ImageUpload
ImageUpload (1) ←→ (1) ImageAnalysis
ImageAnalysis (1) ←→ (many) GeneratedContent
ProcessingSession (1) ←→ (many) GeneratedContent
```

## Data Flow States

1. **Session Creation**: User starts upload → ProcessingSession created
2. **Image Upload**: File uploaded → ImageUpload created, status = UPLOADING
3. **AI Analysis**: Image sent to AI → ImageAnalysis created, status = PROCESSING
4. **Content Generation**: Analysis used for captions → GeneratedContent created, status = COMPLETED
5. **Regeneration**: User requests new content → Additional GeneratedContent created
6. **Expiration**: After 24 hours → Session marked EXPIRED, files cleaned up

## Storage Considerations

**Database Storage** (PostgreSQL):
- Session metadata and relationships
- Generated text content
- Image analysis results
- Processing logs and metrics

**Object Storage** (S3-compatible):
- Original uploaded images (temporary, 24-hour retention)
- Processed/resized images for analysis
- Automatic cleanup via lifecycle policies

**Caching Layer** (Redis):
- Active session data
- Rate limiting counters
- AI API response caching for identical images

## Privacy and Cleanup

**Automatic Cleanup**:
- Images deleted from S3 after 24 hours via lifecycle policy
- Database sessions marked as EXPIRED but metadata retained for analytics
- Personal identifiers scrubbed from expired sessions

**Privacy Controls**:
- No permanent image storage
- No user tracking across sessions
- Optional analytics only on aggregated, anonymized data

## Performance Optimizations

**Database Indexes**:
- `ProcessingSession.session_id` (Primary Key)
- `ProcessingSession.created_at` (for cleanup queries)
- `ProcessingSession.status` (for monitoring)
- `ImageUpload.session_id` (Foreign Key)
- `GeneratedContent.session_id, is_active` (for retrieval)

**Partitioning Strategy**:
- Partition ProcessingSession by creation date (monthly)
- Enables efficient cleanup of old data
- Improves query performance for active sessions