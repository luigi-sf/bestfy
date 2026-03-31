import { Outlet } from "react-router-dom";
import TopBar from "../../components/topBar";

export default function AppLayout() {
  return (
    <div className="app-layout">
      <TopBar />

      <div className="main-content">
        <main>
          <Outlet />
        </main>
      </div>
    </div>
  );
}