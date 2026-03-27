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
      <div className="bg-gray-800 rounded-lg p-8 text-center">
        <div className="animate-spin inline-block w-8 h-8 border-4 border-redhat border-t-transparent rounded-full"></div>
        <p className="mt-4 text-gray-400">Loading leaderboard...</p>
      </div>
    )
  }

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h2 className="text-2xl font-bold mb-6 text-center">
        <span className="text-redhat">🏆</span> Top Detectives
      </h2>

      {leaderboard.length === 0 ? (
        <p className="text-center text-gray-400">No scores yet. Be the first!</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-700">
                <th className="py-3 px-4 text-left">Rank</th>
                <th className="py-3 px-4 text-left">Name</th>
                <th className="py-3 px-4 text-right">Score</th>
                <th className="py-3 px-4 text-right">Accuracy</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((entry, index) => (
                <tr
                  key={index}
                  className={`border-b border-gray-700 ${
                    index < 3 ? 'bg-gray-900 bg-opacity-50' : ''
                  }`}
                >
                  <td className="py-3 px-4">
                    {index === 0 && <span className="text-2xl">🥇</span>}
                    {index === 1 && <span className="text-2xl">🥈</span>}
                    {index === 2 && <span className="text-2xl">🥉</span>}
                    {index > 2 && <span className="text-gray-400">#{index + 1}</span>}
                  </td>
                  <td className="py-3 px-4 font-semibold">{entry.name}</td>
                  <td className="py-3 px-4 text-right text-redhat font-bold">
                    {entry.score}
                  </td>
                  <td className="py-3 px-4 text-right text-green-500">
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
