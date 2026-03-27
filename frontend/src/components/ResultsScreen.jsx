import { useState } from 'react'

export default function ResultsScreen({ session, apiUrl, onRestart }) {
  const [name, setName] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  const accuracy = session.total_guesses > 0
    ? Math.round((session.correct_guesses / session.total_guesses) * 100)
    : 0

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!name.trim()) {
      alert('Please enter your name')
      return
    }

    setSubmitting(true)
    try {
      await fetch(`${apiUrl}/leaderboard`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name.trim(),
          score: session.score,
          accuracy: accuracy / 100
        })
      })
      setSubmitted(true)
    } catch (error) {
      console.error('Failed to submit to leaderboard:', error)
      alert('Failed to submit score. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  const getPerformanceMessage = () => {
    if (accuracy >= 90) return { emoji: '🏆', message: 'Outstanding! You have a keen eye for authenticity!' }
    if (accuracy >= 70) return { emoji: '🎯', message: 'Great job! You spotted most of the fakes!' }
    if (accuracy >= 50) return { emoji: '👍', message: 'Not bad! You got more than half right!' }
    return { emoji: '🤔', message: 'Keep practicing! AI-generated content can be tricky!' }
  }

  const performance = getPerformanceMessage()

  return (
    <div className="max-w-4xl mx-auto text-center">
      <div className="bg-redhat-dark-surface border border-redhat-grid-line rounded-lg p-8 mb-8">
        <h2 className="text-4xl font-display font-bold mb-4 text-redhat-red">Game Over!</h2>
        <div className="text-6xl mb-6">{performance.emoji}</div>
        <p className="text-xl text-redhat-text-secondary font-text mb-8">{performance.message}</p>

        {/* Final Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
          <div>
            <div className="text-4xl font-mono font-bold text-redhat-red mb-2">{session.score}</div>
            <div className="text-xs text-redhat-text-tertiary font-mono uppercase tracking-wider">Final Score</div>
          </div>
          <div>
            <div className="text-4xl font-mono font-bold text-green-400 mb-2">{session.correct_guesses}</div>
            <div className="text-xs text-redhat-text-tertiary font-mono uppercase tracking-wider">Correct</div>
          </div>
          <div>
            <div className="text-4xl font-mono font-bold text-blue-400 mb-2">{session.total_guesses}</div>
            <div className="text-xs text-redhat-text-tertiary font-mono uppercase tracking-wider">Total Guesses</div>
          </div>
          <div>
            <div className="text-4xl font-mono font-bold text-purple-400 mb-2">{accuracy}%</div>
            <div className="text-xs text-redhat-text-tertiary font-mono uppercase tracking-wider">Accuracy</div>
          </div>
        </div>

        {/* Leaderboard Submission */}
        {!submitted ? (
          <form onSubmit={handleSubmit} className="max-w-md mx-auto">
            <h3 className="text-xl font-display font-semibold mb-4 text-redhat-red">Submit to Leaderboard</h3>
            <div className="flex gap-3">
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter your name"
                className="flex-1 px-4 py-3 bg-redhat-dark-elevated border border-redhat-grid-line rounded-lg focus:outline-none focus:border-redhat-red text-redhat-text-primary font-text"
                maxLength={30}
              />
              <button
                type="submit"
                disabled={submitting}
                className="px-6 py-3 bg-redhat-red hover:bg-redhat-red-hover disabled:bg-redhat-dark-elevated disabled:border disabled:border-redhat-grid-line rounded-lg font-mono uppercase tracking-wider font-semibold transition"
              >
                {submitting ? 'Submitting...' : 'Submit'}
              </button>
            </div>
          </form>
        ) : (
          <div className="bg-green-900 bg-opacity-20 border-2 border-green-400 p-4 rounded-lg mb-4">
            <p className="text-green-400 font-semibold font-mono">Score submitted to leaderboard!</p>
          </div>
        )}
      </div>

      {/* Insights */}
      <div className="bg-redhat-dark-surface border border-redhat-grid-line rounded-lg p-8 mb-8">
        <h3 className="text-2xl font-display font-semibold mb-4 text-redhat-red">What You Learned</h3>
        <div className="text-left space-y-4 text-redhat-text-secondary font-text">
          <p>
            <strong className="text-redhat-text-primary">Synthetic data generation</strong> uses AI models to create realistic fake data that mimics real examples. This technology is valuable for:
          </p>
          <ul className="list-disc list-inside space-y-2 ml-4">
            <li>Training machine learning models without real user data</li>
            <li>Testing systems with diverse, edge-case scenarios</li>
            <li>Preserving privacy while maintaining data utility</li>
            <li>Augmenting small datasets for better model performance</li>
          </ul>
          <p className="text-sm text-redhat-text-tertiary mt-4 font-mono">
            The difficulty levels showed how AI temperature, prompt engineering, and model sophistication affect the quality of synthetic data generation.
          </p>
        </div>
      </div>

      {/* Actions */}
      <button
        onClick={onRestart}
        className="px-8 py-4 bg-redhat-red hover:bg-redhat-red-hover border border-redhat-red rounded-lg font-mono uppercase tracking-wider font-semibold text-lg transition transform hover:scale-105"
      >
        Play Again
      </button>
    </div>
  )
}
