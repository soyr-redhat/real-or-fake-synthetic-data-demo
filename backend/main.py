"""
Real or Fake - Synthetic Data Generation Demo
Version: 1.0.0
Last Updated: 2026-03-27
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from models import (
    DataPair, GuessRequest, GuessResponse, GameSession,
    LeaderboardEntry, DataCategory, DifficultyLevel
)
from data_generator import DataGenerator
from real_data import RealDataLibrary

app = FastAPI(title="Real or Fake - Synthetic Data Demo", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data sources
generator = DataGenerator()
real_data = RealDataLibrary()

# In-memory session storage (can be replaced with Redis in production)
active_sessions: Dict[str, GameSession] = {}
current_pairs: Dict[str, DataPair] = {}
pair_to_session: Dict[str, str] = {}  # Maps pair_id to session_id

# Leaderboard storage
LEADERBOARD_FILE = Path(os.getenv("LEADERBOARD_PATH", "./data/leaderboard.json"))
LEADERBOARD_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_leaderboard() -> List[Dict]:
    """Load leaderboard from file"""
    if not LEADERBOARD_FILE.exists():
        return []
    try:
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading leaderboard: {e}")
        return []

def save_leaderboard(entries: List[Dict]):
    """Save leaderboard to file"""
    try:
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(entries, f, indent=2)
    except Exception as e:
        print(f"Error saving leaderboard: {e}")

@app.get("/")
async def root():
    return {
        "service": "Real or Fake",
        "status": "running",
        "demo_type": "Synthetic Data Generation"
    }

@app.post("/session/start")
async def start_session(difficulty: DifficultyLevel = DifficultyLevel.MEDIUM):
    """Start a new game session"""
    session_id = str(uuid.uuid4())
    session = GameSession(
        session_id=session_id,
        score=0,
        streak=0,
        total_guesses=0,
        correct_guesses=0,
        difficulty=difficulty,
        lives=3
    )
    active_sessions[session_id] = session
    return session

@app.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get current session state"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return active_sessions[session_id]

@app.post("/pair/generate")
async def generate_pair(session_id: str, category: DataCategory):
    """Generate a new data pair for comparison"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = active_sessions[session_id]

    # Get real data sample
    real_sample = real_data.get_sample(category, session.difficulty)

    # Generate synthetic data
    synthetic_sample = await generator.generate_synthetic(category, session.difficulty, real_sample)

    # Randomly assign to option a or b
    import random
    real_is_a = random.choice([True, False])

    pair = DataPair(
        id=str(uuid.uuid4()),
        category=category,
        difficulty=session.difficulty,
        option_a=real_sample if real_is_a else synthetic_sample,
        option_b=synthetic_sample if real_is_a else real_sample,
        real_option="a" if real_is_a else "b",
        synthetic_prompt=generator.last_prompt
    )

    current_pairs[pair.id] = pair
    pair_to_session[pair.id] = session_id  # Track which session owns this pair

    # Return pair without revealing the answer
    return {
        "id": pair.id,
        "category": pair.category,
        "difficulty": pair.difficulty,
        "option_a": pair.option_a,
        "option_b": pair.option_b
    }

@app.post("/guess")
async def submit_guess(guess: GuessRequest):
    """Submit a guess and get feedback"""
    if guess.pair_id not in current_pairs:
        raise HTTPException(status_code=404, detail="Data pair not found")

    pair = current_pairs[guess.pair_id]

    # Get the session that owns this pair
    session_id = pair_to_session.get(guess.pair_id) or guess.session_id
    if not session_id or session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = active_sessions[session_id]

    correct = guess.guessed_option == pair.real_option

    # Update session stats
    session.total_guesses += 1
    if correct:
        session.correct_guesses += 1
        session.streak += 1
        # Base points + streak bonus
        points = 10 + (session.streak * 2)
        session.score += points
        score_delta = points
    else:
        session.streak = 0
        session.lives -= 1  # Lose a life on wrong answer
        score_delta = 0

    # Auto-increase difficulty based on score
    difficulty_increased = False
    old_difficulty = session.difficulty
    if session.difficulty == DifficultyLevel.EASY and session.score >= 50:
        session.difficulty = DifficultyLevel.MEDIUM
        difficulty_increased = True
    elif session.difficulty == DifficultyLevel.MEDIUM and session.score >= 150:
        session.difficulty = DifficultyLevel.HARD
        difficulty_increased = True

    # Generate explanation
    explanation = f"The real {pair.category.value} was option {pair.real_option.upper()}. "
    if correct:
        explanation += f"Great job! You earned {score_delta} points (streak bonus: {session.streak}x)."
        if difficulty_increased:
            explanation += f" 🎉 DIFFICULTY INCREASED to {session.difficulty.value.upper()}!"
    else:
        explanation += f"Better luck next time! Your streak has been reset. Lives remaining: {session.lives}"
        if session.lives == 0:
            explanation += " - GAME OVER!"

    response = GuessResponse(
        correct=correct,
        real_option=pair.real_option,
        explanation=explanation,
        score_delta=score_delta
    )

    return response

@app.get("/pair/{pair_id}/reveal")
async def reveal_generation(pair_id: str):
    """Reveal how the synthetic data was generated"""
    if pair_id not in current_pairs:
        raise HTTPException(status_code=404, detail="Data pair not found")

    pair = current_pairs[pair_id]

    return {
        "category": pair.category,
        "difficulty": pair.difficulty,
        "real_option": pair.real_option,
        "synthetic_prompt": pair.synthetic_prompt,
        "generation_technique": "LLM-based text generation using prompt engineering",
        "quality_metrics": {
            "diversity": "High - uses temperature sampling",
            "realism": f"{pair.difficulty.value.capitalize()} - adjusted by prompt complexity",
            "privacy": "Complete - no real user data used in generation"
        }
    }

@app.get("/leaderboard")
async def get_leaderboard(limit: int = 50):
    """Get top entries from the leaderboard"""
    entries = load_leaderboard()
    entries.sort(key=lambda x: x.get('score', 0), reverse=True)
    return {"leaderboard": entries[:limit]}

@app.post("/leaderboard")
async def post_to_leaderboard(entry: LeaderboardEntry):
    """Submit a score to the leaderboard"""
    entries = load_leaderboard()

    entry_dict = entry.model_dump()
    entry_dict['date'] = datetime.utcnow().isoformat()

    entries.append(entry_dict)

    # Keep only top 1000
    entries.sort(key=lambda x: x.get('score', 0), reverse=True)
    entries = entries[:1000]

    save_leaderboard(entries)

    return {"success": True, "rank": entries.index(entry_dict) + 1}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
