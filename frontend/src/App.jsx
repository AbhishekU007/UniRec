import React, { useState, useEffect } from 'react';
import { Search, Film, ShoppingBag, Music, GraduationCap, Sparkles, TrendingUp, User, BarChart3, LogOut, Moon, Sun, Edit2, Save, X, ThumbsUp, ThumbsDown } from 'lucide-react';
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
  const [isEditingPreferences, setIsEditingPreferences] = useState(false);
  const [editedQuizResponses, setEditedQuizResponses] = useState(null);
  const [selectedItem, setSelectedItem] = useState(null); // For modal
  const [showModal, setShowModal] = useState(false);
  const [notification, setNotification] = useState(null); // For toast notifications

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
      // Always use regular unified endpoint (RL is applied on backend)
      // Increased n_per_domain to 10 to show more variety
      const endpoint = selectedDomain === 'unified' 
        ? `${API_BASE}/api/recommendations/unified?n_per_domain=10`
        : `${API_BASE}/api/recommendations/${selectedDomain}/${user?.internal_user_id}?n_recommendations=15`;
      
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

  const handleEditPreferences = () => {
    setEditedQuizResponses(user?.quiz_responses || {});
    setIsEditingPreferences(true);
  };

  const handleCancelEdit = () => {
    setIsEditingPreferences(false);
    setEditedQuizResponses(null);
  };

  const handleSavePreferences = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/auth/update-preferences`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          quiz_responses: editedQuizResponses
        })
      });

      if (!response.ok) {
        throw new Error('Failed to update preferences');
      }

      const data = await response.json();
      
      // Update local user state
      const updatedUser = { ...user, quiz_responses: editedQuizResponses, preferences: data.preferences };
      setUser(updatedUser);
      localStorage.setItem('user', JSON.stringify(updatedUser));
      
      setIsEditingPreferences(false);
      setEditedQuizResponses(null);
      
      // Refresh recommendations
      fetchRecommendations();
      
      showNotification('✅ Preferences updated successfully!', 'success');
    } catch (error) {
      console.error('Error updating preferences:', error);
      showNotification('❌ Failed to update preferences. Please try again.', 'error');
    }
  };

  const handlePreferenceChange = (key, value) => {
    setEditedQuizResponses(prev => ({
      ...prev,
      [key]: value
    }));
  };

  // ============================================================================
  // REINFORCEMENT LEARNING - INTERACTION TRACKING
  // ============================================================================

  const logInteraction = async (itemId, domain, actionType, metadata = {}) => {
    try {
      console.log('📝 Logging interaction:', { itemId, domain, actionType });
      
      const response = await fetch(`${API_BASE}/api/interactions/log`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          item_id: parseInt(itemId),  // Ensure integer
          domain: domain,
          action_type: actionType,
          metadata: metadata
        })
      });
      
      if (!response.ok) {
        console.error('Failed to log interaction:', response.status);
      } else {
        console.log('✅ Interaction logged successfully');
      }
    } catch (error) {
      console.error('❌ Error logging interaction:', error);
      throw error; // Re-throw so handleLike/handleDislike can catch it
    }
  };

  const handleRecommendationClick = (rec) => {
    // Log click interaction
    const itemId = rec.id || rec.item_id || rec.track_id || rec.movie_id || rec.product_id || rec.course_id;
    logInteraction(itemId, rec.domain, 'view', rec.metadata).catch(err => {
      console.error('Failed to log view:', err);
    });
    
    // Show modal with details
    setSelectedItem(rec);
    setShowModal(true);
  };

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  const handleLike = async (rec) => {
    const itemId = rec.id || rec.item_id || rec.track_id || rec.movie_id || rec.product_id || rec.course_id;
    
    try {
      // Log interaction (let it happen in background)
      logInteraction(itemId, rec.domain, 'like', rec.metadata).catch(err => {
        console.error('Failed to log like:', err);
      });
      
      // Visual feedback
      showNotification(`❤️ Liked: ${rec.title}`, 'success');
      
    } catch (error) {
      console.error('Error in handleLike:', error);
    }
  };

  const handleDislike = async (rec) => {
    const itemId = rec.id || rec.item_id || rec.track_id || rec.movie_id || rec.product_id || rec.course_id;
    
    try {
      // Log interaction (don't wait for it, let it happen in background)
      logInteraction(itemId, rec.domain, 'dislike', rec.metadata).catch(err => {
        console.error('Failed to log dislike:', err);
      });
      
      // Visual feedback
      showNotification(`👎 Removed: ${rec.title}`, 'info');
      
      // Remove from current view immediately
      setRecommendations(prev => prev.filter(r => {
        const rId = r.id || r.item_id || r.track_id || r.movie_id || r.product_id || r.course_id;
        return rId !== itemId;
      }));
      
    } catch (error) {
      console.error('Error in handleDislike:', error);
      // Don't show error notification for dislike
    }
  };

  const handleRate = async (rec, rating) => {
    const itemId = rec.id || rec.item_id || rec.track_id || rec.movie_id || rec.product_id || rec.course_id;
    logInteraction(itemId, rec.domain, 'rate', {
      ...rec.metadata,
      rating: rating
    });
    
    showNotification(`⭐ Rated ${rating}/5 stars`, 'success');
  };

  const updatePreferencesFromInteractions = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/preferences/update-from-interactions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ days: 30 })
      });

      if (!response.ok) {
        throw new Error('Failed to update preferences');
      }

      const data = await response.json();
      
      if (data.success) {
        // Update user with new preferences
        const updatedUser = {
          ...user,
          preferences: data.new_preferences
        };
        setUser(updatedUser);
        localStorage.setItem('user', JSON.stringify(updatedUser));
        
        showNotification('✨ Your preferences have been updated based on your interactions!', 'success');
        fetchRecommendations();
      }
    } catch (error) {
      console.error('Error updating preferences from interactions:', error);
      showNotification('⚠️ Could not update preferences at this time.', 'error');
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
                      <span className={`flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-medium ${getDomainColor(rec.domain)}`}>
                        {getDomainIcon(rec.domain)}
                        <span>{rec.domain}</span>
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
                    
                    <div className="space-y-1 text-sm text-gray-600 dark:text-gray-400 mb-4">
                      {Object.entries(rec.metadata || {}).slice(0, 3).map(([key, value]) => (
                        <div key={key} className="flex justify-between items-start gap-2">
                          <span className="capitalize whitespace-nowrap">{key.replace(/_/g, ' ')}:</span>
                          <span className="font-medium text-right">
                            {key === 'genres' && typeof value === 'string' 
                              ? value.split('|').join(' | ') 
                              : value}
                          </span>
                        </div>
                      ))}
                    </div>

                    {/* Interaction Buttons - Reinforcement Learning */}
                    <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
                      <button
                        onClick={() => handleLike(rec)}
                        className="flex items-center space-x-1 px-3 py-2 rounded-lg bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 hover:bg-green-100 dark:hover:bg-green-900/40 transition-colors text-sm font-medium"
                        title="I like this"
                      >
                        <ThumbsUp className="w-4 h-4" />
                        <span>Like</span>
                      </button>
                      
                      <button
                        onClick={() => handleRecommendationClick(rec)}
                        className="px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors text-sm font-medium"
                        title="View details"
                      >
                        View
                      </button>
                      
                      <button
                        onClick={() => handleDislike(rec)}
                        className="flex items-center space-x-1 px-3 py-2 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 hover:bg-red-100 dark:hover:bg-red-900/40 transition-colors text-sm font-medium"
                        title="Not interested"
                      >
                        <ThumbsDown className="w-4 h-4" />
                        <span>Pass</span>
                      </button>
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
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-8 max-w-3xl mx-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Your Profile</h2>
              {!isEditingPreferences && (
                <div className="flex space-x-2">
                  <button
                    onClick={updatePreferencesFromInteractions}
                    className="flex items-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
                    title="Update preferences based on your interactions"
                  >
                    <Sparkles className="w-4 h-4" />
                    <span>Learn from Actions</span>
                  </button>
                  <button
                    onClick={handleEditPreferences}
                    className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                  >
                    <Edit2 className="w-4 h-4" />
                    <span>Edit Preferences</span>
                  </button>
                </div>
              )}
              {isEditingPreferences && (
                <div className="flex space-x-2">
                  <button
                    onClick={handleSavePreferences}
                    className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  >
                    <Save className="w-4 h-4" />
                    <span>Save</span>
                  </button>
                  <button
                    onClick={handleCancelEdit}
                    className="flex items-center space-x-2 px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
                  >
                    <X className="w-4 h-4" />
                    <span>Cancel</span>
                  </button>
                </div>
              )}
            </div>

            <div className="space-y-6">
              <div className="pb-6 border-b border-gray-200 dark:border-gray-700">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                </div>
              </div>

              {!isEditingPreferences && user?.preferences && (
                <div>
                  <label className="text-sm font-medium text-gray-600 dark:text-gray-400 block mb-3">Your Preferences</label>
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

              {isEditingPreferences && editedQuizResponses && (
                <div className="space-y-6">
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white">Edit Your Preferences</h3>
                  
                  {/* Movie Genres */}
                  <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300 block mb-2">
                      Favorite Movie Genres
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller', 'Documentary', 'Animation', 'Fantasy'].map(genre => (
                        <button
                          key={genre}
                          onClick={() => {
                            const current = editedQuizResponses.favorite_movie_genres || [];
                            const updated = current.includes(genre)
                              ? current.filter(g => g !== genre)
                              : [...current, genre];
                            handlePreferenceChange('favorite_movie_genres', updated);
                          }}
                          className={`px-3 py-1 rounded-full text-sm transition-colors ${
                            (editedQuizResponses.favorite_movie_genres || []).includes(genre)
                              ? 'bg-blue-600 text-white'
                              : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
                          }`}
                        >
                          {genre}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Music Genres */}
                  <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300 block mb-2">
                      Favorite Music Genres
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {['Pop', 'Rock', 'Hip Hop', 'Jazz', 'Classical', 'Electronic', 'Country', 'R&B', 'Indie', 'Metal'].map(genre => (
                        <button
                          key={genre}
                          onClick={() => {
                            const current = editedQuizResponses.favorite_music_genres || [];
                            const updated = current.includes(genre)
                              ? current.filter(g => g !== genre)
                              : [...current, genre];
                            handlePreferenceChange('favorite_music_genres', updated);
                          }}
                          className={`px-3 py-1 rounded-full text-sm transition-colors ${
                            (editedQuizResponses.favorite_music_genres || []).includes(genre)
                              ? 'bg-orange-600 text-white'
                              : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
                          }`}
                        >
                          {genre}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Shopping Interests */}
                  <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300 block mb-2">
                      Shopping Interests
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {['Electronics', 'Fashion', 'Books', 'Home & Garden', 'Sports', 'Beauty', 'Toys', 'Food', 'Health', 'Automotive'].map(interest => (
                        <button
                          key={interest}
                          onClick={() => {
                            const current = editedQuizResponses.shopping_interests || [];
                            const updated = current.includes(interest)
                              ? current.filter(i => i !== interest)
                              : [...current, interest];
                            handlePreferenceChange('shopping_interests', updated);
                          }}
                          className={`px-3 py-1 rounded-full text-sm transition-colors ${
                            (editedQuizResponses.shopping_interests || []).includes(interest)
                              ? 'bg-green-600 text-white'
                              : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
                          }`}
                        >
                          {interest}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Learning Topics */}
                  <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300 block mb-2">
                      Learning Topics
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {['Programming', 'Business', 'Design', 'Marketing', 'Data Science', 'Languages', 'Music', 'Photography', 'Finance', 'Health'].map(topic => (
                        <button
                          key={topic}
                          onClick={() => {
                            const current = editedQuizResponses.learning_topics || [];
                            const updated = current.includes(topic)
                              ? current.filter(t => t !== topic)
                              : [...current, topic];
                            handlePreferenceChange('learning_topics', updated);
                          }}
                          className={`px-3 py-1 rounded-full text-sm transition-colors ${
                            (editedQuizResponses.learning_topics || []).includes(topic)
                              ? 'bg-indigo-600 text-white'
                              : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
                          }`}
                        >
                          {topic}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Experience Level */}
                  <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300 block mb-2">
                      Experience Level
                    </label>
                    <div className="space-y-2">
                      {[
                        { value: 'beginner', label: 'Beginner - Just getting started' },
                        { value: 'intermediate', label: 'Intermediate - Comfortable navigating' },
                        { value: 'advanced', label: 'Advanced - Power user' }
                      ].map(option => (
                        <button
                          key={option.value}
                          onClick={() => handlePreferenceChange('experience_level', option.value)}
                          className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                            editedQuizResponses.experience_level === option.value
                              ? 'bg-indigo-600 text-white'
                              : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                          }`}
                        >
                          {option.label}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Budget Range */}
                  <div>
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300 block mb-2">
                      Budget Preference
                    </label>
                    <div className="space-y-2">
                      {[
                        { value: 'low', label: 'Budget-friendly' },
                        { value: 'medium', label: 'Moderate' },
                        { value: 'high', label: 'Premium' }
                      ].map(option => (
                        <button
                          key={option.value}
                          onClick={() => handlePreferenceChange('budget_range', option.value)}
                          className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                            editedQuizResponses.budget_range === option.value
                              ? 'bg-green-600 text-white'
                              : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                          }`}
                        >
                          {option.label}
                        </button>
                      ))}
                    </div>
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

      {/* Item Details Modal */}
      {showModal && selectedItem && (
        <div 
          className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
          onClick={() => setShowModal(false)}
        >
          <div 
            className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="sticky top-0 bg-gradient-to-r from-indigo-600 to-purple-600 p-6 rounded-t-2xl">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-xs font-medium text-white capitalize">
                      {selectedItem.domain}
                    </span>
                    {selectedItem.exploration && (
                      <span className="px-3 py-1 bg-yellow-500/30 backdrop-blur-sm rounded-full text-xs font-medium text-white">
                        🔍 Exploration
                      </span>
                    )}
                  </div>
                  <h2 className="text-2xl font-bold text-white mb-1">
                    {selectedItem.title}
                  </h2>
                  <div className="flex items-center space-x-4 text-white/90">
                    <span className="text-3xl font-bold">{Math.round(selectedItem.score * 100)}%</span>
                    <span className="text-sm">Match Score</span>
                  </div>
                </div>
                <button
                  onClick={() => setShowModal(false)}
                  className="p-2 hover:bg-white/20 rounded-lg transition-colors text-white"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>
            </div>

            {/* Modal Body */}
            <div className="p-6">
              {/* Metadata */}
              <div className="space-y-4 mb-6">
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-3">Details</h3>
                <div className="grid grid-cols-1 gap-3">
                  {selectedItem.metadata && Object.entries(selectedItem.metadata).map(([key, value]) => (
                    <div 
                      key={key} 
                      className="flex justify-between items-start p-3 bg-gray-50 dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700"
                    >
                      <span className="text-sm font-medium text-gray-600 dark:text-gray-400 capitalize">
                        {key.replace(/_/g, ' ')}:
                      </span>
                      <span className="text-sm font-semibold text-gray-900 dark:text-white text-right ml-4">
                        {key === 'genres' && typeof value === 'string' 
                          ? value.split('|').join(' | ') 
                          : value}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* RL Boost Info */}
              {selectedItem.rl_boost && (
                <div className={`p-4 rounded-lg border mb-6 ${
                  selectedItem.rl_boost > 0 
                    ? 'bg-green-50 dark:bg-green-900/30 border-green-200 dark:border-green-800' 
                    : 'bg-red-50 dark:bg-red-900/30 border-red-200 dark:border-red-800'
                }`}>
                  <h3 className="text-lg font-bold mb-2 flex items-center space-x-2">
                    <span>{selectedItem.rl_boost > 0 ? '🚀' : '⚠️'}</span>
                    <span className={selectedItem.rl_boost > 0 ? 'text-green-700 dark:text-green-300' : 'text-red-700 dark:text-red-300'}>
                      Reinforcement Learning
                    </span>
                  </h3>
                  <p className={`text-sm ${selectedItem.rl_boost > 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                    {selectedItem.rl_boost > 0 
                      ? `Boosted ${Math.round(selectedItem.rl_boost * 100)}% based on your past positive interactions!`
                      : `Reduced ${Math.abs(Math.round(selectedItem.rl_boost * 100))}% due to past negative feedback.`
                    }
                  </p>
                </div>
              )}

              {/* Exploration Info */}
              {selectedItem.exploration && (
                <div className="p-4 rounded-lg border bg-yellow-50 dark:bg-yellow-900/30 border-yellow-200 dark:border-yellow-800 mb-6">
                  <h3 className="text-lg font-bold mb-2 flex items-center space-x-2 text-yellow-700 dark:text-yellow-300">
                    <span>🔍</span>
                    <span>Exploration Recommendation</span>
                  </h3>
                  <p className="text-sm text-yellow-600 dark:text-yellow-400">
                    This item was selected to help you discover new favorites! We're showing you something different to expand your horizons.
                  </p>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex space-x-3">
                <button
                  onClick={() => {
                    handleLike(selectedItem);
                    setShowModal(false);
                  }}
                  className="flex-1 flex items-center justify-center space-x-2 px-4 py-3 rounded-lg bg-green-600 text-white hover:bg-green-700 transition-colors font-medium"
                >
                  <ThumbsUp className="w-5 h-5" />
                  <span>Like This</span>
                </button>
                <button
                  onClick={() => {
                    handleDislike(selectedItem);
                    setShowModal(false);
                  }}
                  className="flex-1 flex items-center justify-center space-x-2 px-4 py-3 rounded-lg bg-red-600 text-white hover:bg-red-700 transition-colors font-medium"
                >
                  <ThumbsDown className="w-5 h-5" />
                  <span>Not Interested</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Toast Notification */}
      {notification && (
        <div className="fixed bottom-4 right-4 z-50 animate-slide-up">
          <div className={`rounded-lg shadow-2xl p-4 min-w-[300px] max-w-md backdrop-blur-sm border ${
            notification.type === 'success' 
              ? 'bg-green-500/90 border-green-400 text-white' 
              : notification.type === 'error'
              ? 'bg-red-500/90 border-red-400 text-white'
              : 'bg-blue-500/90 border-blue-400 text-white'
          }`}>
            <div className="flex items-start space-x-3">
              <div className="flex-1">
                <p className="font-medium">{notification.message}</p>
              </div>
              <button
                onClick={() => setNotification(null)}
                className="text-white/80 hover:text-white transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UniRecApp;
