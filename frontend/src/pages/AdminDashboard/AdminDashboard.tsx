import { useNavigate } from "react-router-dom";

export default function AdminDashboard() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-blue-50 flex flex-col items-center justify-center">
      <h1 className="text-3xl font-bold text-blue-700 mb-6">Admin Dashboard</h1>

      <div className="flex flex-col gap-4">
        <button
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl shadow-md"
          onClick={() => navigate("/admin/maintenance")}
        >
          Gestionar Mantenimientos
        </button>
        <button
          className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl shadow-md"
          onClick={() => navigate("/admin/cinemas")}
        >
          Gestionar Cines
        </button>

        <button
          className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl shadow-md"
          onClick={() => navigate("/admin/movies")}
        >
          Gestor de Películas
        </button>
        <button
          className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-3 rounded-xl shadow-md"
          onClick={() => navigate("/admin/showtimes")}
        >
          Gestionar Funciones
        </button>
      </div>
    </div>
  );
}
