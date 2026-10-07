import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  Home, Store, Send, Network, GitGraph, Users, PlayCircle, 
  ShieldAlert, RefreshCw, BarChart3, History, TestTube2, Settings 
} from 'lucide-react';

const navItems = [
  { path: '/', label: 'Home Overview', icon: Home },
  { path: '/marketplace', label: 'Agent Marketplace', icon: Store },
  { path: '/submit', label: 'Submit Objective', icon: Send },
  { path: '/tdg', label: 'Task Graph (TDG)', icon: Network },
  { path: '/actg', label: 'Capability Graph (ACTG)', icon: GitGraph },
  { path: '/team', label: 'Team Selection', icon: Users },
  { path: '/execution', label: 'Live Execution', icon: PlayCircle },
  { path: '/uncertainty', label: 'Uncertainty Gate', icon: ShieldAlert, highlight: 'rose' },
  { path: '/reorchestration', label: 'Re-Orchestration', icon: RefreshCw, highlight: 'rose' },
  { path: '/trust', label: 'Trust Analytics', icon: BarChart3 },
  { path: '/history', label: 'Execution History', icon: History },
  { path: '/evaluation', label: 'Benchmarks & Metrics', icon: TestTube2 },
  { path: '/admin', label: 'Agent Registry Admin', icon: Settings },
];

export const Navigation: React.FC = () => {
  return (
    <aside className="w-64 bg-white border-r border-lime-200/80 flex flex-col h-screen sticky top-0 z-40 shadow-xs">
      {/* Brand Header with Attached Project Logo */}
      <div className="p-4 border-b border-lime-100 flex items-center space-x-3 bg-gradient-to-r from-lime-50/50 to-white">
        <img 
          src="/zyra-logo.png" 
          alt="Zyra Mesh Logo" 
          className="w-10 h-10 object-contain rounded-xl shadow-xs border border-lime-200 bg-black p-0.5" 
        />
        <div>
          <h1 className="font-extrabold text-base text-slate-900 tracking-tight flex items-center gap-1.5 font-sans">
            ZYRA <span className="text-lime-700 text-[10px] px-1.5 py-0.5 rounded bg-lime-100 border border-lime-300 font-bold uppercase tracking-wider">MESH</span>
          </h1>
          <p className="text-[11px] text-slate-500 font-medium">Multi-Agent Marketplace</p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 overflow-y-auto p-3 space-y-1 scrollbar-thin">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isRose = item.highlight === 'rose';
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }: { isActive: boolean }) =>
                `flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-xs font-semibold transition-all ${
                  isActive
                    ? isRose
                      ? 'bg-rose-100/80 text-rose-900 border border-rose-300 shadow-xs font-bold'
                      : 'bg-lime-100/90 text-lime-950 border border-lime-300/80 shadow-xs font-bold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-lime-50/80'
                }`
              }
            >
              <Icon className={`w-4 h-4 ${isRose ? 'text-rose-600' : 'text-lime-600'}`} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
};


