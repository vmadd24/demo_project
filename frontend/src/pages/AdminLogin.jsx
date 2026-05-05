import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { api } from "../api";
import { Wheat, Lock } from "lucide-react";

export default function AdminLogin() {
  const [email, setEmail] = useState("admin@bakery.com");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function submit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const { data } = await api.login(email, password);
      if (data.token) localStorage.setItem("bakery_token", data.token);
      localStorage.setItem("bakery_user", JSON.stringify({ email: data.email, name: data.name }));
      navigate("/admin");
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-bg flex flex-col" data-testid="admin-login-page">
      <header className="border-b border-line">
        <div className="max-w-7xl mx-auto px-6 lg:px-10 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2" data-testid="login-logo-link">
            <Wheat className="w-5 h-5 text-primary" strokeWidth={1.5} />
            <span className="serif text-xl font-bold text-ink">Maison Levain</span>
          </Link>
          <span className="text-xs uppercase tracking-[0.2em] text-sub">Admin</span>
        </div>
      </header>

      <div className="flex-1 flex items-center justify-center p-6">
        <div className="w-full max-w-md bg-surface border border-line rounded-2xl p-10 shadow-sm fade-up">
          <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-6">
            <Lock className="w-5 h-5 text-primary" strokeWidth={1.5} />
          </div>
          <h1 className="serif text-3xl font-bold text-ink mb-2">Welcome back</h1>
          <p className="text-sub mb-8">Sign in to manage the bakery.</p>

          <form onSubmit={submit} className="space-y-5">
            <label className="block">
              <span className="text-xs uppercase tracking-[0.2em] text-sub">Email</span>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="mt-2 w-full bg-bg border border-line rounded-xl px-4 py-3 text-ink focus:outline-none focus:border-primary"
                data-testid="login-email-input"
              />
            </label>
            <label className="block">
              <span className="text-xs uppercase tracking-[0.2em] text-sub">Password</span>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="mt-2 w-full bg-bg border border-line rounded-xl px-4 py-3 text-ink focus:outline-none focus:border-primary"
                data-testid="login-password-input"
              />
            </label>

            {error && (
              <div className="text-sm text-primary" data-testid="login-error">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary text-white hover:bg-primaryHover rounded-full py-3 font-medium transition-colors disabled:opacity-60"
              data-testid="login-submit-btn"
            >
              {loading ? "Signing in…" : "Sign in"}
            </button>
          </form>

          <div className="mt-8 text-xs text-sub border-t border-line pt-6">
            Default: <code className="text-ink">admin@bakery.com</code> / <code className="text-ink">admin123</code>
          </div>
        </div>
      </div>
    </div>
  );
}
