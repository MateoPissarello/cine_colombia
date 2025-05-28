import { useNavigate } from "react-router-dom";
import { LoginForm } from "../../components/LoginForm";

const MaintenanceLogin = () => {
  const navigate = useNavigate();
  return (
    <LoginForm
      endpoint="http://localhost:8000/auth/maintenance/login"
      onSuccess={() => navigate("/maintenance/dashboard")}
      loginType="Maintenance"
    />
  );
};

export default MaintenanceLogin;
