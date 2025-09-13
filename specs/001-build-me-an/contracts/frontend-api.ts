// Frontend API Client Type Definitions
// Generated from OpenAPI spec for TypeScript integration

export interface SessionResponse {
  session_id: string;
  created_at: string;
  expires_at: string;
  upload_url: string;
}

export interface UploadResponse {
  upload_id: string;
  status: 'UPLOADING' | 'PROCESSING';
  estimated_completion?: string;
}

export interface StatusResponse {
  session_id: string;
  status: 'UPLOADING' | 'PROCESSING' | 'COMPLETED' | 'FAILED' | 'EXPIRED';
  progress: number; // 0-100
  estimated_completion?: string;
  error_message?: string;
}

export interface ImageAnalysis {
  objects_detected: string[];
  scene_description: string;
  style_tags: string[];
  mood: string;
  colors: string[]; // Hex color codes
}

export interface ContentResponse {
  content_id: string;
  caption: string;
  hashtags: string[];
  style: 'casual' | 'professional' | 'engaging' | 'funny';
  confidence: number; // 0.0-1.0
  generated_at: string;
  image_analysis: ImageAnalysis;
}

export interface RegenerateResponse {
  regeneration_id: string;
  status: 'PROCESSING';
  estimated_completion?: string;
}

export interface ErrorResponse {
  error: string;
  message: string;
  details?: Record<string, unknown>;
  timestamp: string;
}

export interface RegenerateRequest {
  style?: 'casual' | 'professional' | 'engaging' | 'funny';
}

// API Client Interface
export interface InstaTaleApiClient {
  // Session Management
  createSession(): Promise<SessionResponse>;

  // Image Upload
  uploadImage(sessionId: string, imageFile: File): Promise<UploadResponse>;

  // Status Monitoring
  getStatus(sessionId: string): Promise<StatusResponse>;

  // Content Retrieval
  getContent(sessionId: string): Promise<ContentResponse>;

  // Content Regeneration
  regenerateContent(sessionId: string, options?: RegenerateRequest): Promise<RegenerateResponse>;
}

// Frontend State Management Types
export interface ProcessingSession {
  sessionId: string;
  status: StatusResponse['status'];
  progress: number;
  createdAt: Date;
  expiresAt: Date;
  errorMessage?: string;
}

export interface UploadState {
  isUploading: boolean;
  uploadProgress: number;
  uploadId?: string;
}

export interface GeneratedContent {
  contentId: string;
  caption: string;
  hashtags: string[];
  style: ContentResponse['style'];
  confidence: number;
  generatedAt: Date;
  imageAnalysis: ImageAnalysis;
}

export interface AppState {
  session?: ProcessingSession;
  upload?: UploadState;
  content?: GeneratedContent;
  isRegenerating: boolean;
  error?: string;
}

// Component Props Interfaces
export interface ImageUploaderProps {
  onUpload: (file: File) => Promise<void>;
  isUploading: boolean;
  progress: number;
  error?: string;
}

export interface ProcessingStatusProps {
  status: StatusResponse['status'];
  progress: number;
  estimatedCompletion?: string;
  error?: string;
}

export interface ContentDisplayProps {
  content: GeneratedContent;
  onRegenerate: (style?: ContentResponse['style']) => Promise<void>;
  isRegenerating: boolean;
}

export interface CopyableTextProps {
  text: string;
  label: string;
  onCopy?: () => void;
}

// API Error Types
export class InstaTaleApiError extends Error {
  constructor(
    public readonly errorCode: string,
    public readonly details?: Record<string, unknown>,
    public readonly timestamp?: string
  ) {
    super(`InstaTale API Error: ${errorCode}`);
    this.name = 'InstaTaleApiError';
  }
}

export class SessionExpiredError extends InstaTaleApiError {
  constructor() {
    super('SESSION_EXPIRED', { reason: 'Session has exceeded 24-hour limit' });
  }
}

export class ProcessingFailedError extends InstaTaleApiError {
  constructor(details?: Record<string, unknown>) {
    super('PROCESSING_FAILED', details);
  }
}

export class RateLimitError extends InstaTaleApiError {
  constructor(retryAfter?: number) {
    super('RATE_LIMIT_EXCEEDED', { retry_after_seconds: retryAfter });
  }
}

// Validation Helpers
export const validateImageFile = (file: File): string | null => {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/heic', 'image/webp'];
  const maxSizeBytes = 50 * 1024 * 1024; // 50MB

  if (!allowedTypes.includes(file.type)) {
    return 'Please upload a JPEG, PNG, HEIC, or WebP image.';
  }

  if (file.size > maxSizeBytes) {
    return 'Image must be smaller than 50MB.';
  }

  return null;
};

export const validateHashtags = (hashtags: string[]): string | null => {
  if (hashtags.length < 10 || hashtags.length > 30) {
    return 'Must have between 10-30 hashtags.';
  }

  const hashtagPattern = /^#[a-zA-Z0-9_]+$/;
  const invalidHashtags = hashtags.filter(tag => !hashtagPattern.test(tag));

  if (invalidHashtags.length > 0) {
    return `Invalid hashtags: ${invalidHashtags.join(', ')}`;
  }

  return null;
};

// Constants
export const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8000/v1',
  TIMEOUT_MS: 30000,
  MAX_FILE_SIZE_MB: 50,
  SESSION_DURATION_HOURS: 24,
  POLLING_INTERVAL_MS: 2000,
} as const;

export const SUPPORTED_FILE_TYPES = [
  'image/jpeg',
  'image/png',
  'image/heic',
  'image/webp'
] as const;

export const CAPTION_STYLES = [
  'casual',
  'professional',
  'engaging',
  'funny'
] as const;