import axios from "axios";
import { useEffect, useState } from "react";

interface Movie {
  id: number;
  title: string;
  genre: string;
  duration: number;
  description: string;
}

interface Showtime {
  id: number;
  movie_id: number;
  cinema_room_id: number;
  showtime: string;
  day_of_week: string;
  movie?: Movie;
}

interface Occupancy {
  showtime_id: number;
  tickets_sold: number;
  room_capacity: number;
  occupancy_percentage: number;
  state: string;
  message: string;
}

export default function ShowtimeModal({
  cinemaId,
  onClose,
}: {
  cinemaId: number;
  onClose: () => void;
}) {
  const [showtimes, setShowtimes] = useState<Showtime[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [occupancyData, setOccupancyData] = useState<Record<number, Occupancy>>(
    {}
  );

  const fetchShowtimesWithMovies = async () => {
    try {
      setLoading(true);
      const { data: rawShowtimes } = await axios.get(
        `http://localhost:8000/movies/showtimes/${cinemaId}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      const showtimesWithMovies = await Promise.all(
        rawShowtimes.map(async (showtime: Showtime) => {
          try {
            const { data: movie } = await axios.get(
              `http://localhost:8000/movies/${showtime.movie_id}`,
              {
                headers: {
                  Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
              }
            );
            return { ...showtime, movie };
          } catch {
            return { ...showtime, movie: undefined };
          }
        })
      );

      setShowtimes(showtimesWithMovies);
    } catch (err: any) {
      if (err.response?.status === 404) {
        setError("No se encontraron funciones para este cine.");
      } else {
        setError("Error al cargar funciones.");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchShowtimesWithMovies();
  }, [cinemaId]);

  const handleSnapshot = async () => {
    try {
      await axios.post(
        `http://localhost:8000/movies/cinemas/${cinemaId}/save-snapshot`,
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      alert("Snapshot guardado correctamente.");
    } catch {
      alert("Error al guardar snapshot.");
    }
  };

  const handleRestore = async () => {
    try {
      await axios.post(
        `http://localhost:8000/movies/cinemas/${cinemaId}/restore-snapshot`,
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      alert("Snapshot restaurado correctamente.");
      await fetchShowtimesWithMovies();
    } catch {
      alert("Error al restaurar snapshot.");
    }
  };

  const handleDelete = async (showtimeId: number) => {
    try {
      await axios.delete(
        `http://localhost:8000/movies/showtime/${showtimeId}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      alert("Función eliminada correctamente.");
      await fetchShowtimesWithMovies();
    } catch {
      alert("Error al eliminar función.");
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

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center z-50 overflow-y-auto">
      <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-4xl max-h-[80vh] overflow-y-auto">
        <h2 className="text-xl font-bold text-blue-700 mb-4">
          Funciones del cine
        </h2>

        {/* Botones superiores */}
        <div className="flex gap-4 mb-4">
          <button
            onClick={handleSnapshot}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
          >
            Hacer snapshot de funciones
          </button>
          <button
            onClick={handleRestore}
            className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded"
          >
            Restaurar último snapshot
          </button>
        </div>

        {loading ? (
          <p className="text-gray-600">Cargando funciones...</p>
        ) : error ? (
          <p className="text-red-600">{error}</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {showtimes.map((show) => (
              <div key={show.id} className="border rounded p-4 shadow">
                <h3 className="font-bold text-blue-800">
                  {show.movie?.title ?? "Película no encontrada"}
                </h3>
                {show.movie ? (
                  <>
                    <p>
                      <strong>Género:</strong> {show.movie.genre}
                    </p>
                    <p>
                      <strong>Duración:</strong> {show.movie.duration} minutos
                    </p>
                    <p>{show.movie.description}</p>
                  </>
                ) : (
                  <p className="text-red-600">
                    No se pudo cargar información de la película.
                  </p>
                )}
                <hr className="my-2" />
                <p>
                  <strong>Día:</strong> {show.day_of_week}
                </p>
                <p>
                  <strong>Hora:</strong> {show.showtime}
                </p>
                <p>
                  <strong>Sala ID:</strong> {show.cinema_room_id}
                </p>

                <div className="mt-3 flex flex-col gap-2">
                  <button
                    onClick={() => handleDelete(show.id)}
                    className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded"
                  >
                    Eliminar función
                  </button>
                  <button
                    onClick={() => handleOccupancyCheck(show.id)}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white px-3 py-1 rounded"
                  >
                    Ver disponibilidad
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
