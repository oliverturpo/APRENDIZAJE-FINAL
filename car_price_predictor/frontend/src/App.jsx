import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LayoutTailwind from './components/LayoutTailwind';
import Home from './components/Home';
import DashboardTailwind from './components/DashboardTailwind';
import PredictForm from './components/PredictForm';
import Results from './components/Results';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Home page without sidebar */}
        <Route path="/" element={<Home />} />

        {/* App pages with sidebar */}
        <Route element={<LayoutTailwind />}>
          <Route path="/dashboard" element={<DashboardTailwind />} />
          <Route path="/predictor" element={<PredictForm />} />
          <Route path="/results" element={<Results />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
