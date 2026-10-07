import React from 'react';
import { Navigation } from '../components/Navigation';
import { ShieldCheck, Sparkles } from 'lucide-react';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  return (
    <div className="flex min-h-screen bg-[#f6f9f3] text-slate-800 font-sans">
      {/* Sidebar Navigation */}
      <Navigation />

      {/* Main Container */}
      <div className="flex-1 flex flex-col min-h-screen overflow-x-hidden">
        {/* Production Header */}
        <header className="bg-white/90 border-b border-lime-200/80 px-8 py-3 flex items-center justify-between sticky top-0 z-30 backdrop-blur-md shadow-xs">
          <div className="text-xs text-slate-600 font-semibold tracking-wide flex items-center gap-2">
            <span className="font-extrabold text-slate-900">Zyra Mesh</span>
            <span className="text-slate-300">|</span>
            <span className="text-slate-500 font-normal">Intelligent Multi-Agent Marketplace & Dynamic Orchestration Engine</span>
          </div>

          {/* Deploy Ready Platform Badge */}
          <div className="flex items-center space-x-3 text-xs font-sans">
            <div className="flex items-center space-x-1.5 bg-lime-50 text-lime-800 border border-lime-200 px-3 py-1 rounded-full font-bold shadow-xs">
              <ShieldCheck className="w-3.5 h-3.5 text-lime-600" />
              <span>Production Mesh v1.0</span>
            </div>
            <div className="hidden sm:flex items-center space-x-1.5 text-slate-500 font-medium px-2 py-1">
              <Sparkles className="w-3.5 h-3.5 text-amber-500" />
              <span>Bayesian Trust Enabled</span>
            </div>
          </div>
        </header>

        {/* Page Content Container */}
        <main className="flex-1 p-2">
          {children}
        </main>
      </div>
    </div>
  );
};



