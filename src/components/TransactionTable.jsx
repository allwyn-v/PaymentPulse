import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, CheckCircle2, XCircle } from 'lucide-react';

const TransactionTable = ({ data = [] }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  const mockTransactions = [
    { id: 'TXN000001', amount: 1500.50, category: 'Food', status: 'Success', date: '2024-02-28', device: 'iPhone' },
    { id: 'TXN000002', amount: 3200.00, category: 'Shopping', status: 'Success', date: '2024-02-28', device: 'Android' },
    { id: 'TXN000003', amount: 850.75, category: 'Entertainment', status: 'Failed', date: '2024-02-27', device: 'iPhone' },
    { id: 'TXN000004', amount: 5100.00, category: 'Utilities', status: 'Success', date: '2024-02-27', device: 'Android' },
    { id: 'TXN000005', amount: 420.25, category: 'Food', status: 'Success', date: '2024-02-26', device: 'iPhone' },
  ];

  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const paginatedData = mockTransactions.slice(startIndex, endIndex);

  return (
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
            {paginatedData.map((txn) => (
              <tr key={txn.id} className="hover:bg-slate-800/50 transition-colors">
                <td className="px-6 py-4 text-sm font-mono text-blue-400">{txn.id}</td>
                <td className="px-6 py-4 text-sm font-semibold text-green-400">₹{txn.amount.toFixed(2)}</td>
                <td className="px-6 py-4 text-sm text-gray-300">{txn.category}</td>
                <td className="px-6 py-4 text-sm">
                  <span className={`inline-flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-medium ${
                    txn.status === 'Success' 
                      ? 'bg-green-500/20 text-green-400' 
                      : 'bg-red-500/20 text-red-400'
                  }`}>
                    {txn.status === 'Success' ? (
                      <CheckCircle2 className="w-3 h-3" />
                    ) : (
                      <XCircle className="w-3 h-3" />
                    )}
                    <span>{txn.status}</span>
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-gray-400">{txn.date}</td>
                <td className="px-6 py-4 text-sm text-gray-300">{txn.device}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div className="px-6 py-4 border-t border-slate-800 flex items-center justify-between bg-slate-800/30">
        <p className="text-sm text-gray-400">Showing {startIndex + 1} to {Math.min(endIndex, mockTransactions.length)} of {mockTransactions.length} transactions</p>
        <div className="flex items-center space-x-2">
          <button 
            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
            disabled={currentPage === 1}
            className="p-2 text-sm border border-slate-700 rounded-lg hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="text-sm text-gray-400 px-3">Page {currentPage}</span>
          <button 
            onClick={() => setCurrentPage(prev => prev + 1)}
            disabled={endIndex >= mockTransactions.length}
            className="p-2 text-sm border border-slate-700 rounded-lg hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default TransactionTable;
