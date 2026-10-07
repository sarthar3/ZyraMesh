import React from 'react';
import { GitGraph, Network } from 'lucide-react';

interface GraphPlaceholderProps {
  title: string;
  type: 'TDG' | 'ACTG';
  nodesCount: number;
}

export const GraphPlaceholder: React.FC<GraphPlaceholderProps> = ({ title, type, nodesCount }) => {
  const isACTG = type === 'ACTG';
  return (
    <div className={`p-6 rounded-xl space-y-4 ${isACTG ? 'glass-panel-rose' : 'glass-panel'}`}>
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-slate-900 text-sm flex items-center space-x-2">
          {type === 'TDG' ? <Network className="w-4 h-4 text-lime-600" /> : <GitGraph className="w-4 h-4 text-rose-600" />}
          <span>{title}</span>
        </h3>
        <span className={`text-[10px] px-2.5 py-0.5 rounded-full font-semibold border ${
          isACTG ? 'bg-rose-50 text-rose-800 border-rose-200' : 'bg-lime-50 text-lime-800 border-lime-200'
        }`}>
          {nodesCount} Nodes Active
        </span>
      </div>

      <div className="h-64 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-500 font-sans text-xs font-medium">
        {type} Network Topology Visualization Subsystem
      </div>
    </div>
  );
};


