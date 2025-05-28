import { useEffect, useState } from "react";
import axios from "axios";

interface Movie {
  id: number;
  title: string;
  genre: string;
  duration: number;
  description: string;
}

export default function MovieManager() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    axios
      .get("http://localhost:8000/movies/", {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      })
      .then((res) => setMovies(res.data))
      .catch((err) => {
        if (err.response?.status === 404) {
          setError("No se encontraron películas.");
        } else {
          setError("Error al cargar las películas.");
        }
      });
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold text-blue-700 mb-4">Gestor de Películas</h2>
      {error ? (
        <p className="text-red-600">{error}</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {movies.map((movie) => (
            <div key={movie.id} className="bg-white shadow-md rounded-lg p-4">
              <h3 className="text-lg font-bold text-blue-800">{movie.title}</h3>
              <p><strong>Género:</strong> {movie.genre}</p>
              <p><strong>Duración:</strong> {movie.duration} minutos</p>
              <p className="text-gray-700 mt-2">{movie.description}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
