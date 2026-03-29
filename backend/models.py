from pydantic import BaseModel
from typing import Literal, Optional
from enum import Enum

class DataCategory(str, Enum):
    """Categories of data for the game"""
    CUSTOMER_REVIEW = "customer_review"
    PRODUCT_DESCRIPTION = "product_description"
    USER_PROFILE = "user_profile"
    CODE_SNIPPET = "code_snippet"

class DifficultyLevel(str, Enum):
    """Difficulty levels for the game"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class DataPair(BaseModel):
    """A pair of real and synthetic data for comparison"""
    id: str
    category: DataCategory
    difficulty: DifficultyLevel
    option_a: str
    option_b: str
    real_option: Literal["a", "b"]  # Which option is real
    synthetic_prompt: Optional[str] = None  # Prompt used to generate synthetic data

class GuessRequest(BaseModel):
    """User's guess for which data is real"""
    pair_id: str
    guessed_option: Literal["a", "b"]

class GuessResponse(BaseModel):
    """Response to user's guess"""
    correct: bool
    real_option: Literal["a", "b"]
    explanation: str
    score_delta: int

class GameSession(BaseModel):
    """Current game session state"""
    session_id: str
    score: int
    streak: int
    total_guesses: int
    correct_guesses: int
    difficulty: DifficultyLevel
    lives: int = 3  # Start with 3 lives

class LeaderboardEntry(BaseModel):
    """Leaderboard entry"""
    name: str
    score: int
    accuracy: float
    rank: Optional[int] = None
    date: Optional[str] = None
