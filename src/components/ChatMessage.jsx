import React from 'react';
import { Bot, User } from 'lucide-react';

const ChatMessage = ({ message }) => {
  const isUser = message.type === 'user';
  const isError = message.isError;

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-slide-up`}>
      <div className={`flex items-start space-x-3 max-w-2xl lg:max-w-3xl ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center text-white font-bold ${
          isUser 
            ? 'bg-gradient-to-r from-blue-600 to-cyan-600' 
            : 'bg-gradient-to-r from-slate-700 to-slate-600'
        }`}>
          {isUser ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
        </div>

        {/* Message Content */}
        <div className={`message-bubble ${isUser ? 'message-user' : 'message-ai'} ${
          isError ? 'border-2 border-red-500/50 bg-red-500/10' : ''
        }`}>
          <div className="markdown-content text-sm leading-relaxed">
            <MarkdownRenderer content={message.content} />
          </div>
          
          {/* Timestamp */}
          <div className={`mt-2 text-xs ${isUser ? 'text-blue-100' : 'text-gray-400'}`}>
            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        </div>
      </div>
    </div>
  );
};

const MarkdownRenderer = ({ content }) => {
  return (
    <div className="prose prose-invert max-w-none">
      {content.split('\n').map((line, index) => {
        // Handle bold text
        const boldRegex = /\*\*(.*?)\*\*/g;
        const parts = line.split(boldRegex);
        
        return (
          <div key={index} className={line.trim() === '' ? 'h-2' : ''}>
            {parts.map((part, i) => 
              i % 2 === 1 ? <strong key={i} className="text-blue-300 font-bold">{part}</strong> : part
            )}
          </div>
        );
      })}
    </div>
  );
};

export default ChatMessage;
