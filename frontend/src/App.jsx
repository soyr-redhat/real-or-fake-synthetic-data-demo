import { useState, useEffect } from 'react'
import GameScreen from './components/GameScreen'
import StartScreen from './components/StartScreen'
import ResultsScreen from './components/ResultsScreen'
import Leaderboard from './components/Leaderboard'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [screen, setScreen] = useState('start') // start, game, results
  const [session, setSession] = useState(null)
  const [difficulty, setDifficulty] = useState('medium')
  const [currentPair, setCurrentPair] = useState(null)
  const [loading, setLoading] = useState(false)
  const [guessResult, setGuessResult] = useState(null)
  const [showLeaderboard, setShowLeaderboard] = useState(false)

  const startGame = async (selectedDifficulty) => {
    setLoading(true)
    try {
      const response = await fetch(`${API_URL}/session/start?difficulty=${selectedDifficulty}`, {
        method: 'POST'
      })
      const newSession = await response.json()
      setSession(newSession)
      setDifficulty(selectedDifficulty)
      setScreen('game')
      await loadNextPair(newSession.session_id, 'customer_review')
    } catch (error) {
      console.error('Failed to start game:', error)
      alert('Failed to start game. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const loadNextPair = async (sessionId, category) => {
    setLoading(true)
    setGuessResult(null)
    try {
      const response = await fetch(`${API_URL}/pair/generate?session_id=${sessionId}&category=${category}`, {
        method: 'POST'
      })
      const pair = await response.json()
      setCurrentPair(pair)
    } catch (error) {
      console.error('Failed to load pair:', error)
      alert('Failed to load data. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const submitGuess = async (option) => {
    if (!currentPair) return

    setLoading(true)
    try {
      const response = await fetch(`${API_URL}/guess`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pair_id: currentPair.id,
          guessed_option: option,
          session_id: session.session_id
        })
      })
      const result = await response.json()

      // Update session FIRST
      const sessionResponse = await fetch(`${API_URL}/session/${session.session_id}`)
      const updatedSession = await sessionResponse.json()
      setSession(updatedSession)

      // Set guess result AFTER session is updated
      setGuessResult(result)
    } catch (error) {
      console.error('Failed to submit guess:', error)
      alert('Failed to submit guess. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const continueToNext = async (category) => {
    // Don't load next pair if game is over
    if (session && session.lives > 0) {
      setGuessResult(null) // Clear guess result before loading next
      await loadNextPair(session.session_id, category)
    }
  }

  const endGame = () => {
    setScreen('results')
  }

  const restartGame = () => {
    setSession(null)
    setCurrentPair(null)
    setGuessResult(null)
    setScreen('start')
  }

  return (
    <div className="min-h-screen bg-redhat-dark-bg text-white">
      {/* Red Hat Brand Visual Elements */}
      <div className="grid-background"></div>

      {/* Header */}
      <header className="bg-redhat-dark-surface border-b border-redhat-grid-line relative z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="grid grid-cols-3 items-center gap-4">
            {/* Left: Title */}
            <div>
              <h1 className="text-3xl font-display font-bold text-redhat-red">Real or Fake?</h1>
              <p className="text-redhat-text-secondary mt-1 font-mono text-xs uppercase tracking-wider">Pillar 03 / Synthetic Data Generation Demo</p>
            </div>

            {/* Center: Session Stats */}
            {session && (
              <div className="flex justify-center">
                <div className="bg-redhat-dark-elevated rounded-lg px-6 py-3 flex items-center gap-4 border border-redhat-grid-line">
                  <div className="text-center">
                    <div className="text-redhat-red font-bold text-2xl font-mono">{session.score}</div>
                    <div className="text-xs text-gray-400">Score</div>
                  </div>
                  <div className="text-gray-600 font-bold text-xl">|</div>
                  <div className="text-center">
                    <div className="text-yellow-400 font-bold text-2xl font-mono">{session.streak}</div>
                    <div className="text-xs text-gray-400">Streak</div>
                  </div>
                  <div className="text-gray-600 font-bold text-xl">|</div>
                  <div className="text-center">
                    <div className="text-green-400 font-bold text-2xl font-mono">
                      {session.total_guesses > 0 ? Math.round((session.correct_guesses / session.total_guesses) * 100) : 0}%
                    </div>
                    <div className="text-xs text-gray-400">Accuracy</div>
                  </div>
                  <div className="text-gray-600 font-bold text-xl">|</div>
                  <div className="text-center">
                    <div className={`font-bold text-lg font-mono uppercase ${
                      session.difficulty === 'easy' ? 'text-green-400' :
                      session.difficulty === 'medium' ? 'text-yellow-400' :
                      'text-redhat-red'
                    }`}>
                      {session.difficulty === 'easy' ? '🟢' : session.difficulty === 'medium' ? '🟡' : '🔴'}
                    </div>
                    <div className="text-xs text-gray-400">{session.difficulty}</div>
                  </div>
                </div>
              </div>
            )}

            {/* Right: Powered by */}
            <div className="text-right">
              <div className="text-sm font-mono text-redhat-text-tertiary uppercase tracking-wider">Powered by</div>
              <div className="text-redhat-red font-display font-bold text-lg">Red Hat OpenShift AI</div>
            </div>
          </div>

          {/* Leaderboard Toggle */}
          <div className="mt-3 flex justify-end">
            <button
              onClick={() => setShowLeaderboard(!showLeaderboard)}
              className="px-4 py-2 bg-redhat-dark-elevated hover:bg-redhat-red border border-redhat-grid-line hover:border-redhat-red rounded font-mono text-xs uppercase tracking-wider transition"
            >
              {showLeaderboard ? 'Hide' : 'Show'} Leaderboard
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 relative z-10">
        {showLeaderboard && (
          <div className="mb-8">
            <Leaderboard apiUrl={API_URL} />
          </div>
        )}

        {screen === 'start' && (
          <StartScreen onStart={startGame} loading={loading} />
        )}

        {screen === 'game' && session && (
          <GameScreen
            session={session}
            currentPair={currentPair}
            guessResult={guessResult}
            loading={loading}
            onGuess={submitGuess}
            onContinue={continueToNext}
            onEndGame={endGame}
          />
        )}

        {screen === 'results' && session && (
          <ResultsScreen
            session={session}
            apiUrl={API_URL}
            onRestart={restartGame}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-redhat-dark-surface border-t border-redhat-grid-line mt-8 py-4 relative z-10">
        <div className="container mx-auto px-4 text-center font-mono text-redhat-text-tertiary text-xs uppercase tracking-wider">
          <p>Built with open source technologies | Red Hat AI - Four Pillars Demo</p>
        </div>
      </footer>
    </div>
  )
}

export default App
