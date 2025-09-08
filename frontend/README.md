# YouTube Channel Q&A - Frontend

A Next.js frontend for the YouTube Channel Q&A chatbot application.

## Getting Started

### Prerequisites

- Node.js 18+ 
- Yarn package manager

### Installation

1. Install dependencies:
```bash
yarn install
```

2. Run the development server:
```bash
yarn dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Available Scripts

- `yarn dev` - Start development server
- `yarn build` - Build for production
- `yarn start` - Start production server
- `yarn lint` - Run ESLint
- `yarn type-check` - Run TypeScript type checking

## Project Structure

```
src/
├── app/
│   ├── globals.css      # Global styles
│   ├── layout.tsx       # Root layout
│   └── page.tsx         # Main page component
├── components/
│   └── ui/              # Reusable UI components
│       ├── button.tsx
│       ├── input.tsx
│       └── textarea.tsx
└── lib/
    └── utils.ts         # Utility functions
```

## UI Components

The app uses custom UI components built on top of Radix UI primitives:

- **Button**: Various button styles and sizes
- **Input**: Text input with consistent styling
- **Textarea**: Multi-line text input

## State Management

The app uses React's built-in `useState` hook for simple state management across the three screens:

- `currentScreen`: Tracks which screen to display
- `channelUrl`: Stores the YouTube channel URL
- `question`: Stores the user's question
- `answer`: Stores the chatbot's response

## Next Steps

This frontend skeleton will be connected to the backend API in subsequent steps to enable real transcript fetching and AI-powered question answering.
