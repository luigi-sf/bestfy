import { useState } from "react";
import { useAuth } from "../../components/hooks/useAuth";
import { useNavigate, Link } from "react-router-dom";

export default function LoginPage() {
  const { login, loading } = useAuth();
  const navigate = useNavigate();

  // USESTATE
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");


  // FORMS
  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");

    if (!email || !password) {
      setError("Preencha todos os campos.");
      return;
    }

    try {
      const user = await login({ email, password });

      if (!user) {
        setError("Email ou senha inválidos.");
        return;
      }

      navigate("/home");
    } catch (err) {
      console.error(err);
      setError("Erro inesperado. Tente novamente.");
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-black text-white">
      <div className="bg-zinc-900 p-8 rounded-lg w-full max-w-md shadow-lg">
        <h1 className="text-3xl font-bold mb-2 text-center">bestfy</h1>
        <p className="text-center text-gray-400 mb-6">Acesse sua conta</p>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="email"
            placeholder="Digite seu email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
            className="bg-zinc-800 p-3 rounded-md outline-none focus:ring-2 focus:ring-green-500"
          />

          <input
            type="password"
            placeholder="Digite sua senha"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            className="bg-zinc-800 p-3 rounded-md outline-none focus:ring-2 focus:ring-green-500"
          />

          {error && <div className="text-red-500 text-sm">{error}</div>}

          <button
            type="submit"
            disabled={loading}
            className="bg-green-500 hover:bg-green-400 text-black font-semibold py-3 rounded-full transition-colors"
          >
            {loading ? "Entrando..." : "Entrar"}
          </button>
        </form>

        <p className="text-sm text-gray-400 mt-6 text-center">
          Não tem conta?{" "}
          <Link to="/register" className="text-white underline">
            Criar conta
          </Link>
        </p>
      </div>
    </div>
  );
}