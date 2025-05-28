import { useNavigate } from "react-router-dom";
import { LoginForm } from "../../components/LoginForm";

const ClientLogin = () => {
  const navigate = useNavigate();
  return (
    <LoginForm
      endpoint="http://localhost:8000/auth/client/login"
      onSuccess={() => navigate("/client/dashboard")}
      loginType="Client"
    />
  );
};

export default ClientLogin;
