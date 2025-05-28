import { useEffect, useState } from "react";
import axios from "axios";

interface Cinema {
  id: number;
  name: string;
  address: string;
  phone: string;
  email: string;
}

export default function CinemaManagementPage() {
  const [cinemas, setCinemas] = useState<Cinema[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    axios
      .get("http://localhost:8000/cinema/", {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      })
      .then((res) => setCinemas(res.data))
      .catch((err) => {
        console.error(err);
        setError("Error al cargar los cines.");
      });
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-blue-800 mb-4">Gestionar Cines</h1>

      {error && <p className="text-red-600 text-sm">{error}</p>}

      {cinemas.length === 0 ? (
        <p className="text-gray-600">No hay cines registrados.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {cinemas.map((cinema) => (
            <div
              key={cinema.id}
              className="bg-white p-4 rounded shadow-md border border-gray-200"
            >
              <h3 className="text-lg font-bold text-blue-700">{cinema.name}</h3>
              <p className="text-sm text-gray-700">
                <strong>Dirección:</strong> {cinema.address}
              </p>
              <p className="text-sm text-gray-700">
                <strong>Teléfono:</strong> {cinema.phone}
              </p>
              <p className="text-sm text-gray-700">
                <strong>Email:</strong> {cinema.email}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
