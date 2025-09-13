# InstaTale 📸✨

> AI-powered Instagram content creation tool that transforms your photos into engaging captions and trending hashtags

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Development Status](https://img.shields.io/badge/Status-Planning%20Phase-blue.svg)](#development-status)
[![AI Integration](https://img.shields.io/badge/AI-OpenAI%20%7C%20OpenRouter%20%7C%20LM%20Studio-green.svg)](#ai-integration)

## 🚀 Overview

InstaTale helps content creators save time and boost engagement by automatically generating contextual Instagram captions and relevant hashtags from uploaded images. Using advanced AI vision and language models, it analyzes your photos and creates compelling content that resonates with your audience.

### ✨ Key Features

- **🖼️ Smart Image Analysis** - AI identifies objects, scenes, mood, and visual style
- **✍️ Dynamic Caption Generation** - Creates engaging captions in multiple styles (casual, professional, funny, engaging)
- **🏷️ Trending Hashtag Suggestions** - Generates 10-30 relevant hashtags for maximum discoverability
- **⚡ Fast Processing** - Results in under 10 seconds with real-time progress updates
- **🔄 Content Regeneration** - Multiple caption variations for the same image
- **📱 Responsive Design** - Works seamlessly on desktop and mobile devices
- **🔒 Privacy-First** - Images automatically deleted after 24 hours
- **📋 Easy Copy** - One-click copying to clipboard for Instagram posting

## 🏗️ Architecture

### Technology Stack

**Backend**:
- Python 3.11 with FastAPI
- PostgreSQL database with SQLAlchemy ORM
- S3-compatible storage for temporary images
- Redis for caching and rate limiting

**Frontend**:
- React 18 with TypeScript
- TailwindCSS for responsive design
- Progressive Web App (PWA) capabilities

**AI Integration** (3-tier failover):
1. **Primary**: OpenAI GPT-4 Vision + GPT-4
2. **Secondary**: OpenRouter (Claude, Llama, Gemini, etc.)
3. **Local**: LM Studio for privacy and cost control

### Project Structure

```
InstaTale/
├── README.md                    # This file
├── CLAUDE.md                    # AI assistant context
├── specs/001-build-me-an/       # Feature specification
│   ├── spec.md                  # Business requirements
│   ├── research.md              # Technical decisions
│   ├── data-model.md            # Database schema
│   ├── plan.md                  # Implementation plan
│   ├── quickstart.md            # Integration tests
│   └── contracts/               # API specifications
│       ├── api-spec.yaml        # OpenAPI 3.0 spec
│       └── frontend-api.ts      # TypeScript definitions
├── backend/                     # FastAPI backend (TBD)
├── frontend/                    # React frontend (TBD)
└── tests/                       # Test suites (TBD)
```

## 🎯 Development Status

### ✅ Completed Phases

- **Phase 0**: ✅ Research & Technical Decisions
- **Phase 1**: ✅ Feature Specification & API Design
- **Phase 2**: ✅ Implementation Planning (54 ordered tasks)

### 🚧 Current Phase

**Phase 3**: Task Generation - Ready for `/tasks` command to create detailed implementation roadmap

### 📋 Next Steps

1. Generate detailed task list with `/tasks` command
2. Set up development environment and dependencies
3. Implement backend API following TDD principles
4. Build React frontend with real-time processing UI
5. Deploy MVP for user testing and feedback

## 🛠️ Development Workflow

This project follows the **Specify** methodology with constitutional development principles:

- **📚 Library-First**: Every feature built as standalone, testable library
- **🧪 Test-Driven Development**: RED-GREEN-Refactor cycle enforced
- **🎯 Simplicity**: Maximum 3 projects, no unnecessary abstractions
- **🔍 Integration Testing**: Real dependencies, no mocking for contracts
- **📊 Observability**: Structured logging and error monitoring

### Commands

```bash
# Specify workflow commands
/specify "feature description"    # Create feature specification
/plan "additional context"        # Generate implementation plan
/tasks "context for tasks"        # Generate ordered task list

# Development commands (coming soon)
npm run dev                       # Start development servers
npm run test                      # Run test suites
npm run build                     # Build for production
```

## 🧠 AI Integration

### Supported Providers

| Provider | Purpose | Models | Failover Priority |
|----------|---------|--------|-------------------|
| **OpenAI** | Primary analysis & generation | GPT-4 Vision, GPT-4 | 1st |
| **OpenRouter** | Alternative model access | Claude, Llama, Gemini | 2nd |
| **LM Studio** | Local model hosting | Any compatible model | 3rd |

### Content Generation Process

1. **Image Upload** → Validation & preprocessing
2. **AI Analysis** → Object detection, scene understanding, mood analysis
3. **Content Generation** → Contextual captions and trending hashtags
4. **Quality Assurance** → Content moderation and validation
5. **User Delivery** → Copy-ready content with regeneration options

## 📖 Documentation

### For Developers
- [`CLAUDE.md`](./CLAUDE.md) - AI assistant context and commands
- [`specs/001-build-me-an/`](./specs/001-build-me-an/) - Complete feature specification
- [`specs/001-build-me-an/contracts/`](./specs/001-build-me-an/contracts/) - API documentation

### For Users
- [Quickstart Guide](./specs/001-build-me-an/quickstart.md) - Integration testing scenarios
- API Documentation - Available after implementation

## 🤝 Contributing

### Development Setup (Coming Soon)

```bash
# Clone repository
git clone https://github.com/iowahawkeyedave/InstaTale.git
cd InstaTale

# Backend setup
cd backend
pip install -r requirements.txt
python -m pytest  # Run backend tests

# Frontend setup
cd frontend
npm install
npm test          # Run frontend tests
npm start         # Start development server
```

### Contributing Guidelines

1. Follow constitutional development principles (library-first, TDD)
2. All features start with failing tests
3. Use conventional commit messages
4. Ensure 95th percentile response time <10 seconds
5. Maintain privacy-first data handling

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: https://github.com/iowahawkeyedave/InstaTale
- **Issues**: https://github.com/iowahawkeyedave/InstaTale/issues
- **Discussions**: https://github.com/iowahawkeyedave/InstaTale/discussions

## 📞 Support

For questions, bug reports, or feature requests:
- Open an [issue](https://github.com/iowahawkeyedave/InstaTale/issues)
- Start a [discussion](https://github.com/iowahawkeyedave/InstaTale/discussions)

---

**Built with ❤️ for content creators everywhere**

*InstaTale: Where your photos find their voice* ✨