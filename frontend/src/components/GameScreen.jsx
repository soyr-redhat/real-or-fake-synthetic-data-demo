import { useState } from 'react'

const CATEGORIES = [
  { value: 'customer_review', label: 'Customer Review', icon: '⭐' },
  { value: 'product_description', label: 'Product Description', icon: '🏷️' },
  { value: 'user_profile', label: 'User Profile', icon: '👤' },
  { value: 'code_snippet', label: 'Code Snippet', icon: '💻' }
]

export default function GameScreen({ session, currentPair, guessResult, loading, onGuess, onContinue, onEndGame }) {
  const [selectedCategory, setSelectedCategory] = useState('customer_review')

  const categoryInfo = CATEGORIES.find(c => c.value === currentPair?.category) || CATEGORIES[0]

  const accuracy = session.total_guesses > 0
    ? Math.round((session.correct_guesses / session.total_guesses) * 100)
    : 0

  return (
    <div className="max-w-6xl mx-auto">
      {/* Stats Bar */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
        <div className="bg-redhat-dark-elevated border border-redhat-grid-line rounded-lg p-4 text-center">
          <div className="text-2xl font-mono font-bold text-redhat-red">{session.score}</div>
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

      {/* Category Selector */}
      {!guessResult && (
        <div className="mb-6">
          <h3 className="text-lg font-display font-semibold mb-3 text-redhat-red">Select Category:</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {CATEGORIES.map(cat => (
              <button
                key={cat.value}
                onClick={() => setSelectedCategory(cat.value)}
                disabled={loading}
                className={`p-3 rounded-lg border-2 transition ${
                  currentPair?.category === cat.value
                    ? 'bg-redhat-red border-redhat-red text-white'
                    : 'bg-redhat-dark-elevated border-redhat-grid-line hover:border-redhat-red'
                }`}
              >
                <div className="text-2xl mb-1">{cat.icon}</div>
                <div className="text-sm">{cat.label}</div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Main Comparison */}
      {currentPair && (
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
              onClick={() => !guessResult && onGuess('a')}
              disabled={loading || guessResult}
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
              onClick={() => !guessResult && onGuess('b')}
              disabled={loading || guessResult}
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

      {/* Result Feedback */}
      {guessResult && (
        <div className={`p-6 rounded-lg mb-6 border-2 ${
          guessResult.correct ? 'bg-green-900 bg-opacity-20 border-green-400' : 'bg-redhat-red bg-opacity-10 border-redhat-red'
        }`}>
          <div className="text-center">
            <div className="text-4xl font-display mb-3">
              {guessResult.correct ? '🎉 Correct!' : '❌ Incorrect'}
            </div>
            <p className="text-lg mb-4 text-redhat-text-primary">{guessResult.explanation}</p>
            <div className="flex justify-center gap-4">
              <button
                onClick={() => onContinue(selectedCategory)}
                className="px-6 py-3 bg-redhat-red hover:bg-redhat-red-hover border border-redhat-red rounded-lg font-mono uppercase tracking-wider font-semibold transition"
              >
                Next Challenge
              </button>
              <button
                onClick={onEndGame}
                className="px-6 py-3 bg-redhat-dark-elevated border border-redhat-grid-line hover:border-redhat-red rounded-lg font-mono uppercase tracking-wider font-semibold transition"
              >
                End Game
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && !currentPair && (
        <div className="text-center py-12">
          <div className="animate-spin inline-block w-12 h-12 border-4 border-redhat-red border-t-transparent rounded-full mb-4"></div>
          <p className="text-redhat-text-secondary font-mono">Generating data pair...</p>
        </div>
      )}
    </div>
  )
}
