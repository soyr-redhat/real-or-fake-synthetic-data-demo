# Real or Fake? - Synthetic Data Generation Demo

An interactive game demonstrating synthetic data generation capabilities through a detective-style challenge.

## Concept

Test your ability to distinguish between real and AI-generated data. Choose a difficulty level and see how well you can detect synthetic content across different data types: customer reviews, product descriptions, user profiles, and code snippets.

## Features

- **Multiple Data Categories**: Customer reviews, product descriptions, user profiles, and code snippets
- **Three Difficulty Levels**: Easy (obvious fakes), Medium (realistic), Hard (nearly indistinguishable)
- **Real-time Scoring**: Points, streaks, and accuracy tracking
- **Educational Reveal**: Learn how synthetic data was generated after each guess
- **Leaderboard**: Compete with other players
- **Quality Metrics**: See diversity, realism, and privacy aspects of synthetic data

## Architecture

- **Frontend**: React + Vite + Tailwind CSS (nginx-unprivileged)
- **Backend**: Python FastAPI + LLM integration (Mistral-Small-24B-W8A8)
- **Deployment**: OpenShift with automated CI/CD
- **CI/CD**: GitHub Actions + OpenShift BuildConfig webhooks

## Quick Start

The application is deployed at: **https://red.ht/real-or-fake** _(placeholder URL)_

## Automated Deployment

Push to `main` branch automatically triggers:
1. OpenShift builds via GitHub webhooks
2. GitHub Actions workflow orchestration
3. Automatic pod rollout with new images
4. Cleanup of old builds (keeps last 3)

See [DEPLOYMENT.md](DEPLOYMENT.md) for setup details.

## Local Development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
export LLM_API_URL="https://litellm-litemaas.apps.prod.rhoai.rh-aiservices-bu.com/v1"
export LLM_API_KEY="your-api-key"
export MODEL_NAME="Mistral-Small-24B-W8A8"
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

### Backend
- `LLM_API_URL` - LLM API endpoint URL
- `LLM_API_KEY` - LLM API authentication token
- `MODEL_NAME` - Model to use for synthetic data generation (default: Mistral-Small-24B-W8A8)
- `LEADERBOARD_PATH` - Path to store leaderboard data (default: ./data/leaderboard.json)

### Frontend
- `VITE_API_URL` - Backend API URL (set during build)

## How It Works

### Synthetic Data Generation

The demo uses prompt engineering with an LLM to generate synthetic data that mimics real examples:

1. **Easy Mode**: Low temperature (0.3), simple prompts → obvious AI patterns
2. **Medium Mode**: Medium temperature (0.7), style-matching prompts → realistic outputs
3. **Hard Mode**: High temperature (0.9), sophisticated prompts → nearly indistinguishable

### Game Mechanics

- **Base Points**: 10 points per correct guess
- **Streak Bonus**: +2 points per consecutive correct answer
- **Accuracy Tracking**: Live statistics on detection success rate
- **Educational Mode**: Reveals generation technique and quality metrics

## Data Categories

### Customer Reviews
Real data includes authentic user-written reviews with natural language quirks, typos, and informal tone. Synthetic versions are generated to match style complexity based on difficulty.

### Product Descriptions
Real marketing copy vs. AI-generated product descriptions. Higher difficulties include specific details and authentic marketing language.

### User Profiles
Actual social media bios vs. generated personas. Hard mode includes personality quirks and authentic voice.

### Code Snippets
Production code samples vs. AI-generated functions. Difficulty affects variable naming, edge cases, and coding patterns.

## Technical Highlights

- **Adaptive Temperature**: Adjusts LLM creativity based on difficulty
- **Prompt Engineering**: Sophisticated prompts for realistic generation
- **Fallback Generation**: Graceful degradation if LLM unavailable
- **Persistent Leaderboard**: PVC-backed score storage
- **Real-time Updates**: Instant feedback and scoring

## Contributing

This demo is part of the Four Pillars of AI initiative. For issues or improvements, please contribute to the main repository.

## License

Built with open source technologies - React, FastAPI, vLLM. Powered by Red Hat OpenShift AI.
