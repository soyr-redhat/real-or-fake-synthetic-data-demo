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
          guessed_option: option
        })
      })
      const result = await response.json()
      setGuessResult(result)

      // Update session
      const sessionResponse = await fetch(`${API_URL}/session/${session.session_id}`)
      const updatedSession = await sessionResponse.json()
      setSession(updatedSession)
    } catch (error) {
      console.error('Failed to submit guess:', error)
      alert('Failed to submit guess. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const continueToNext = (category) => {
    loadNextPair(session.session_id, category)
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
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white">
      {/* Header */}
      <header className="bg-black bg-opacity-50 border-b border-red-900">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-redhat">Real or Fake?</h1>
            <p className="text-sm text-gray-400">Synthetic Data Generation Demo</p>
          </div>
          <button
            onClick={() => setShowLeaderboard(!showLeaderboard)}
            className="px-4 py-2 bg-redhat hover:bg-redhat-dark rounded-lg transition"
          >
            {showLeaderboard ? 'Hide' : 'Show'} Leaderboard
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
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
      <footer className="mt-12 py-6 border-t border-gray-800 text-center text-sm text-gray-500">
        <p>Powered by Red Hat OpenShift AI</p>
        <p className="mt-1">Built with open source - React, FastAPI, vLLM</p>
      </footer>
    </div>
  )
}

export default App
