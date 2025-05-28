import { useState } from "react";
import MaintenanceRequestModal from "./MaintenanceRequestModal";
import MaintenanceListModal from "./MaintenanceListModal";

interface Cinema {
  id: number;
  name: string;
  address: string;
}

export default function CinemaCard({ cinema }: { cinema: Cinema }) {
  const [isRequestModalOpen, setRequestModalOpen] = useState(false);
  const [isListModalOpen, setListModalOpen] = useState(false);

  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      <h3 className="text-lg font-bold text-blue-700">{cinema.name}</h3>
      <p className="text-sm text-gray-600">{cinema.address}</p>

      <div className="mt-4 flex gap-2">
        <button
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          onClick={() => setRequestModalOpen(true)}
        >
          Pedir mantenimiento
        </button>

        <button
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
          onClick={() => setListModalOpen(true)}
        >
          Ver mantenimientos
        </button>
      </div>

      {isRequestModalOpen && (
        <MaintenanceRequestModal
          cinemaId={cinema.id}
          onClose={() => setRequestModalOpen(false)}
        />
      )}

      {isListModalOpen && (
        <MaintenanceListModal
          cinemaId={cinema.id}
          onClose={() => setListModalOpen(false)}
        />
      )}
    </div>
  );
}
