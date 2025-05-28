import axios from "axios";
import { useEffect, useState } from "react";

interface Props {
  cinemaId: number;
  onClose: () => void;
}

interface CinemaRoom {
  id: number;
  room_number: number;
}

interface MaintenanceResponse {
  id: number;
  issue: string;
  complexity: number;
  handled_by_id: number;
  state: string;
  solved: boolean;
  cinema_room: number;
}

interface User {
  user_id: number;
  first_name: string;
  last_name: string;
  email: string;
  role: string;
  cinema_id: number;
  available: boolean;
}

export default function MaintenanceRequestModal({ cinemaId, onClose }: Props) {
  const [issue, setIssue] = useState("");
  const [complexity, setComplexity] = useState(1);
  const [rooms, setRooms] = useState<CinemaRoom[]>([]);
  const [selectedRoom, setSelectedRoom] = useState<number | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    axios
      .get(`http://localhost:8000/cinema/rooms/${cinemaId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      })
      .then((res) => setRooms(res.data))
      .catch((err) => console.error(err));
  }, [cinemaId]);

  const handleSubmit = async () => {
    try {
      const body = {
        issue,
        complexity,
        cinema_room: selectedRoom,
      };

      // 1. Crear solicitud de mantenimiento
      const createRes = await axios.post<MaintenanceResponse>(
        "http://localhost:8000/maintenance/request",
        body,
        {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        }
      );

      const requestId = createRes.data.id;

      // 2. Procesar solicitud automáticamente
      const processRes = await axios.put<MaintenanceResponse>(
        `http://localhost:8000/maintenance/request/process/${requestId}`,
        {},
        {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        }
      );

      const handledById = processRes.data.handled_by_id;

      // 3. Obtener datos del usuario asignado
      const userRes = await axios.get<User>(
        `http://localhost:8000/users/get/${handledById}`,
        {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        }
      );

      const user = userRes.data;

      // 4. Mostrar mensaje
      setMessage(
        `Mantenimiento asignado a usuario ${user.user_id} con rol ${user.role}`
      );

      setTimeout(() => {
        setMessage(null);
        onClose();
      }, 3000);
    } catch (error) {
      console.error(error);
      setMessage("Error al enviar o procesar la solicitud.");
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-xl font-bold text-blue-700 mb-4">
          Solicitar mantenimiento
        </h2>

        <label className="block mb-2 text-sm font-medium text-gray-700">
          Problema
        </label>
        <input
          type="text"
          className="w-full px-4 py-2 border rounded mb-4"
          value={issue}
          onChange={(e) => setIssue(e.target.value)}
        />

        <label className="block mb-2 text-sm font-medium text-gray-700">
          Complejidad
        </label>
        <select
          className="w-full px-4 py-2 border rounded mb-4"
          value={complexity}
          onChange={(e) => setComplexity(Number(e.target.value))}
        >
          {[1, 2, 3].map((level) => (
            <option key={level} value={level}>
              {level}
            </option>
          ))}
        </select>

        <label className="block mb-2 text-sm font-medium text-gray-700">
          Sala
        </label>
        <select
          className="w-full px-4 py-2 border rounded mb-4"
          value={selectedRoom ?? ""}
          onChange={(e) => setSelectedRoom(Number(e.target.value))}
        >
          <option value="" disabled>
            Selecciona una sala
          </option>
          {rooms.map((room) => (
            <option key={room.id} value={room.id}>
              Sala {room.room_number}
            </option>
          ))}
        </select>

        {message && (
          <p className="text-sm text-center text-blue-600 mb-2">{message}</p>
        )}

        <div className="flex justify-between">
          <button
            onClick={handleSubmit}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          >
            Enviar
          </button>
          <button
            onClick={onClose}
            className="bg-gray-300 hover:bg-gray-400 px-4 py-2 rounded"
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>
  );
}
