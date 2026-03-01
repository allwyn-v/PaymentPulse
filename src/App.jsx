import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { 
  Send, 
  Sparkles, 
  TrendingUp, 
  BarChart3, 
  Activity,
  MessageSquare,
  Loader2,
  ArrowUpRight,
  ArrowDownRight,
  DollarSign,
  Users,
  FileText,
  Search,
  Filter,
  Menu,
  X,
  Clock,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import ChatMessage from './components/ChatMessage';
import Visualization from './components/Visualization';
import StatsCard from './components/StatsCard';
import SuggestedQueries from './components/SuggestedQueries';
import TransactionTable from './components/TransactionTable';
import MetricsCard from './components/MetricsCard';

const API_BASE = '/api';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [isHealthy, setIsHealthy] = useState(false);
  const [activeTab, setActiveTab] = useState('chat'); // 'chat', 'dashboard', 'transactions'
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [transactions, setTransactions] = useState([]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    checkHealth();
    fetchStats();
    
    // Welcome message
    setMessages([{
      type: 'ai',
      content: "👋 Welcome to **PaymentPulse**! I'm your AI assistant for analyzing UPI transaction data.\n\nI can help you with:\n- Transaction patterns and trends\n- Success and failure rates\n- Category-wise analysis\n- Device and network comparisons\n- Fraud detection insights\n- Peak time analysis\n\nTry asking me something like *\"What's the average transaction amount for Food category?\"* or *\"Compare iOS vs Android performance\"*",
      timestamp: new Date()
    }]);
  }, []);

  const checkHealth = async () => {
    try {
      const response = await axios.get(`${API_BASE}/health`);
      setIsHealthy(response.data.status === 'healthy');
    } catch (error) {
      console.error('Health check failed:', error);
      setIsHealthy(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE}/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || loading) return;

    const userMessage = {
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE}/query`, {
        query: inputValue,
        history: messages.slice(-5) // Send last 5 messages for context
      });

      const aiMessage = {
        type: 'ai',
        content: response.data.response.answer,
        data: response.data.response.data,
        visualization: response.data.response.visualization,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = {
        type: 'ai',
        content: `❌ Sorry, I encountered an error: ${error.response?.data?.error || error.message}. Please try again.`,
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSuggestedQuery = (query) => {
    setInputValue(query);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Sidebar Navigation */}
      <div className={`fixed left-0 top-0 h-screen bg-slate-900 border-r border-slate-800 transition-all duration-300 z-40 ${
        sidebarOpen ? 'w-64' : 'w-20'
      }`}>
        <div className="p-4 border-b border-slate-800">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg">
              <Sparkles className="w-6 h-6" />
            </div>
            {sidebarOpen && (
              <div>
                <h1 className="text-xl font-bold">PaymentPulse</h1>
                <p className="text-xs text-gray-400">Analytics</p>
              </div>
            )}
          </div>
        </div>

        <nav className="p-4 space-y-2">
          {[
            { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
            { id: 'chat', label: 'Chat', icon: MessageSquare },
            { id: 'transactions', label: 'Transactions', icon: FileText },
          ].map(item => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${
                  activeTab === item.id
                    ? 'bg-gradient-to-r from-blue-500/20 to-cyan-500/20 border border-blue-500/30 text-blue-400'
                    : 'text-gray-400 hover:bg-slate-800'
                }`}
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                {sidebarOpen && <span>{item.label}</span>}
              </button>
            );
          })}
        </nav>

        <div className="absolute bottom-4 left-4 right-4 p-3 bg-slate-800/50 rounded-lg border border-slate-700">
          <div className={`flex items-center ${sidebarOpen ? 'space-x-2' : 'justify-center'}`}>
            <div className={`w-2 h-2 rounded-full ${isHealthy ? 'bg-green-500' : 'bg-red-500'} animate-pulse`} />
            {sidebarOpen && (
              <span className="text-xs text-gray-400">{isHealthy ? 'Online' : 'Offline'}</span>
            )}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className={`transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-20'}`}>
        {/* Top Header */}
        <header className="bg-slate-900/50 backdrop-blur border-b border-slate-800 sticky top-0 z-30">
          <div className="px-6 py-4 flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
              >
                {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </button>
              <h2 className="text-xl font-bold capitalize">{activeTab}</h2>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="hidden md:flex items-center bg-slate-800 border border-slate-700 rounded-lg px-3 py-2">
                <Search className="w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search..."
                  className="bg-transparent ml-2 text-sm focus:outline-none text-white placeholder-gray-500"
                />
              </div>
            </div>
          </div>
        </header>

        {/* Dashboard View */}
        {activeTab === 'dashboard' && (
          <div className="p-6 space-y-6">
            {/* Key Metrics */}
            {stats && (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <MetricsCard
                    title="Total Transactions"
                    value={stats.total_transactions?.toLocaleString()}
                    icon={Activity}
                    trend={12}
                    color="blue"
                  />
                  <MetricsCard
                    title="Total Volume"
                    value={`₹${(stats.total_volume / 1000000).toFixed(2)}M`}
                    icon={DollarSign}
                    trend={8}
                    color="green"
                  />
                  <MetricsCard
                    title="Success Rate"
                    value={`${stats.success_rate?.toFixed(1)}%`}
                    icon={TrendingUp}
                    trend={3}
                    color="cyan"
                  />
                  <MetricsCard
                    title="Avg Transaction"
                    value={`₹${stats.avg_transaction?.toFixed(0)}`}
                    icon={BarChart3}
                    trend={-2}
                    color="purple"
                  />
                </div>

                {/* Charts Section */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="text-lg font-semibold mb-4">Transaction Trends</h3>
                    <div className="h-64 flex items-center justify-center text-gray-400">
                      <p>Chart visualization goes here</p>
                    </div>
                  </div>

                  <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="text-lg font-semibold mb-4">Category Distribution</h3>
                    <div className="h-64 flex items-center justify-center text-gray-400">
                      <p>Chart visualization goes here</p>
                    </div>
                  </div>
                </div>

                {/* Recent Activity */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                  <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
                  <div className="space-y-3">
                    {[1, 2, 3].map(i => (
                      <div key={i} className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <div className="p-2 bg-blue-500/20 rounded-lg">
                            <CheckCircle2 className="w-4 h-4 text-blue-400" />
                          </div>
                          <div>
                            <p className="text-sm font-medium">Transaction processed</p>
                            <p className="text-xs text-gray-400">2 hours ago</p>
                          </div>
                        </div>
                        <span className="text-sm font-semibold text-green-400">+₹1,234</span>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            )}
          </div>
        )}

        {/* Chat View */}
        {activeTab === 'chat' && (
          <div className="p-6 flex flex-col h-[calc(100vh-100px)]">
            <div className="flex-1 overflow-y-auto space-y-4 mb-6">
              {messages.map((message, index) => (
                <div key={index}>
                  <ChatMessage message={message} />
                  {message.visualization && (
                    <div className="mt-4 animate-slide-up">
                      <Visualization data={message.visualization} />
                    </div>
                  )}
                </div>
              ))}
              
              {loading && (
                <div className="flex justify-start animate-fade-in">
                  <div className="bg-slate-800 border border-slate-700 rounded-lg p-4">
                    <div className="flex items-center space-x-2">
                      <Loader2 className="w-4 h-4 animate-spin text-blue-400" />
                      <span className="text-sm">Analyzing data...</span>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>

            {messages.length === 1 && (
              <SuggestedQueries onSelectQuery={handleSuggestedQuery} />
            )}

            {/* Input Area */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="flex items-end space-x-3">
                <div className="flex-1">
                  <textarea
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask me anything about the transaction data..."
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                    rows="2"
                    disabled={loading || !isHealthy}
                  />
                </div>
                <button
                  onClick={handleSendMessage}
                  disabled={loading || !inputValue.trim() || !isHealthy}
                  className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold px-6 py-3 rounded-lg transition-all flex items-center space-x-2"
                >
                  {loading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <Send className="w-5 h-5" />
                  )}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Transactions View */}
        {activeTab === 'transactions' && (
          <div className="p-6">
            <div className="mb-6 flex items-center justify-between">
              <h3 className="text-2xl font-bold">Transaction History</h3>
              <button className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white px-6 py-2 rounded-lg flex items-center space-x-2">
                <Filter className="w-4 h-4" />
                <span>Filter</span>
              </button>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-slate-800 bg-slate-800/50">
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Transaction ID</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Amount</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Category</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Status</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Date</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Device</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800">
                    {[1, 2, 3, 4, 5].map(i => (
                      <tr key={i} className="hover:bg-slate-800/50 transition-colors">
                        <td className="px-6 py-4 text-sm font-mono text-blue-400">#TXN{i.toString().padStart(6, '0')}</td>
                        <td className="px-6 py-4 text-sm font-semibold text-green-400">₹{(Math.random() * 10000).toFixed(2)}</td>
                        <td className="px-6 py-4 text-sm text-gray-300">Food</td>
                        <td className="px-6 py-4 text-sm">
                          <span className="inline-flex items-center space-x-1 px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-xs font-medium">
                            <CheckCircle2 className="w-3 h-3" />
                            <span>Success</span>
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-400">2024-02-{String(i).padStart(2, '0')}</td>
                        <td className="px-6 py-4 text-sm text-gray-300">iPhone</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              
              <div className="px-6 py-4 border-t border-slate-800 flex items-center justify-between">
                <p className="text-sm text-gray-400">Showing 1 to 5 of 100 transactions</p>
                <div className="flex items-center space-x-2">
                  <button className="px-3 py-2 text-sm border border-slate-700 rounded-lg hover:bg-slate-800">Previous</button>
                  <button className="px-3 py-2 text-sm bg-blue-600 rounded-lg">1</button>
                  <button className="px-3 py-2 text-sm border border-slate-700 rounded-lg hover:bg-slate-800">2</button>
                  <button className="px-3 py-2 text-sm border border-slate-700 rounded-lg hover:bg-slate-800">Next</button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
