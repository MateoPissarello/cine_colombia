import axios from "axios";
import { useEffect, useState } from "react";

interface Showtime {
  id: number;
  movie_id: number;
  cinema_room_id: number;
  showtime: string;
  day_of_week: string;
}

interface Occupancy {
  showtime_id: number;
  tickets_sold: number;
  room_capacity: number;
  occupancy_percentage: number;
  state: string;
  message: string;
}

export default function TicketModal({
  cinemaId,
  onClose,
}: {
  cinemaId: number;
  onClose: () => void;
}) {
  const [showtimes, setShowtimes] = useState<Showtime[]>([]);
  const [occupancyData, setOccupancyData] = useState<Record<number, Occupancy>>(
    {}
  );
  const [selectedShowtime, setSelectedShowtime] = useState<number | null>(null);
  const [tickets, setTickets] = useState(1);
  const [isAnonymous, setIsAnonymous] = useState(true);
  const [buyerName, setBuyerName] = useState("");
  const [buyerEmail, setBuyerEmail] = useState("");
  const [buyerPhone, setBuyerPhone] = useState("");

  const fetchShowtimes = async () => {
    try {
      const { data } = await axios.get(
        `http://localhost:8000/movies/showtimes/${cinemaId}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      setShowtimes(data);
    } catch {
      alert("Error al cargar funciones.");
    }
  };

  const handleOccupancyCheck = async (showtimeId: number) => {
    try {
      const { data } = await axios.get(
        `http://localhost:8000/occupancy/${showtimeId}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      setOccupancyData((prev) => ({ ...prev, [showtimeId]: data }));
    } catch {
      alert("Error al consultar disponibilidad.");
    }
  };

  const handleBuyTickets = async () => {
    if (!selectedShowtime) return;

    try {
      let payload: any = {
        showtime_id: selectedShowtime,
        tickets_sold: tickets,
      };

      if (isAnonymous) {
        payload = {
          ...payload,
          buyer_name: buyerName,
          buyer_email: buyerEmail,
          buyer_phone: buyerPhone,
        };
      } else {
        const { data } = await axios.get(
          "http://localhost:8000/users/get/my_info",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        );
        payload.user_id = data.user_id;
      }

      await axios.post("http://localhost:8000/ticket/buy", payload, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      alert("Compra realizada exitosamente.");
      setSelectedShowtime(null);
    } catch (err: any) {
      alert(
        `Error al realizar la compra: ${
          err.response?.data?.detail ?? "Error desconocido"
        }`
      );
    }
  };

  useEffect(() => {
    fetchShowtimes();
  }, [cinemaId]);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-start z-50 overflow-y-auto py-10">
      <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <h2 className="text-xl font-bold text-blue-700 mb-4">
          Funciones disponibles
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {showtimes.map((show) => (
            <div key={show.id} className="border rounded p-4 shadow">
              <p>
                <strong>Día:</strong> {show.day_of_week}
              </p>
              <p>
                <strong>Hora:</strong> {show.showtime}
              </p>
              <p>
                <strong>Sala ID:</strong> {show.cinema_room_id}
              </p>

              <div className="mt-2 flex flex-col gap-2">
                <button
                  onClick={() => handleOccupancyCheck(show.id)}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white px-3 py-1 rounded"
                >
                  Ver disponibilidad
                </button>
                <button
                  onClick={() => setSelectedShowtime(show.id)}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded"
                >
                  Comprar tickets
                </button>
              </div>

              {occupancyData[show.id] && (
                <div className="mt-3 text-sm bg-gray-100 p-2 rounded">
                  <p>
                    <strong>Entradas vendidas:</strong>{" "}
                    {occupancyData[show.id].tickets_sold}
                  </p>
                  <p>
                    <strong>Capacidad:</strong>{" "}
                    {occupancyData[show.id].room_capacity}
                  </p>
                  <p>
                    <strong>Ocupación:</strong>{" "}
                    {occupancyData[show.id].occupancy_percentage}%
                  </p>
                  <p>
                    <strong>Estado:</strong> {occupancyData[show.id].state}
                  </p>
                  <p>{occupancyData[show.id].message}</p>
                </div>
              )}
            </div>
          ))}
        </div>

        {selectedShowtime && (
          <div className="bg-white p-6 rounded-lg shadow-lg w-full mt-6 border border-gray-200">
            <h3 className="text-lg font-semibold text-blue-800 mb-2">
              Comprar tickets para función #{selectedShowtime}
            </h3>

            <label className="block mb-2">
              Cantidad de tickets:
              <input
                type="number"
                min={1}
                value={tickets}
                onChange={(e) => setTickets(Number(e.target.value))}
                className="border px-2 py-1 rounded w-full mt-1"
              />
            </label>

            <div className="flex items-center gap-4 my-2">
              <label className="flex items-center gap-2">
                <input
                  type="radio"
                  checked={isAnonymous}
                  onChange={() => setIsAnonymous(true)}
                />
                Compra anónima
              </label>
              <label className="flex items-center gap-2">
                <input
                  type="radio"
                  checked={!isAnonymous}
                  onChange={() => setIsAnonymous(false)}
                />
                Compra no anónima
              </label>
            </div>

            {isAnonymous && (
              <div className="space-y-2">
                <input
                  placeholder="Nombre"
                  value={buyerName}
                  onChange={(e) => setBuyerName(e.target.value)}
                  className="border px-2 py-1 rounded w-full"
                />
                <input
                  placeholder="Email"
                  type="email"
                  value={buyerEmail}
                  onChange={(e) => setBuyerEmail(e.target.value)}
                  className="border px-2 py-1 rounded w-full"
                />
                <input
                  placeholder="Teléfono"
                  value={buyerPhone}
                  onChange={(e) => setBuyerPhone(e.target.value)}
                  className="border px-2 py-1 rounded w-full"
                />
              </div>
            )}

            <div className="flex gap-3 mt-4">
              <button
                onClick={handleBuyTickets}
                className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
              >
                Confirmar compra
              </button>
              <button
                onClick={() => setSelectedShowtime(null)}
                className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded"
              >
                Cancelar
              </button>
            </div>
          </div>
        )}

        <button
          onClick={onClose}
          className="mt-6 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          Cerrar
        </button>
      </div>
    </div>
  );
}
