import React from 'react';

const StatsCard = ({ icon, label, value, color = 'blue' }) => {
  const colorClasses = {
    blue: 'from-blue-500/20 to-blue-600/20 border-blue-500/30 text-blue-400 bg-blue-500/10',
    green: 'from-green-500/20 to-green-600/20 border-green-500/30 text-green-400 bg-green-500/10',
    cyan: 'from-cyan-500/20 to-cyan-600/20 border-cyan-500/30 text-cyan-400 bg-cyan-500/10',
    purple: 'from-purple-500/20 to-purple-600/20 border-purple-500/30 text-purple-400 bg-purple-500/10',
  };

  return (
    <div className={`rounded-xl p-6 border bg-gradient-to-br ${colorClasses[color]} hover:scale-105 transition-all duration-300 cursor-pointer backdrop-blur`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-300 mb-2">{label}</p>
          <p className="text-3xl font-bold">{value}</p>
        </div>
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          {icon}
        </div>
      </div>
    </div>
  );
};

export default StatsCard;
