export const login = async (
  email: string,
  password: string,
  role: string
): Promise<string> => {
  const rolePath =
    role === "admin" || role === "cinema_admin" ? "admin" : "login";
  const response = await fetch(`http://localhost:8000/auth/${rolePath}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Login failed");
  }

  const data = await response.json();
  return data.access_token;
};
