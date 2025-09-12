# Frontend - YouTube Channel Q&A

Next.js frontend for the YouTube Channel Q&A chatbot application.

## Quick Start

### Prerequisites
- Node.js 18+
- Yarn package manager
- Backend running on http://localhost:8000

### Development

```bash
# Install dependencies
yarn install

# Start development server
yarn dev

# Open http://localhost:3000
```

### Available Scripts

- `yarn dev` - Start development server
- `yarn build` - Build for production  
- `yarn start` - Start production server
- `yarn lint` - Run ESLint
- `yarn type-check` - Run TypeScript type checking

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_BACKEND_URL` | Backend API URL | `http://localhost:8000` |

## Project Structure

```
src/
├── app/
│   ├── channel/         # Channel URL input page
│   ├── loading/         # Loading/processing page
│   ├── chat/           # Q&A chat interface
│   ├── globals.css     # Global styles
│   └── layout.tsx      # Root layout
├── components/
│   └── ui/             # Reusable UI components
│       ├── button.tsx
│       ├── input.tsx
│       └── textarea.tsx
└── lib/
    ├── api.ts          # Backend API client
    └── utils.ts        # Utility functions
```

## Features

- **Channel Input**: YouTube channel URL validation and submission
- **Loading State**: Progress indicator during transcript processing
- **Chat Interface**: Question input with AI-powered responses
- **Transcript Preview**: Shows fetched transcripts for verification

## API Integration

The frontend communicates with the backend via `src/lib/api.ts`:

```typescript
// Fetch transcripts from YouTube channel
const transcripts = await fetchTranscripts(channelUrl)
```

## UI Components

Built with Radix UI primitives and TailwindCSS:

- **Button**: Various styles and sizes with loading states
- **Input**: Text input with validation
- **Textarea**: Multi-line text input for questions

## State Management

React hooks for state management:

- Channel URL persistence across screens
- Loading states and progress tracking
- Transcript storage and display
- Question/answer state management
