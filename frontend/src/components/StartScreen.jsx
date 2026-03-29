export default function StartScreen({ onStart, loading }) {
  return (
    <div className="text-center max-w-4xl mx-auto">
      <div className="mb-8">
        <h2 className="text-5xl font-display font-bold mb-4 text-redhat-text-primary">Can You Spot the Fake?</h2>
        <p className="text-xl text-redhat-text-secondary mb-6 font-text">
          Test your ability to distinguish between real and AI-generated data.
          Choose a difficulty level and see how well you can detect synthetic content!
        </p>
      </div>

      <div className="bg-redhat-dark-surface border border-redhat-grid-line rounded-lg p-8 mb-8">
        <h3 className="text-2xl font-display font-semibold mb-6 text-redhat-red">How to Play</h3>
        <div className="grid md:grid-cols-3 gap-6 text-left">
          <div className="bg-redhat-dark-elevated border border-redhat-grid-line p-6 rounded-lg">
            <div className="text-4xl mb-3 font-display text-redhat-red">01</div>
            <h4 className="font-display font-semibold mb-2 text-redhat-text-primary">Compare Data</h4>
            <p className="text-sm text-redhat-text-secondary font-text">
              You'll see two similar pieces of data side-by-side: one real, one AI-generated
            </p>
          </div>
          <div className="bg-redhat-dark-elevated border border-redhat-grid-line p-6 rounded-lg">
            <div className="text-4xl mb-3 font-display text-redhat-red">02</div>
            <h4 className="font-display font-semibold mb-2 text-redhat-text-primary">Make Your Guess</h4>
            <p className="text-sm text-redhat-text-secondary font-text">
              Click the option you think is the REAL data
            </p>
          </div>
          <div className="bg-redhat-dark-elevated border border-redhat-grid-line p-6 rounded-lg">
            <div className="text-4xl mb-3 font-display text-redhat-red">03</div>
            <h4 className="font-display font-semibold mb-2 text-redhat-text-primary">Progress & Score</h4>
            <p className="text-sm text-redhat-text-secondary font-text">
              Categories cycle automatically. Difficulty increases as you score points. Build streaks for bonus points!
            </p>
          </div>
        </div>
      </div>

      <div className="mb-8">
        <h3 className="text-2xl font-display font-semibold mb-4 text-redhat-red">Select Starting Difficulty</h3>
        <p className="text-sm text-redhat-text-tertiary font-mono text-center mb-4">
          💡 Difficulty auto-increases: Easy (0pts) → Medium (50pts) → Hard (150pts)
        </p>
        <div className="grid md:grid-cols-3 gap-4 max-w-3xl mx-auto">
          <button
            onClick={() => onStart('easy')}
            disabled={loading}
            className="bg-redhat-dark-elevated border-2 border-green-500 hover:bg-green-500 hover:bg-opacity-10 disabled:bg-redhat-dark-surface disabled:border-redhat-grid-line p-6 rounded-lg transition transform hover:scale-105"
          >
            <div className="text-2xl mb-2">🟢 Easy</div>
            <p className="text-sm">
              Obvious fakes with generic AI language
            </p>
          </button>

          <button
            onClick={() => onStart('medium')}
            disabled={loading}
            className="bg-redhat-dark-elevated border-2 border-yellow-500 hover:bg-yellow-500 hover:bg-opacity-10 disabled:bg-redhat-dark-surface disabled:border-redhat-grid-line p-6 rounded-lg transition transform hover:scale-105"
          >
            <div className="text-2xl mb-2">🟡 Medium</div>
            <p className="text-sm">
              Realistic synthetics that mimic human style
            </p>
          </button>

          <button
            onClick={() => onStart('hard')}
            disabled={loading}
            className="bg-redhat-dark-elevated border-2 border-redhat-red hover:bg-redhat-red hover:bg-opacity-10 disabled:bg-redhat-dark-surface disabled:border-redhat-grid-line p-6 rounded-lg transition transform hover:scale-105"
          >
            <div className="text-2xl mb-2">🔴 Hard</div>
            <p className="text-sm">
              Nearly indistinguishable from real data
            </p>
          </button>
        </div>

        {loading && (
          <div className="mt-4 text-redhat-text-secondary font-mono">
            <div className="animate-spin inline-block w-6 h-6 border-4 border-redhat-red border-t-transparent rounded-full mr-2"></div>
            Starting game...
          </div>
        )}
      </div>

      <div className="bg-redhat-dark-surface border border-redhat-grid-line rounded-lg p-6 max-w-2xl mx-auto">
        <h4 className="font-semibold mb-3 text-redhat-text-primary">Game Rules:</h4>
        <div className="space-y-2 text-sm text-redhat-text-secondary font-text text-left">
          <p>❤️ <strong className="text-redhat-text-primary">3 Lives:</strong> Lose one per wrong answer. Game over when lives reach 0.</p>
          <p>🔄 <strong className="text-redhat-text-primary">Auto-Cycling:</strong> Categories rotate automatically (Reviews → Descriptions → Profiles → Code)</p>
          <p>📈 <strong className="text-redhat-text-primary">Progressive Difficulty:</strong> Harder challenges unlock as you score points</p>
          <p>🔥 <strong className="text-redhat-text-primary">Streak Bonus:</strong> Consecutive correct answers earn extra points!</p>
        </div>
      </div>
    </div>
  )
}
