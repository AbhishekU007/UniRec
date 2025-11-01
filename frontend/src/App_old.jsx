import React, { useState, useEffect } from 'react';
import { Search, Film, ShoppingBag, Music, GraduationCap, Sparkles, TrendingUp, User, BarChart3 } from 'lucide-react';

// API base URL
const API_BASE = 'http://localhost:8000';

const UniRecApp = () => {
  const [userId, setUserId] = useState(1);
  const [recommendations, setRecommendations] = useState([]);
  const [userProfile, setUserProfile] = useState(null);
  const [selectedDomain, setSelectedDomain] = useState('unified');
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [view, setView] = useState('recommendations'); // recommendations, profile, stats

  const domains = {
    unified: { name: 'All Domains', icon: Sparkles, color: 'from-purple-500 to-pink-500' },
    movies: { name: 'Movies', icon: Film, color: 'from-blue-500 to-cyan-500' },
    products: { name: 'Products', icon: ShoppingBag, color: 'from-green-500 to-emerald-500' },
    music: { name: 'Music', icon: Music, color: 'from-orange-500 to-red-500' },
    courses: { name: 'Courses', icon: GraduationCap, color: 'from-indigo-500 to-purple-500' }
  };

  useEffect(() => {
    fetchRecommendations();
    fetchUserProfile();
    fetchStats();
  }, [userId, selectedDomain]);

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const endpoint = selectedDomain === 'unified' 
        ? `${API_BASE}/api/recommendations/unified/${userId}`
        : `${API_BASE}/api/recommendations/${selectedDomain}/${userId}`;
      
      const response = await fetch(endpoint);
      const data = await response.json();
      setRecommendations(data.recommendations || []);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      // Mock data for demo
      setRecommendations([
        { item_id: 1, title: 'Inception', domain: 'movies', score: 0.95, metadata: { genres: 'Sci-Fi, Thriller' } },
        { item_id: 2, title: 'Sony WH-1000XM5', domain: 'products', score: 0.92, metadata: { category: 'Electronics', price: 399 } },
        { item_id: 3, title: 'Bohemian Rhapsody', domain: 'music', score: 0.89, metadata: { artist: 'Queen', genre: 'Rock' } },
        { item_id: 4, title: 'Machine Learning A-Z', domain: 'courses', score: 0.87, metadata: { difficulty: 'Intermediate', duration: 44 } }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const fetchUserProfile = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/profile/${userId}`);
      const data = await response.json();
      setUserProfile(data);
    } catch (error) {
      console.error('Error fetching profile:', error);
      setUserProfile({
        user_id: userId,
        domains_engaged: ['movies', 'products', 'music', 'courses'],
        preferences: {}
      });
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/stats`);
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
      setStats({
        models_loaded: 4,
        domains: [
          { name: 'movies', total_items: 62423, total_users: 162541 },
          { name: 'products', total_items: 10000, total_users: 50000 },
          { name: 'music', total_items: 50000, total_users: 100000 },
          { name: 'courses', total_items: 3500, total_users: 15000 }
        ]
      });
    }
  };

  const getDomainIcon = (domain) => {
    const DomainIcon = domains[domain]?.icon || Sparkles;
    return <DomainIcon className="w-5 h-5" />;
  };

  const getDomainColor = (domain) => {
    return domains[domain]?.color || 'from-gray-500 to-gray-600';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="bg-black/30 backdrop-blur-lg border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">UniRec</h1>
                <p className="text-sm text-purple-300">Multi-Domain AI Recommendations</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <button
                onClick={() => setView('recommendations')}
                className={`px-4 py-2 rounded-lg transition-all ${
                  view === 'recommendations'
                    ? 'bg-white/20 text-white'
                    : 'text-white/60 hover:text-white'
                }`}
              >
                <TrendingUp className="w-5 h-5" />
              </button>
              <button
                onClick={() => setView('profile')}
                className={`px-4 py-2 rounded-lg transition-all ${
                  view === 'profile'
                    ? 'bg-white/20 text-white'
                    : 'text-white/60 hover:text-white'
                }`}
              >
                <User className="w-5 h-5" />
              </button>
              <button
                onClick={() => setView('stats')}
                className={`px-4 py-2 rounded-lg transition-all ${
                  view === 'stats'
                    ? 'bg-white/20 text-white'
                    : 'text-white/60 hover:text-white'
                }`}
              >
                <BarChart3 className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* User Input */}
          <div className="mt-6 flex items-center gap-4">
            <div className="flex-1 max-w-md">
              <label className="block text-sm text-purple-200 mb-2">User ID</label>
              <input
                type="number"
                value={userId}
                onChange={(e) => setUserId(parseInt(e.target.value) || 1)}
                className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="Enter user ID..."
              />
            </div>
            <button
              onClick={fetchRecommendations}
              disabled={loading}
              className="mt-7 px-6 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-lg hover:shadow-lg hover:shadow-purple-500/50 transition-all disabled:opacity-50"
            >
              {loading ? 'Loading...' : 'Get Recommendations'}
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {view === 'recommendations' && (
          <>
            {/* Domain Tabs */}
            <div className="flex gap-2 mb-8 overflow-x-auto pb-2">
              {Object.entries(domains).map(([key, domain]) => {
                const Icon = domain.icon;
                return (
                  <button
                    key={key}
                    onClick={() => setSelectedDomain(key)}
                    className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all whitespace-nowrap ${
                      selectedDomain === key
                        ? `bg-gradient-to-r ${domain.color} text-white shadow-lg`
                        : 'bg-white/10 text-white/60 hover:bg-white/20'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    {domain.name}
                  </button>
                );
              })}
            </div>

            {/* Recommendations Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {recommendations.map((rec, idx) => (
                <div
                  key={idx}
                  className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-6 hover:bg-white/15 transition-all group"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className={`p-2 rounded-lg bg-gradient-to-br ${getDomainColor(rec.domain)}`}>
                      {getDomainIcon(rec.domain)}
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-white">
                        {(rec.score * 100).toFixed(0)}%
                      </div>
                      <div className="text-xs text-purple-300">Match Score</div>
                    </div>
                  </div>

                  <h3 className="text-lg font-semibold text-white mb-2 line-clamp-2">
                    {rec.title}
                  </h3>

                  <div className="space-y-1">
                    {Object.entries(rec.metadata).map(([key, value]) => (
                      <div key={key} className="text-sm text-white/60">
                        <span className="capitalize">{key}:</span>{' '}
                        <span className="text-white/80">{value}</span>
                      </div>
                    ))}
                  </div>

                  <div className="mt-4 pt-4 border-t border-white/10">
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r ${getDomainColor(rec.domain)} text-white`}>
                      {rec.domain.toUpperCase()}
                    </span>
                  </div>
                </div>
              ))}
            </div>

            {recommendations.length === 0 && !loading && (
              <div className="text-center py-16">
                <div className="text-white/40 text-lg">No recommendations available</div>
                <p className="text-white/30 text-sm mt-2">Try a different user ID or domain</p>
              </div>
            )}
          </>
        )}

        {view === 'profile' && userProfile && (
          <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-8">
            <h2 className="text-2xl font-bold text-white mb-6">User Profile</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-semibold text-purple-300 mb-3">Engaged Domains</h3>
                <div className="space-y-2">
                  {userProfile.domains_engaged.map((domain) => (
                    <div key={domain} className="flex items-center gap-3 p-3 bg-white/5 rounded-lg">
                      {getDomainIcon(domain)}
                      <span className="text-white capitalize">{domain}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-purple-300 mb-3">Preferences</h3>
                <pre className="text-sm text-white/70 bg-black/20 p-4 rounded-lg overflow-auto max-h-64">
                  {JSON.stringify(userProfile.preferences, null, 2)}
                </pre>
              </div>
            </div>
          </div>
        )}

        {view === 'stats' && stats && (
          <div className="space-y-6">
            <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-8">
              <h2 className="text-2xl font-bold text-white mb-6">System Statistics</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.domains.map((domain) => (
                  <div key={domain.name} className="bg-white/5 rounded-xl p-6">
                    <div className="flex items-center gap-3 mb-4">
                      {getDomainIcon(domain.name)}
                      <h3 className="text-lg font-semibold text-white capitalize">{domain.name}</h3>
                    </div>
                    <div className="space-y-2">
                      <div>
                        <div className="text-3xl font-bold text-white">{domain.total_items.toLocaleString()}</div>
                        <div className="text-sm text-white/60">Total Items</div>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-purple-300">{domain.total_users.toLocaleString()}</div>
                        <div className="text-sm text-white/60">Total Users</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UniRecApp;