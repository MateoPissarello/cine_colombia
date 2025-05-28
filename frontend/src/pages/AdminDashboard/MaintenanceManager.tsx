import axios from "axios";
import { useEffect, useState } from "react";
import CinemaCard from "../../components/CinemaCard";

interface Cinema {
  id: number;
  name: string;
  address: string;
}

export default function MaintenanceManager() {
  const [cinemas, setCinemas] = useState<Cinema[]>([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/cinema/", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
      .then((res) => setCinemas(res.data))
      .catch(console.error);
  }, []);

  return (
    <div className="p-8 bg-blue-50 min-h-screen">
      <h2 className="text-2xl font-semibold text-blue-800 mb-6">
        Gestionar Mantenimientos
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {cinemas.map((cinema) => (
          <CinemaCard key={cinema.id} cinema={cinema} />
        ))}
      </div>
    </div>
  );
}
