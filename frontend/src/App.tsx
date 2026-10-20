import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { DashboardLayout } from './layouts/DashboardLayout';

// 14 Research Pages
import { HomePage } from './pages/HomePage';
import { MarketplacePage } from './pages/MarketplacePage';
import { AgentDetailPage } from './pages/AgentDetailPage';
import { TaskSubmissionPage } from './pages/TaskSubmissionPage';
import { TDGPage } from './pages/TDGPage';
import { ACTGPage } from './pages/ACTGPage';
import { TeamFormationPage } from './pages/TeamFormationPage';
import { LiveExecutionPage } from './pages/LiveExecutionPage';
import { UncertaintyGatePage } from './pages/UncertaintyGatePage';
import { ReOrchestrationPage } from './pages/ReOrchestrationPage';
import { TrustAnalyticsPage } from './pages/TrustAnalyticsPage';
import { WorkflowHistoryPage } from './pages/WorkflowHistoryPage';
import { EvaluationPage } from './pages/EvaluationPage';
import { AdminManagementPage } from './pages/AdminManagementPage';
import { DistillationStudioPage } from './pages/DistillationStudioPage';

export function App() {
  return (
    <Router>
      <DashboardLayout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/distill" element={<DistillationStudioPage />} />
          <Route path="/marketplace" element={<MarketplacePage />} />
          <Route path="/marketplace/:agentId" element={<AgentDetailPage />} />
          <Route path="/submit" element={<TaskSubmissionPage />} />
          <Route path="/tdg" element={<TDGPage />} />
          <Route path="/actg" element={<ACTGPage />} />
          <Route path="/team" element={<TeamFormationPage />} />
          <Route path="/execution" element={<LiveExecutionPage />} />
          <Route path="/uncertainty" element={<UncertaintyGatePage />} />
          <Route path="/reorchestration" element={<ReOrchestrationPage />} />
          <Route path="/trust" element={<TrustAnalyticsPage />} />
          <Route path="/history" element={<WorkflowHistoryPage />} />
          <Route path="/evaluation" element={<EvaluationPage />} />
          <Route path="/admin" element={<AdminManagementPage />} />
        </Routes>
      </DashboardLayout>
    </Router>
  );
}


export default App;
