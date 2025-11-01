import React, { useState, useEffect } from 'react';
import { Search, Film, ShoppingBag, Music, GraduationCap, Sparkles, TrendingUp, User, BarChart3, LogOut, Moon, Sun } from 'lucide-react';
import Auth from './Auth';
import OnboardingQuiz from './OnboardingQuiz';
import LandingPage from './LandingPage';

// API base URL
const API_BASE = 'http://localhost:8000';

const UniRecApp = () => {
  const [authState, setAuthState] = useState('loading'); // loading, landing, login, signup, authenticated
  const [authMode, setAuthMode] = useState('login'); // login or signup for Auth component
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [userProfile, setUserProfile] = useState(null);
  const [selectedDomain, setSelectedDomain] = useState('unified');
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [view, setView] = useState('recommendations'); // recommendations, profile, stats
  const [darkMode, setDarkMode] = useState(false);

  // Initialize dark mode from localStorage
  useEffect(() => {
    const isDark = localStorage.getItem('darkMode') === 'true';
    setDarkMode(isDark);
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, []);

  const toggleDarkMode = () => {
    const newMode = !darkMode;
    setDarkMode(newMode);
    localStorage.setItem('darkMode', String(newMode));
    if (newMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  const domains = {
    unified: { name: 'All Domains', icon: Sparkles, color: 'from-purple-500 to-pink-500' },
    movies: { name: 'Movies', icon: Film, color: 'from-blue-500 to-cyan-500' },
    products: { name: 'Products', icon: ShoppingBag, color: 'from-green-500 to-emerald-500' },
    music: { name: 'Music', icon: Music, color: 'from-orange-500 to-red-500' },
    courses: { name: 'Courses', icon: GraduationCap, color: 'from-indigo-500 to-purple-500' }
  };

  // Check for existing auth on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    
    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
      setAuthState('authenticated');
    } else {
      setAuthState('landing'); // Show landing page by default
    }
  }, []);

  // Fetch recommendations when authenticated
  useEffect(() => {
    if (authState === 'authenticated') {
      fetchRecommendations();
      fetchStats();
    }
  }, [authState, selectedDomain]);

  const handleAuth = (data) => {
    setToken(data.access_token);
    setUser(data.user);
    setAuthState('authenticated');
  };

  const handleNavigate = (destination) => {
    if (destination === 'login') {
      setAuthMode('login');
      setAuthState('auth');
    } else if (destination === 'signup') {
      setAuthMode('signup');
      setAuthState('auth');
    } else if (destination === 'landing') {
      setAuthState('landing');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
    setAuthState('landing'); // Go back to landing page
    setRecommendations([]);
  };

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const endpoint = selectedDomain === 'unified' 
        ? `${API_BASE}/api/recommendations/unified`
        : `${API_BASE}/api/recommendations/${selectedDomain}`;
      
      const response = await fetch(endpoint, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
      }
      
      const data = await response.json();
      setRecommendations(data.recommendations || []);
      setUserProfile(data.profile_summary);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  // Show different views based on auth state
  if (authState === 'loading') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-900 dark:to-indigo-950 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading...</p>
        </div>
      </div>
    );
  }

  if (authState === 'landing') {
    return <LandingPage onNavigate={handleNavigate} />;
  }

  if (authState === 'auth') {
    return <Auth onAuth={handleAuth} initialMode={authMode} onBack={() => setAuthState('landing')} />;
  }

  // Main App UI (authenticated)
  const getDomainIcon = (domain) => {
    const DomainIcon = domains[domain]?.icon || Sparkles;
    return <DomainIcon className="w-4 h-4" />;
  };

  const getDomainColor = (domain) => {
    const colors = {
      movies: 'bg-blue-100 text-blue-700',
      products: 'bg-green-100 text-green-700',
      music: 'bg-orange-100 text-orange-700',
      courses: 'bg-indigo-100 text-indigo-700',
      unified: 'bg-purple-100 text-purple-700'
    };
    return colors[domain] || 'bg-gray-100 text-gray-700';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-900 dark:to-indigo-950">
      {/* Header */}
      <header className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">UniRec</h1>
                <p className="text-xs text-gray-500 dark:text-gray-400">Personalized for {user?.name}</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setView('recommendations')}
                className={`p-2 rounded-lg transition-colors ${
                  view === 'recommendations' 
                    ? 'bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400' 
                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
                }`}
              >
                <TrendingUp className="w-5 h-5" />
              </button>
              <button
                onClick={() => setView('profile')}
                className={`p-2 rounded-lg transition-colors ${
                  view === 'profile' 
                    ? 'bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400' 
                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
                }`}
              >
                <User className="w-5 h-5" />
              </button>
              <button
                onClick={() => setView('stats')}
                className={`p-2 rounded-lg transition-colors ${
                  view === 'stats' 
                    ? 'bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400' 
                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
                }`}
              >
                <BarChart3 className="w-5 h-5" />
              </button>
              <button
                onClick={toggleDarkMode}
                className="p-2 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                aria-label="Toggle dark mode"
              >
                {darkMode ? (
                  <Sun className="w-5 h-5 text-yellow-500" />
                ) : (
                  <Moon className="w-5 h-5 text-gray-700" />
                )}
              </button>
              <button
                onClick={handleLogout}
                className="p-2 text-gray-600 dark:text-gray-400 hover:bg-red-100 dark:hover:bg-red-900/50 hover:text-red-600 dark:hover:text-red-400 rounded-lg transition-colors"
                title="Logout"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {view === 'recommendations' && (
          <>
            {/* Domain Tabs */}
            <div className="flex space-x-2 mb-8 overflow-x-auto pb-2">
              {Object.entries(domains).map(([key, domain]) => {
                const Icon = domain.icon;
                return (
                  <button
                    key={key}
                    onClick={() => setSelectedDomain(key)}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-all whitespace-nowrap ${
                      selectedDomain === key
                        ? `bg-gradient-to-r ${domain.color} text-white shadow-lg`
                        : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:shadow-md border border-gray-200 dark:border-gray-700'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{domain.name}</span>
                  </button>
                );
              })}
            </div>

            {/* Recommendations Grid */}
            {loading ? (
              <div className="text-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
                <p className="text-gray-600 dark:text-gray-400">Loading recommendations...</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {recommendations.map((rec, index) => (
                  <div
                    key={`${rec.domain}-${rec.item_id}-${index}`}
                    className="bg-white dark:bg-gray-800 rounded-xl shadow-md hover:shadow-xl transition-all p-6 border border-gray-100 dark:border-gray-700"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getDomainColor(rec.domain)}`}>
                        {getDomainIcon(rec.domain)}
                        <span className="ml-1">{rec.domain}</span>
                      </span>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
                          {Math.round(rec.score * 100)}%
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">Match</div>
                      </div>
                    </div>
                    
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2 line-clamp-2">
                      {rec.title}
                    </h3>
                    
                    <div className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                      {Object.entries(rec.metadata || {}).slice(0, 3).map(([key, value]) => (
                        <div key={key} className="flex justify-between">
                          <span className="capitalize">{key.replace(/_/g, ' ')}:</span>
                          <span className="font-medium">{value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {!loading && recommendations.length === 0 && (
              <div className="text-center py-12">
                <Sparkles className="w-16 h-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
                <p className="text-gray-600 dark:text-gray-400">No recommendations found</p>
              </div>
            )}
          </>
        )}

        {view === 'profile' && (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-8 max-w-2xl mx-auto">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Your Profile</h2>
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-600 dark:text-gray-400">Name</label>
                <p className="text-lg text-gray-900 dark:text-white">{user?.name}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600 dark:text-gray-400">Email</label>
                <p className="text-lg text-gray-900 dark:text-white">{user?.email}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600 dark:text-gray-400">Member Since</label>
                <p className="text-lg text-gray-900 dark:text-white">
                  {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                </p>
              </div>
              {user?.preferences && (
                <div>
                  <label className="text-sm font-medium text-gray-600 dark:text-gray-400 block mb-2">Your Preferences</label>
                  <div className="grid grid-cols-2 gap-4">
                    {Object.entries(user.preferences).map(([key, value]) => (
                      <div key={key} className="p-3 bg-gray-50 dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
                        <p className="text-xs text-gray-600 dark:text-gray-400 capitalize">{key.replace(/_/g, ' ')}</p>
                        <p className="text-sm font-medium text-gray-900 dark:text-white">
                          {Array.isArray(value) ? value.join(', ') : value}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {view === 'stats' && (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-8 max-w-2xl mx-auto">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">System Stats</h2>
            {stats && (
              <div className="space-y-4">
                <div className="p-4 bg-green-50 dark:bg-green-900/30 rounded-lg border border-green-200 dark:border-green-800">
                  <p className="text-sm text-green-600 dark:text-green-400 font-medium">Status</p>
                  <p className="text-2xl font-bold text-green-700 dark:text-green-300 capitalize">{stats.status}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">Models Loaded</p>
                  <div className="grid grid-cols-2 gap-2">
                    {Object.entries(stats.models_loaded || {}).map(([model, loaded]) => (
                      <div key={model} className={`p-3 rounded-lg border ${loaded ? 'bg-green-50 dark:bg-green-900/30 border-green-200 dark:border-green-800' : 'bg-red-50 dark:bg-red-900/30 border-red-200 dark:border-red-800'}`}>
                        <p className="text-sm capitalize text-gray-900 dark:text-white">{model}</p>
                        <p className={`text-xs font-medium ${loaded ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                          {loaded ? '✓ Loaded' : '✗ Not loaded'}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default UniRecApp;
