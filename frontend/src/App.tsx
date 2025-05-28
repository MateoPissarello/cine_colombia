import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import CinemaManagementPage from "./components/CinemaManagementPage";
import MovieManager from "./components/MovieManager";
import ShowtimeManager from "./components/ShowtimeManager";
import TicketsManager from "./components/TicketsManager";
import "./index.css";
import AdminDashboard from "./pages/AdminDashboard/AdminDashboard";
import MaintenanceManager from "./pages/AdminDashboard/MaintenanceManager"; // <- Importa la nueva página
import CinemaAdminDashboard from "./pages/CinemaAdminDashboard";
import ClientDashboard from "./pages/ClientDashboard/ClientDashboard";
import MyTickets from "./pages/ClientDashboard/MyTickets";
import AdminLogin from "./pages/LoginPages/AdminLogin";
import ClientLogin from "./pages/LoginPages/ClientLogin";
import MaintenanceLogin from "./pages/LoginPages/MaintenanceLogin";
import MaintenanceDashboard from "./pages/MaintenanceDashboard";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/admin-login" element={<AdminLogin />} />
        <Route path="/maintenance-login" element={<MaintenanceLogin />} />
        <Route path="/client-login" element={<ClientLogin />} />
        <Route path="/admin/dashboard" element={<AdminDashboard />} />
        <Route
          path="/admin/maintenance"
          element={<MaintenanceManager />}
        />{" "}
        {/* <- Nueva ruta */}
        <Route
          path="/cinema-admin/dashboard"
          element={<CinemaAdminDashboard />}
        />
        <Route
          path="/maintenance/dashboard"
          element={<MaintenanceDashboard />}
        />
        <Route path="/client/dashboard" element={<ClientDashboard />} />
        <Route path="/admin/cinemas" element={<CinemaManagementPage />} />
        <Route path="/admin/movies" element={<MovieManager />} />
        <Route path="/admin/showtimes" element={<ShowtimeManager />} />
        <Route path="/client/buy-tickets" element={<TicketsManager />} />
        <Route path="/client/my-tickets" element={<MyTickets />} />
      </Routes>
    </Router>
  );
}

export default App;
