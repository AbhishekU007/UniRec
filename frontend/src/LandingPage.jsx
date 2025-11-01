import React, { useState, useEffect } from 'react';
import { Sparkles, TrendingUp, Shield, Zap, Users, Heart, Film, Music, ShoppingBag, GraduationCap, ArrowRight, Star, Moon, Sun } from 'lucide-react';

const LandingPage = ({ onNavigate }) => {
  const [darkMode, setDarkMode] = useState(false);

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
  const features = [
    {
      icon: Sparkles,
      title: 'AI-Powered Recommendations',
      description: 'Advanced machine learning algorithms analyze your preferences to deliver personalized suggestions across all domains.'
    },
    {
      icon: TrendingUp,
      title: 'Multi-Domain Intelligence',
      description: 'Get recommendations for movies, music, products, and courses - all from a single unified platform.'
    },
    {
      icon: Shield,
      title: 'Privacy First',
      description: 'Your data is encrypted and secure. We never share your personal information with third parties.'
    },
    {
      icon: Zap,
      title: 'Instant Results',
      description: 'Real-time recommendations that adapt to your tastes. No waiting, just instant personalized content.'
    },
    {
      icon: Users,
      title: 'Personalized Profile',
      description: 'Take a quick quiz to help us understand your preferences and get better recommendations from day one.'
    },
    {
      icon: Heart,
      title: 'Discover New Favorites',
      description: 'Explore content you never knew existed. Our hybrid recommendation engine finds hidden gems just for you.'
    }
  ];

  const domains = [
    {
      icon: Film,
      name: 'Movies',
      description: 'Discover films that match your taste',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: Music,
      name: 'Music',
      description: 'Find your next favorite song or artist',
      color: 'from-orange-500 to-red-500'
    },
    {
      icon: ShoppingBag,
      name: 'Products',
      description: 'Shop smarter with personalized picks',
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: GraduationCap,
      name: 'Courses',
      description: 'Learn skills tailored to your goals',
      color: 'from-indigo-500 to-purple-500'
    }
  ];

  const stats = [
    { number: '160K+', label: 'Recommendations Generated' },
    { number: '1000+', label: 'Active Users' },
    { number: '4', label: 'Content Domains' },
    { number: '95%', label: 'Satisfaction Rate' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-900 dark:to-indigo-950">
      {/* Hero Section */}
      <header className="relative overflow-hidden">
        {/* Navigation */}
        <nav className="absolute top-0 left-0 right-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm border-b border-gray-200 dark:border-gray-700">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">UniRec</h1>
              </div>
              
              <div className="flex items-center space-x-4">
                <button
                  onClick={() => onNavigate('login')}
                  className="px-6 py-2 text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400 font-medium transition-colors"
                >
                  Sign In
                </button>
                <button
                  onClick={() => onNavigate('signup')}
                  className="px-6 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-medium hover:shadow-lg hover:scale-105 transition-all"
                >
                  Get Started
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
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Content */}
        <div className="max-w-7xl mx-auto px-4 pt-32 pb-20">
          <div className="text-center">
            <div className="inline-block mb-6">
              <span className="px-4 py-2 bg-indigo-100 dark:bg-indigo-900/50 text-indigo-700 dark:text-indigo-300 rounded-full text-sm font-medium">
                🎯 AI-Powered Personalization
              </span>
            </div>
            
            <h2 className="text-6xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
              Your Personal
              <br />
              <span className="bg-gradient-to-r from-indigo-600 to-purple-600 dark:from-indigo-400 dark:to-purple-400 bg-clip-text text-transparent">
                Recommendation Engine
              </span>
            </h2>
            
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-10 max-w-2xl mx-auto">
              Discover movies, music, products, and courses tailored just for you. 
              Powered by advanced AI and machine learning algorithms.
            </p>
            
            <div className="flex items-center justify-center space-x-4">
              <button
                onClick={() => onNavigate('signup')}
                className="flex items-center space-x-2 px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-medium hover:shadow-xl hover:scale-105 transition-all text-lg"
              >
                <span>Start Your Journey</span>
                <ArrowRight className="w-5 h-5" />
              </button>
              <button
                onClick={() => onNavigate('login')}
                className="px-8 py-4 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 rounded-xl font-medium hover:shadow-lg transition-all text-lg border border-gray-200 dark:border-gray-700"
              >
                Sign In
              </button>
            </div>

            {/* Stats */}
            <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-4xl font-bold text-indigo-600 dark:text-indigo-400 mb-2">{stat.number}</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Decorative Elements */}
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-300 dark:bg-purple-500 rounded-full mix-blend-multiply dark:mix-blend-normal filter blur-xl opacity-70 dark:opacity-20 animate-blob"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-indigo-300 dark:bg-indigo-500 rounded-full mix-blend-multiply dark:mix-blend-normal filter blur-xl opacity-70 dark:opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-20 left-1/2 w-72 h-72 bg-pink-300 dark:bg-pink-500 rounded-full mix-blend-multiply dark:mix-blend-normal filter blur-xl opacity-70 dark:opacity-20 animate-blob animation-delay-4000"></div>
      </header>

      {/* Domains Section */}
      <section className="py-20 bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h3 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              One Platform, Endless Possibilities
            </h3>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Get personalized recommendations across multiple domains
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {domains.map((domain, index) => {
              const Icon = domain.icon;
              return (
                <div
                  key={index}
                  className="group p-8 bg-gradient-to-br from-gray-50 to-white dark:from-gray-800 dark:to-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-all hover:scale-105"
                >
                  <div className={`w-16 h-16 bg-gradient-to-r ${domain.color} rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h4 className="text-xl font-bold text-gray-900 dark:text-white mb-2">{domain.name}</h4>
                  <p className="text-gray-600 dark:text-gray-400">{domain.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 dark:bg-gray-950">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h3 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Why Choose UniRec?
            </h3>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Powerful features designed to deliver the best recommendations
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div
                  key={index}
                  className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-md hover:shadow-xl transition-all border border-gray-100 dark:border-gray-700"
                >
                  <div className="w-12 h-12 bg-indigo-100 dark:bg-indigo-900/50 rounded-lg flex items-center justify-center mb-4">
                    <Icon className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
                  </div>
                  <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-2">{feature.title}</h4>
                  <p className="text-gray-600 dark:text-gray-400 text-sm">{feature.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-gradient-to-br from-indigo-50 to-purple-50 dark:from-gray-900 dark:to-indigo-950">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h3 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              How It Works
            </h3>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Get personalized recommendations in 3 simple steps
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                step: '1',
                title: 'Sign Up & Take Quiz',
                description: 'Create your account and complete a quick 6-question quiz about your preferences.',
                icon: Users
              },
              {
                step: '2',
                title: 'AI Analyzes Your Taste',
                description: 'Our machine learning algorithms process your answers to understand your unique preferences.',
                icon: Sparkles
              },
              {
                step: '3',
                title: 'Get Recommendations',
                description: 'Receive personalized suggestions for movies, music, products, and courses instantly.',
                icon: Star
              }
            ].map((item, index) => {
              const Icon = item.icon;
              return (
                <div key={index} className="text-center">
                  <div className="relative mb-6">
                    <div className="w-20 h-20 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-full flex items-center justify-center mx-auto">
                      <Icon className="w-10 h-10 text-white" />
                    </div>
                    <div className="absolute -top-2 w-12 h-12 bg-white dark:bg-gray-800 rounded-full flex items-center justify-center shadow-lg mx-auto left-0 right-0">
                      <span className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">{item.step}</span>
                    </div>
                  </div>
                  <h4 className="text-xl font-bold text-gray-900 dark:text-white mb-3">{item.title}</h4>
                  <p className="text-gray-600 dark:text-gray-400">{item.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-indigo-600 to-purple-600 dark:from-indigo-700 dark:to-purple-700">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h3 className="text-4xl font-bold text-white mb-6">
            Ready to Discover Your Perfect Matches?
          </h3>
          <p className="text-xl text-indigo-100 dark:text-indigo-200 mb-10">
            Join thousands of users who are already enjoying personalized recommendations
          </p>
          <div className="flex items-center justify-center space-x-4">
            <button
              onClick={() => onNavigate('signup')}
              className="flex items-center space-x-2 px-8 py-4 bg-white dark:bg-gray-900 text-indigo-600 dark:text-indigo-400 rounded-xl font-medium hover:shadow-2xl hover:scale-105 transition-all text-lg"
            >
              <span>Get Started Free</span>
              <ArrowRight className="w-5 h-5" />
            </button>
            <button
              onClick={() => onNavigate('login')}
              className="px-8 py-4 bg-indigo-800 dark:bg-indigo-900 text-white rounded-xl font-medium hover:bg-indigo-900 dark:hover:bg-black transition-all text-lg"
            >
              Sign In
            </button>
          </div>
          <p className="mt-6 text-indigo-200 dark:text-indigo-300 text-sm">
            No credit card required • Free forever • Cancel anytime
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-gray-900 dark:bg-black">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <span className="text-white font-bold text-lg">UniRec</span>
            </div>
            <p className="text-gray-400 dark:text-gray-500 text-sm">
              © 2025 UniRec. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
