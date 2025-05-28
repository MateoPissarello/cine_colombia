import { useNavigate } from "react-router-dom";

export default function ClientDashboard() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-green-50 flex flex-col items-center justify-center">
      <h1 className="text-3xl font-bold text-green-700 mb-6">Client Dashboard</h1>
      <button
        className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl shadow-md mb-4"
        onClick={() => navigate("/client/buy-tickets")}
      >
        Comprar Tickets
      </button>
      <button
        className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl shadow-md"
        onClick={() => navigate("/client/my-tickets")}
      >
        Ver mis Tickets
      </button>
    </div>
  );
}
