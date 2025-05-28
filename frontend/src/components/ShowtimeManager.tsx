import { useEffect, useState } from "react";
import axios from "axios";
import ShowtimeModal from "./ShowtimeModal";
;

interface Cinema {
  id: number;
  name: string;
  address: string;
  phone: string;
  email: string;
}

export default function ShowtimeManager() {
  const [cinemas, setCinemas] = useState<Cinema[]>([]);
  const [selectedCinemaId, setSelectedCinemaId] = useState<number | null>(null);

  useEffect(() => {
    axios
      .get("http://localhost:8000/cinema/", {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      })
      .then((res) => setCinemas(res.data))
      .catch((err) => console.error("Error cargando cines:", err));
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold text-blue-700 mb-4">Gestionar Funciones</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cinemas.map((cinema) => (
          <div key={cinema.id} className="bg-white p-4 shadow rounded">
            <h3 className="text-lg font-bold text-blue-800">{cinema.name}</h3>
            <p>{cinema.address}</p>
            <p>{cinema.phone}</p>
            <p>{cinema.email}</p>
            <button
              className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
              onClick={() => setSelectedCinemaId(cinema.id)}
            >
              Ver funciones
            </button>
          </div>
        ))}
      </div>
      {selectedCinemaId && (
        <ShowtimeModal
          cinemaId={selectedCinemaId}
          onClose={() => setSelectedCinemaId(null)}
        />
      )}
    </div>
  );
}
