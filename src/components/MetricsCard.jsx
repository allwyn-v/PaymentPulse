import React from 'react';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';

const MetricsCard = ({ title, value, icon: Icon, trend, color }) => {
  const colorMap = {
    blue: 'from-blue-500/20 to-blue-600/20 border-blue-500/30',
    green: 'from-green-500/20 to-green-600/20 border-green-500/30',
    cyan: 'from-cyan-500/20 to-cyan-600/20 border-cyan-500/30',
    purple: 'from-purple-500/20 to-purple-600/20 border-purple-500/30',
  };

  const iconColorMap = {
    blue: 'bg-blue-500/20 text-blue-400',
    green: 'bg-green-500/20 text-green-400',
    cyan: 'bg-cyan-500/20 text-cyan-400',
    purple: 'bg-purple-500/20 text-purple-400',
  };

  return (
    <div className={`bg-gradient-to-br ${colorMap[color]} border rounded-xl p-6 backdrop-blur`}>
      <div className="flex items-start justify-between mb-4">
        <div className={`p-3 rounded-lg ${iconColorMap[color]}`}>
          <Icon className="w-6 h-6" />
        </div>
        <div className={`flex items-center space-x-1 text-sm font-semibold ${
          trend > 0 ? 'text-green-400' : 'text-red-400'
        }`}>
          {trend > 0 ? (
            <ArrowUpRight className="w-4 h-4" />
          ) : (
            <ArrowDownRight className="w-4 h-4" />
          )}
          <span>{Math.abs(trend)}%</span>
        </div>
      </div>

      <div>
        <p className="text-sm text-gray-400 mb-1">{title}</p>
        <p className="text-3xl font-bold">{value}</p>
      </div>
    </div>
  );
};

export default MetricsCard;
