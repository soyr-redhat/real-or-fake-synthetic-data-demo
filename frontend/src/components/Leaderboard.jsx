import { useState, useEffect } from 'react'

export default function Leaderboard({ apiUrl }) {
  const [leaderboard, setLeaderboard] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadLeaderboard()
    // Refresh every 10 seconds
    const interval = setInterval(loadLeaderboard, 10000)
    return () => clearInterval(interval)
  }, [])

  const loadLeaderboard = async () => {
    try {
      const response = await fetch(`${apiUrl}/leaderboard?limit=10`)
      const data = await response.json()
      setLeaderboard(data.leaderboard || [])
    } catch (error) {
      console.error('Failed to load leaderboard:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="bg-redhat-dark-surface border border-redhat-grid-line rounded-lg p-8 text-center">
        <div className="animate-spin inline-block w-8 h-8 border-4 border-redhat-red border-t-transparent rounded-full"></div>
        <p className="mt-4 text-redhat-text-secondary font-mono">Loading leaderboard...</p>
      </div>
    )
  }

  return (
    <div className="bg-redhat-dark-surface border border-redhat-grid-line rounded-lg p-6">
      <h2 className="text-2xl font-display font-bold mb-6 text-center text-redhat-text-primary">
        <span className="text-redhat-red">🏆</span> Top Detectives
      </h2>

      {leaderboard.length === 0 ? (
        <p className="text-center text-redhat-text-secondary font-mono">No scores yet. Be the first!</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-redhat-grid-line">
                <th className="py-3 px-4 text-left font-mono text-redhat-text-tertiary uppercase text-xs tracking-wider">Rank</th>
                <th className="py-3 px-4 text-left font-mono text-redhat-text-tertiary uppercase text-xs tracking-wider">Name</th>
                <th className="py-3 px-4 text-right font-mono text-redhat-text-tertiary uppercase text-xs tracking-wider">Score</th>
                <th className="py-3 px-4 text-right font-mono text-redhat-text-tertiary uppercase text-xs tracking-wider">Accuracy</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((entry, index) => (
                <tr
                  key={index}
                  className={`border-b border-redhat-grid-line ${
                    index < 3 ? 'bg-redhat-dark-elevated' : ''
                  }`}
                >
                  <td className="py-3 px-4">
                    {index === 0 && <span className="text-2xl">🥇</span>}
                    {index === 1 && <span className="text-2xl">🥈</span>}
                    {index === 2 && <span className="text-2xl">🥉</span>}
                    {index > 2 && <span className="text-redhat-text-tertiary font-mono">#{index + 1}</span>}
                  </td>
                  <td className="py-3 px-4 font-semibold text-redhat-text-primary font-text">{entry.name}</td>
                  <td className="py-3 px-4 text-right text-redhat-red font-bold font-mono text-lg">
                    {entry.score}
                  </td>
                  <td className="py-3 px-4 text-right text-green-400 font-mono">
                    {Math.round(entry.accuracy * 100)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
