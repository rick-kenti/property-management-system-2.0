import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Properties from "./pages/Properties";
import Tenants from "./pages/Tenants";
import RentPayments from "./pages/RentPayments";

function AppLayout({ children }) {
  return (
    <div className="app-layout">
      <Navbar />
      <main className="main-content">{children}</main>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <AppLayout>
                  <Dashboard />
                </AppLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/properties"
            element={
              <ProtectedRoute>
                <AppLayout>
                  <Properties />
                </AppLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/tenants"
            element={
              <ProtectedRoute>
                <AppLayout>
                  <Tenants />
                </AppLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/rent-payments"
            element={
              <ProtectedRoute>
                <AppLayout>
                  <RentPayments />
                </AppLayout>
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
