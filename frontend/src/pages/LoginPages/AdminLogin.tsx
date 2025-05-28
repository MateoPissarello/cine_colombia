import { useNavigate } from "react-router-dom";
import { LoginForm } from "../../components/LoginForm";

const AdminLogin = () => {
  const navigate = useNavigate();

  const handleLoginSuccess = (role: string) => {
    if (role === "admin") navigate("/admin/dashboard");
    else if (role === "cinema_admin") navigate("/cinema-admin/dashboard");
  };

  return (
    <LoginForm
      endpoint="http://localhost:8000/auth/admin/login"
      onSuccess={handleLoginSuccess}
      loginType="Admin"
    />
  );
};

export default AdminLogin;
