import React, { useState } from "react";

interface LoginFormProps {
  endpoint: string;
  onSuccess: (role: string) => void;
  loginType: string;
}

export const LoginForm: React.FC<LoginFormProps> = ({ endpoint, onSuccess, loginType }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        throw new Error("Credenciales inválidas");
      }

      const data = await res.json();
      const tokenData = JSON.parse(atob(data.access_token.split(".")[1]));
      const role = tokenData.role;
      localStorage.setItem("token", data.access_token);
      onSuccess(role);
    } catch (err: any) {
      setError(err.message || "Error al iniciar sesión");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-blue-50">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-md border border-blue-100"
      >
        <h2 className="text-2xl font-bold text-blue-700 mb-6 text-center">Login ({loginType})</h2>

        <div className="mb-4">
          <label className="block text-sm font-medium text-blue-800 mb-1" htmlFor="email">
            Correo electrónico
          </label>
          <input
            id="email"
            type="email"
            className="w-full p-2 border border-blue-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium text-blue-800 mb-1" htmlFor="password">
            Contraseña
          </label>
          <input
            id="password"
            type="password"
            className="w-full p-2 border border-blue-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {error && <p className="text-red-600 text-sm mb-4 text-center">{error}</p>}

        <button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
        >
          Iniciar sesión
        </button>
      </form>
    </div>
  );
};
