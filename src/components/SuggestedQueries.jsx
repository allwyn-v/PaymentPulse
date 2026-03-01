import React from 'react';
import { Lightbulb, Zap } from 'lucide-react';

const SUGGESTED_QUERIES = [
  "What is the average transaction amount for Food category?",
  "Show me peak hours for transactions",
  "Compare iOS vs Android transaction performance",
  "What is the failure rate across different categories?",
  "Show transactions flagged for fraud",
  "What are the top 5 states by transaction volume?",
  "Compare 5G vs WiFi network performance",
  "What's the distribution of transactions by age group?",
];

const SuggestedQueries = ({ onSelectQuery }) => {
  return (
    <div className="mb-6 animate-fade-in">
      <div className="flex items-center space-x-2 mb-4">
        <Lightbulb className="w-5 h-5 text-amber-400" />
        <h3 className="text-sm font-semibold text-gray-300">Try asking me...</h3>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {SUGGESTED_QUERIES.map((query, index) => (
          <button
            key={index}
            onClick={() => onSelectQuery(query)}
            className="group bg-slate-800/50 hover:bg-slate-800 text-left px-4 py-3 rounded-lg text-sm transition-all duration-200 hover:scale-105 border border-slate-700 hover:border-blue-500/50 hover:shadow-lg hover:shadow-blue-500/10"
          >
            <div className="flex items-start space-x-3">
              <Zap className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5 group-hover:animate-pulse" />
              <span className="text-gray-300 group-hover:text-white">{query}</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default SuggestedQueries;
