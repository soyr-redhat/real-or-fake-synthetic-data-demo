import { useState, useEffect } from 'react'

const CATEGORIES = [
  { value: 'customer_review', label: 'Customer Review', icon: '⭐' },
  { value: 'product_description', label: 'Product Description', icon: '🏷️' },
  { value: 'user_profile', label: 'User Profile', icon: '👤' },
  { value: 'code_snippet', label: 'Code Snippet', icon: '💻' }
]

export default function GameScreen({ session, currentPair, guessResult, loading, onGuess, onContinue, onEndGame }) {
  const [categoryIndex, setCategoryIndex] = useState(0)
  const [showNotification, setShowNotification] = useState(false)
  const [notificationMessage, setNotificationMessage] = useState('')
  const [notificationType, setNotificationType] = useState('success') // success or error
  const [prevScore, setPrevScore] = useState(session.score)
  const [prevLives, setPrevLives] = useState(session.lives)
  const [scoreChanged, setScoreChanged] = useState(false)
  const [livesChanged, setLivesChanged] = useState(false)

  const categoryInfo = CATEGORIES.find(c => c.value === currentPair?.category) || CATEGORIES[categoryIndex]

  const accuracy = session.total_guesses > 0
    ? Math.round((session.correct_guesses / session.total_guesses) * 100)
    : 0

  // Detect stat changes for animation
  useEffect(() => {
    if (session.score !== prevScore) {
      setScoreChanged(true)
      setPrevScore(session.score)
      setTimeout(() => setScoreChanged(false), 400)
    }
    if (session.lives !== prevLives) {
      setLivesChanged(true)
      setPrevLives(session.lives)
      setTimeout(() => setLivesChanged(false), 400)
    }
  }, [session.score, session.lives])

  // Auto-advance after showing result
  useEffect(() => {
    if (guessResult) {
      // Show notification
      setNotificationMessage(guessResult.explanation)
      setNotificationType(guessResult.correct ? 'success' : 'error')
      setShowNotification(true)

      // Auto-advance or end game
      if (session.lives === 0) {
        const timeout = setTimeout(() => {
          console.log('Game over - navigating to results')
          onEndGame()
        }, 3000) // Give 3 seconds to see game over message
        return () => clearTimeout(timeout)
      } else {
        const timeout = setTimeout(() => {
          setShowNotification(false)
          onContinue(getNextCategory())
        }, 3000) // 3 seconds to see feedback and updated stats
        return () => clearTimeout(timeout)
      }
    }
  }, [guessResult, session.lives])

  // Get next category in cycle
  const getNextCategory = () => {
    const nextIndex = (categoryIndex + 1) % CATEGORIES.length
    setCategoryIndex(nextIndex)
    return CATEGORIES[nextIndex].value
  }

  return (
    <div className="max-w-6xl mx-auto relative">
      {/* Toast Notification */}
      {showNotification && (
        <div className={`fixed top-24 left-1/2 transform -translate-x-1/2 z-50 px-6 py-4 rounded-lg shadow-lg border-2 transition-all max-w-2xl ${
          notificationType === 'success'
            ? 'bg-green-900 bg-opacity-90 border-green-400 text-green-100'
            : 'bg-redhat-red bg-opacity-90 border-redhat-red text-white'
        }`}>
          <div className="flex items-center gap-3">
            <span className="text-2xl">{notificationType === 'success' ? '✓' : session.lives === 0 ? '💀' : '✗'}</span>
            <div className="flex-1">
              <p className="font-mono text-sm">{notificationMessage}</p>
              {session.lives === 0 && (
                <p className="font-display font-bold text-lg mt-2">Redirecting to results...</p>
              )}
            </div>
          </div>
        </div>
      )}
      {/* Stats Bar */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4 mb-8">
        <div className="bg-redhat-dark-elevated border border-redhat-grid-line rounded-lg p-4 text-center">
          <div className={`text-2xl font-mono font-bold text-redhat-red ${livesChanged ? 'stat-update' : ''}`}>
            {session.lives > 0 ? '❤️'.repeat(session.lives) : '💀'}
          </div>
          <div className="text-xs text-redhat-text-tertiary font-mono uppercase tracking-wider">Lives</div>
        </div>
        <div className="bg-redhat-dark-elevated border border-redhat-grid-line rounded-lg p-4 text-center">
          <div className={`text-2xl font-mono font-bold text-redhat-red ${scoreChanged ? 'stat-update' : ''}`}>{session.score}</div>
          <div className="text-xs text-redhat-text-tertiary font-mono uppercase tracking-wider">Score</div>
        </div>
        <div className="bg-redhat-dark-elevated border border-redhat-grid-line rounded-lg p-4 text-center">
          <div className="text-2xl font-mono font-bold text-yellow-400">{session.streak}</div>
          <div className="text-xs text-redhat-text-tertiary font-mono uppercase tracking-wider">Streak</div>
        </div>
        <div className="bg-redhat-dark-elevated border border-redhat-grid-line rounded-lg p-4 text-center">
          <div className="text-2xl font-mono font-bold text-green-400">{session.correct_guesses}</div>
          <div className="text-xs text-redhat-text-tertiary font-mono uppercase tracking-wider">Correct</div>
        </div>
        <div className="bg-redhat-dark-elevated border border-redhat-grid-line rounded-lg p-4 text-center">
          <div className="text-2xl font-mono font-bold text-blue-400">{session.total_guesses}</div>
          <div className="text-xs text-redhat-text-tertiary font-mono uppercase tracking-wider">Total</div>
        </div>
        <div className="bg-redhat-dark-elevated border border-redhat-grid-line rounded-lg p-4 text-center">
          <div className="text-2xl font-mono font-bold text-purple-400">{accuracy}%</div>
          <div className="text-xs text-redhat-text-tertiary font-mono uppercase tracking-wider">Accuracy</div>
        </div>
      </div>

      {/* Category Progress Indicator */}
      <div className="mb-6">
        <div className="flex items-center justify-center gap-3">
          {CATEGORIES.map((cat, idx) => (
            <div
              key={cat.value}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg border transition ${
                currentPair?.category === cat.value
                  ? 'bg-redhat-red border-redhat-red text-white scale-110'
                  : idx === categoryIndex && !currentPair
                  ? 'bg-redhat-red bg-opacity-20 border-redhat-red'
                  : 'bg-redhat-dark-elevated border-redhat-grid-line opacity-50'
              }`}
            >
              <span className="text-xl">{cat.icon}</span>
              <span className="text-xs font-mono hidden md:inline">{cat.label}</span>
            </div>
          ))}
        </div>
        <p className="text-center mt-3 text-redhat-text-tertiary font-mono text-xs uppercase tracking-wider">
          Categories cycle automatically • Current: {categoryInfo.label}
        </p>
      </div>

      {/* Main Comparison */}
      {currentPair && session.lives > 0 && (
        <div className="mb-6">
          <div className="text-center mb-6">
            <h2 className="text-3xl font-display font-bold mb-2 text-redhat-text-primary">
              {categoryInfo.icon} {categoryInfo.label}
            </h2>
            <p className="text-redhat-text-secondary font-mono uppercase tracking-wider">Which one is REAL?</p>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Option A */}
            <button
              onClick={() => !guessResult && !loading && onGuess('a')}
              disabled={loading || guessResult || session.lives === 0}
              className={`bg-redhat-dark-elevated border-2 p-6 rounded-lg text-left transition transform hover:scale-105 ${
                !guessResult && !loading ? 'hover:border-redhat-red cursor-pointer border-redhat-grid-line' : 'border-redhat-grid-line'
              } ${
                guessResult && guessResult.real_option === 'a'
                  ? 'ring-4 ring-green-400 border-green-400'
                  : guessResult && guessResult.real_option === 'b'
                  ? 'ring-4 ring-redhat-red border-redhat-red'
                  : ''
              }`}
            >
              <div className="flex justify-between items-start mb-3">
                <span className="text-2xl font-display font-bold text-redhat-red">Option A</span>
                {guessResult && guessResult.real_option === 'a' && (
                  <span className="text-green-500 text-xl">✓ REAL</span>
                )}
              </div>
              <div className={`${currentPair.category === 'code_snippet' ? 'font-mono text-sm' : ''}`}>
                {currentPair.option_a}
              </div>
            </button>

            {/* Option B */}
            <button
              onClick={() => !guessResult && !loading && onGuess('b')}
              disabled={loading || guessResult || session.lives === 0}
              className={`bg-redhat-dark-elevated border-2 p-6 rounded-lg text-left transition transform hover:scale-105 ${
                !guessResult && !loading ? 'hover:border-redhat-red cursor-pointer border-redhat-grid-line' : 'border-redhat-grid-line'
              } ${
                guessResult && guessResult.real_option === 'b'
                  ? 'ring-4 ring-green-400 border-green-400'
                  : guessResult && guessResult.real_option === 'a'
                  ? 'ring-4 ring-redhat-red border-redhat-red'
                  : ''
              }`}
            >
              <div className="flex justify-between items-start mb-3">
                <span className="text-2xl font-display font-bold text-redhat-red">Option B</span>
                {guessResult && guessResult.real_option === 'b' && (
                  <span className="text-green-500 text-xl">✓ REAL</span>
                )}
              </div>
              <div className={`${currentPair.category === 'code_snippet' ? 'font-mono text-sm' : ''}`}>
                {currentPair.option_b}
              </div>
            </button>
          </div>
        </div>
      )}


      {/* Game Over State */}
      {session.lives === 0 && !loading && (
        <div className="text-center py-12">
          <div className="bg-redhat-red bg-opacity-20 border-2 border-redhat-red rounded-lg p-8">
            <div className="text-6xl mb-4">💀</div>
            <h3 className="text-3xl font-display font-bold text-redhat-red mb-4">Game Over!</h3>
            <p className="text-redhat-text-secondary font-mono mb-6">
              You ran out of lives. Final Score: {session.score}
            </p>
            <button
              onClick={onEndGame}
              className="px-8 py-4 bg-redhat-red hover:bg-redhat-red-hover border border-redhat-red rounded-lg font-mono uppercase tracking-wider font-semibold text-lg transition"
            >
              View Results
            </button>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && !currentPair && session.lives > 0 && (
        <div className="text-center py-12">
          <div className="animate-spin inline-block w-12 h-12 border-4 border-redhat-red border-t-transparent rounded-full mb-4"></div>
          <p className="text-redhat-text-secondary font-mono">Generating data pair...</p>
        </div>
      )}
    </div>
  )
}
