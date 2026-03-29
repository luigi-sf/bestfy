import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./components/hooks/useAuth";

import LoginPage from "./pages/auth/login";
import SignupPage from "./pages/auth/signup";
import Home from "./pages/home";
import ArtistPage from "./pages/artist_page";
import AlbumPage from "./pages/album_page";

import AppLayout from "./assets/layout/topBar";


export default function App() {
  const { token } = useAuth();

  console.log("TOKEN:", token);

  return (
    <Routes>
      {/* 🔓 AUTH PAGES (sem proteção por token) */}
      <Route path="/register" element={<SignupPage />} />
      <Route path="/login" element={<LoginPage />} />

      {/* 🔐 APP PRINCIPAL */}
      <Route element={<AppLayout />}>
        <Route path="/" element={<Home />} />
        <Route path="/artist/:name" element={<ArtistPage />} />
        <Route path="/album/:name" element={<AlbumPage />} />
      </Route>

      {/* 🔁 fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}