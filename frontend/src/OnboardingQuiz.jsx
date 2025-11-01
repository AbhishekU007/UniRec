import React, { useState } from 'react';
import { User, Film, Music, ShoppingCart, GraduationCap, ChevronRight, ChevronLeft } from 'lucide-react';

const OnboardingQuiz = ({ onComplete }) => {
  const [step, setStep] = useState(0);
  const [responses, setResponses] = useState({
    favorite_movie_genres: [],
    favorite_music_genres: [],
    shopping_interests: [],
    learning_topics: [],
    experience_level: 'beginner',
    budget_range: 'medium'
  });

  const questions = [
    {
      id: 'favorite_movie_genres',
      title: 'What movie genres do you enjoy?',
      subtitle: 'Select all that apply',
      icon: Film,
      type: 'multi-select',
      options: [
        'Action', 'Comedy', 'Drama', 'Horror', 'Romance',
        'Sci-Fi', 'Thriller', 'Documentary', 'Animation', 'Fantasy'
      ]
    },
    {
      id: 'favorite_music_genres',
      title: 'What music genres do you listen to?',
      subtitle: 'Select all that apply',
      icon: Music,
      type: 'multi-select',
      options: [
        'Pop', 'Rock', 'Hip Hop', 'Jazz', 'Classical',
        'Electronic', 'Country', 'R&B', 'Indie', 'Metal'
      ]
    },
    {
      id: 'shopping_interests',
      title: 'What do you usually shop for?',
      subtitle: 'Select your main interests',
      icon: ShoppingCart,
      type: 'multi-select',
      options: [
        'Electronics', 'Fashion', 'Books', 'Home & Garden', 'Sports',
        'Beauty', 'Toys', 'Food', 'Health', 'Automotive'
      ]
    },
    {
      id: 'learning_topics',
      title: 'What topics would you like to learn?',
      subtitle: 'Select areas of interest',
      icon: GraduationCap,
      type: 'multi-select',
      options: [
        'Programming', 'Business', 'Design', 'Marketing', 'Data Science',
        'Languages', 'Music', 'Photography', 'Finance', 'Health'
      ]
    },
    {
      id: 'experience_level',
      title: 'How would you describe your overall experience with online platforms?',
      subtitle: 'Choose one',
      icon: User,
      type: 'single-select',
      options: [
        { value: 'beginner', label: 'Beginner - Just getting started' },
        { value: 'intermediate', label: 'Intermediate - Comfortable navigating' },
        { value: 'advanced', label: 'Advanced - Power user' }
      ]
    },
    {
      id: 'budget_range',
      title: 'What\'s your typical spending preference?',
      subtitle: 'For products and services',
      icon: ShoppingCart,
      type: 'single-select',
      options: [
        { value: 'low', label: 'Budget-friendly' },
        { value: 'medium', label: 'Moderate' },
        { value: 'high', label: 'Premium' }
      ]
    }
  ];

  const currentQuestion = questions[step];
  const Icon = currentQuestion.icon;

  const handleMultiSelect = (option) => {
    const current = responses[currentQuestion.id] || [];
    if (current.includes(option)) {
      setResponses({
        ...responses,
        [currentQuestion.id]: current.filter(item => item !== option)
      });
    } else {
      setResponses({
        ...responses,
        [currentQuestion.id]: [...current, option]
      });
    }
  };

  const handleSingleSelect = (value) => {
    setResponses({
      ...responses,
      [currentQuestion.id]: value
    });
  };

  const canProceed = () => {
    const response = responses[currentQuestion.id];
    if (currentQuestion.type === 'multi-select') {
      return response && response.length > 0;
    }
    return response !== undefined && response !== '';
  };

  const handleNext = () => {
    if (step < questions.length - 1) {
      setStep(step + 1);
    } else {
      onComplete(responses);
    }
  };

  const handleBack = () => {
    if (step > 0) {
      setStep(step - 1);
    }
  };

  const progress = ((step + 1) / questions.length) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-600">
              Question {step + 1} of {questions.length}
            </span>
            <span className="text-sm font-medium text-indigo-600">
              {Math.round(progress)}% Complete
            </span>
          </div>
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-indigo-500 to-purple-600 transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Question Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
          <div className="flex items-center mb-6">
            <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mr-4">
              <Icon className="w-6 h-6 text-indigo-600" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{currentQuestion.title}</h2>
              <p className="text-gray-500">{currentQuestion.subtitle}</p>
            </div>
          </div>

          {/* Options */}
          <div className="space-y-3">
            {currentQuestion.type === 'multi-select' ? (
              <div className="grid grid-cols-2 gap-3">
                {currentQuestion.options.map((option) => {
                  const isSelected = (responses[currentQuestion.id] || []).includes(option);
                  return (
                    <button
                      key={option}
                      onClick={() => handleMultiSelect(option)}
                      className={`p-4 rounded-xl border-2 transition-all ${
                        isSelected
                          ? 'border-indigo-500 bg-indigo-50 text-indigo-700'
                          : 'border-gray-200 hover:border-indigo-300 text-gray-700'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-medium">{option}</span>
                        {isSelected && (
                          <div className="w-5 h-5 bg-indigo-500 rounded-full flex items-center justify-center">
                            <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                          </div>
                        )}
                      </div>
                    </button>
                  );
                })}
              </div>
            ) : (
              <div className="space-y-3">
                {currentQuestion.options.map((option) => {
                  const value = typeof option === 'string' ? option : option.value;
                  const label = typeof option === 'string' ? option : option.label;
                  const isSelected = responses[currentQuestion.id] === value;
                  return (
                    <button
                      key={value}
                      onClick={() => handleSingleSelect(value)}
                      className={`w-full p-4 rounded-xl border-2 transition-all text-left ${
                        isSelected
                          ? 'border-indigo-500 bg-indigo-50 text-indigo-700'
                          : 'border-gray-200 hover:border-indigo-300 text-gray-700'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-medium">{label}</span>
                        {isSelected && (
                          <div className="w-5 h-5 bg-indigo-500 rounded-full flex items-center justify-center">
                            <div className="w-2 h-2 bg-white rounded-full" />
                          </div>
                        )}
                      </div>
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        </div>

        {/* Navigation */}
        <div className="flex justify-between">
          <button
            onClick={handleBack}
            disabled={step === 0}
            className={`flex items-center px-6 py-3 rounded-lg font-medium transition-all ${
              step === 0
                ? 'opacity-50 cursor-not-allowed text-gray-400'
                : 'text-gray-700 hover:bg-white hover:shadow-md'
            }`}
          >
            <ChevronLeft className="w-5 h-5 mr-2" />
            Back
          </button>
          <button
            onClick={handleNext}
            disabled={!canProceed()}
            className={`flex items-center px-8 py-3 rounded-lg font-medium transition-all ${
              canProceed()
                ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:shadow-lg hover:scale-105'
                : 'bg-gray-200 text-gray-400 cursor-not-allowed'
            }`}
          >
            {step === questions.length - 1 ? 'Complete' : 'Next'}
            <ChevronRight className="w-5 h-5 ml-2" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default OnboardingQuiz;
