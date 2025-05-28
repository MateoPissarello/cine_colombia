import { useEffect, useState } from "react";
import axios from "axios";

interface Ticket {
  id: number;
  showtime_id: number;
  tickets_sold: number;
  user_id: number | null;
  buyer_name: string | null;
  buyer_email: string | null;
  buyer_phone: string | null;
  purchase_time: string;
}

export default function MyTickets() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    axios
      .get("http://localhost:8000/ticket/my/tickets", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
      .then((res) => setTickets(res.data))
      .catch((err) => {
        setError("Error al cargar los tickets");
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-green-50 p-6">
      <h1 className="text-2xl font-bold text-green-700 mb-6">Mis Tickets</h1>

      {loading ? (
        <p className="text-gray-600">Cargando tickets...</p>
      ) : error ? (
        <p className="text-red-600">{error}</p>
      ) : tickets.length === 0 ? (
        <p className="text-gray-700">No has comprado tickets aún.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {tickets.map((ticket) => (
            <div key={ticket.id} className="bg-white shadow p-4 rounded-lg">
              <p>
                <strong>ID Ticket:</strong> {ticket.id}
              </p>
              <p>
                <strong>Showtime ID:</strong> {ticket.showtime_id}
              </p>
              <p>
                <strong>Cantidad:</strong> {ticket.tickets_sold}
              </p>
              {ticket.buyer_name && (
                <p>
                  <strong>Comprador:</strong> {ticket.buyer_name}
                </p>
              )}
              {ticket.buyer_email && (
                <p>
                  <strong>Email:</strong> {ticket.buyer_email}
                </p>
              )}
              {ticket.buyer_phone && (
                <p>
                  <strong>Teléfono:</strong> {ticket.buyer_phone}
                </p>
              )}
              <p>
                <strong>Fecha de compra:</strong>{" "}
                {new Date(ticket.purchase_time).toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
