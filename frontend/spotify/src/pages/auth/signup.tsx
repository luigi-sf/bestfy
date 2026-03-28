// src/pages/auth/SignupPage.tsx
import { useState } from "react"
import { useAuth } from "../../components/hooks/useAuth"
import { useNavigate, Link } from "react-router-dom"

export default function SignupPage() {
  const { signup, loading } = useAuth()
  const navigate = useNavigate()

  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setError("")

    if (!name || !email || !password) {
      setError("Preencha todos os campos.")
      return
    }

    const payload = { name, email, password }

    try {
      const success = await signup(payload)

      if (success) {
        navigate("/home")
      } else {
        setError("Erro ao criar conta.")
      }
    } catch (err) {
      console.error("Erro capturado no catch:", err)
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-black text-white">
      <div className="bg-zinc-900 p-8 rounded-lg w-full max-w-md shadow-lg">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold">bestfy</h1>
          <p className="text-gray-400">Crie sua conta</p>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Nome"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="bg-zinc-800 p-3 rounded-md outline-none focus:ring-2 focus:ring-green-500"
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
            className="bg-zinc-800 p-3 rounded-md outline-none focus:ring-2 focus:ring-green-500"
          />
          <input
            type="password"
            placeholder="Senha"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="new-password"
            className="bg-zinc-800 p-3 rounded-md outline-none focus:ring-2 focus:ring-green-500"
          />

          {error && <div className="text-red-500 text-sm">{error}</div>}

          <button
            type="submit"
            disabled={loading}
            className="bg-green-500 hover:bg-green-400 text-black font-semibold py-3 rounded-full mt-2"
          >
            {loading ? "Criando..." : "Criar conta"}
          </button>
        </form>

        <p className="text-sm text-gray-400 mt-6 text-center">
          Já tem conta?{" "}
          <Link to="/login" className="text-white underline">
            Entrar
          </Link>
        </p>
      </div>
    </div>
  )
}