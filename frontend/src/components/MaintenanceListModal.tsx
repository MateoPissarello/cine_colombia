import axios from "axios";
import { useEffect, useState } from "react";

interface Props {
  cinemaId: number;
  onClose: () => void;
}

interface MaintenanceRequest {
  id: number;
  issue: string;
  complexity: number;
  handled_by_id: number;
  state: string;
  solved: boolean;
  cinema_room: number;
}

export default function MaintenanceListModal({ cinemaId, onClose }: Props) {
  const [requests, setRequests] = useState<MaintenanceRequest[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    axios
      .get(`http://localhost:8000/maintenance/requests/cinema/${cinemaId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      })
      .then((res) => setRequests(res.data))
      .catch((err) => {
        console.error(err);
        setError("Error al cargar mantenimientos.");
      });
  }, [cinemaId]);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-2xl max-h-[80vh] overflow-y-auto">
        <h2 className="text-xl font-bold text-blue-700 mb-4">
          Mantenimientos del cine
        </h2>

        {error && <p className="text-red-600 text-sm">{error}</p>}

        {requests.length === 0 ? (
          <p className="text-gray-600">No hay solicitudes registradas.</p>
        ) : (
          <ul className="space-y-3">
            {requests.map((req) => (
              <li
                key={req.id}
                className="border border-gray-300 p-4 rounded-md shadow-sm"
              >
                <p>
                  <strong>Problema:</strong> {req.issue}
                </p>
                <p>
                  <strong>Complejidad:</strong> {req.complexity}
                </p>
                <p>
                  <strong>Sala:</strong> {req.cinema_room}
                </p>
                <p>
                  <strong>Estado:</strong> {req.state}
                </p>
                <p>
                  <strong>Resuelto:</strong>{" "}
                  {req.solved ? "Sí" : "No"}
                </p>
                <p>
                  <strong>Asignado a usuario:</strong> {req.handled_by_id}
                </p>
              </li>
            ))}
          </ul>
        )}

        <div className="mt-4 text-right">
          <button
            onClick={onClose}
            className="bg-gray-300 hover:bg-gray-400 px-4 py-2 rounded"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
}
