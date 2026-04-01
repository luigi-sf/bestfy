import { Routes, Route, Navigate } from "react-router-dom";

import LoginPage from "./pages/auth/login";
import SignupPage from "./pages/auth/signup";
import Home from "./pages/home";
import ArtistPage from "./pages/artist_page";
import AlbumPage from "./pages/album_page";

import AppLayout from "./assets/layout/topBar";
import PrivateRoute from "./components/private_route";


export default function App() {
  return (
    <Routes>
      {/* AUTH */}
      <Route path="/register" element={<SignupPage />} />
      <Route path="/login" element={<LoginPage />} />

      {/* PÚBLICO */}
      <Route element={<AppLayout />}>
        <Route path="/" element={<Home />} />
      </Route>

      {/* PROTEGIDO */}
      <Route
        element={
          <PrivateRoute>
            <AppLayout />
          </PrivateRoute>
        }
      >
        <Route path="/artist/:name" element={<ArtistPage />} />
        <Route path="/album/:name" element={<AlbumPage />} />
      </Route>

      {/* fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}