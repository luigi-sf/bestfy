import { Link } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "./hooks/useAuth";
import { Search } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { authService } from "../service/authService";

export default function TopBar() {
  const { user, isAuthenticated, logout} = useAuth();
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleLogout() {
  if (loading) return;

  setLoading(true);

  try {
    await authService.logout(); 
  } catch (err) {
    console.error("Erro ao fazer logout:", err);
  } finally {
    logout(); 
    navigate("/login");
  }
}

  return (
    <div className="flex items-center justify-between bg-black px-6 py-3 text-white">
      {/* Logo */}
      <Link to="/" className="text-xl font-bold">
        bestfy
      </Link>

      {/* Search */}
      <div className="flex items-center bg-zinc-800 rounded-full px-4 py-2 w-[40%]">
        <Search size={18} className="text-gray-400" />
        <input
          type="text"
          placeholder="O que você quer ouvir?"
          className="bg-transparent outline-none ml-2 w-full text-sm"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Right */}
      <div className="flex items-center gap-4">
        {isAuthenticated && user ? (
          <>
            <span className="text-sm">Olá, {user.name}</span>
            <button
              onClick={handleLogout}
              className="bg-green-500 hover:bg-green-400 text-black px-4 py-1 rounded-full text-sm font-semibold"
            >
              Sair
            </button>
          </>
        ) : (
          <>
            <Link to="/register" className="text-sm text-gray-300 hover:text-white">
              Inscrever-se
            </Link>
            <Link
              to="/login"
              className="bg-white text-black px-4 py-1 rounded-full text-sm font-semibold"
            >
              Entrar
            </Link>
          </>
        )}
      </div>
    </div>
  );
}