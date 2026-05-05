import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api";
import {
  Wheat,
  LogOut,
  Plus,
  Edit2,
  Trash2,
  Package,
  ClipboardList,
  X,
  Check,
} from "lucide-react";

const EMPTY_PRODUCT = {
  name: "",
  category: "Bread",
  price: 0,
  description: "",
  image_url: "",
  available: true,
};

export default function AdminDashboard() {
  const [tab, setTab] = useState("products");
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("bakery_user") || "{}");

  async function logout() {
    try {
      await api.logout();
    } catch (e) {}
    localStorage.removeItem("bakery_token");
    localStorage.removeItem("bakery_user");
    navigate("/admin/login");
  }

  return (
    <div className="min-h-screen bg-bg" data-testid="admin-dashboard">
      <header className="border-b border-line bg-surface">
        <div className="max-w-7xl mx-auto px-6 lg:px-10 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2" data-testid="dashboard-logo">
            <Wheat className="w-5 h-5 text-primary" strokeWidth={1.5} />
            <span className="serif text-xl font-bold text-ink">Maison Levain</span>
            <span className="text-xs uppercase tracking-[0.2em] text-sub ml-3 border-l border-line pl-3">
              Admin
            </span>
          </Link>
          <div className="flex items-center gap-4">
            <span className="text-sm text-sub hidden sm:inline" data-testid="admin-user">
              {user.email}
            </span>
            <button
              onClick={logout}
              className="inline-flex items-center gap-2 text-sm text-ink hover:text-primary transition-colors"
              data-testid="logout-btn"
            >
              <LogOut className="w-4 h-4" /> Sign out
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 lg:px-10 py-10">
        <div className="flex items-center gap-2 mb-8 border-b border-line" data-testid="dashboard-tabs">
          <TabButton
            active={tab === "products"}
            onClick={() => setTab("products")}
            icon={<Package className="w-4 h-4" />}
            label="Products"
            testId="tab-products"
          />
          <TabButton
            active={tab === "orders"}
            onClick={() => setTab("orders")}
            icon={<ClipboardList className="w-4 h-4" />}
            label="Orders"
            testId="tab-orders"
          />
        </div>

        {tab === "products" ? <ProductsPanel /> : <OrdersPanel />}
      </div>
    </div>
  );
}

function TabButton({ active, onClick, icon, label, testId }) {
  return (
    <button
      onClick={onClick}
      data-testid={testId}
      className={`inline-flex items-center gap-2 px-5 py-3 text-sm font-medium transition-colors border-b-2 -mb-px ${
        active
          ? "border-primary text-ink"
          : "border-transparent text-sub hover:text-ink"
      }`}
    >
      {icon} {label}
    </button>
  );
}

function ProductsPanel() {
  const [products, setProducts] = useState([]);
  const [editing, setEditing] = useState(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    const { data } = await api.listProducts();
    setProducts(data);
    setLoading(false);
  }

  useEffect(() => {
    load();
  }, []);

  async function handleDelete(id) {
    if (!window.confirm("Delete this product?")) return;
    await api.deleteProduct(id);
    load();
  }

  return (
    <div data-testid="products-panel">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="serif text-3xl font-bold text-ink">Products</h2>
          <p className="text-sub mt-1 text-sm">Manage the day's catalogue.</p>
        </div>
        <button
          onClick={() => setEditing({ ...EMPTY_PRODUCT })}
          className="inline-flex items-center gap-2 bg-primary text-white hover:bg-primaryHover rounded-full px-5 py-2.5 text-sm font-medium"
          data-testid="new-product-btn"
        >
          <Plus className="w-4 h-4" /> New product
        </button>
      </div>

      {loading ? (
        <div className="py-20 text-center text-sub">Loading…</div>
      ) : products.length === 0 ? (
        <div className="py-20 text-center text-sub border border-dashed border-line rounded-2xl">
          No products yet. Add your first bake.
        </div>
      ) : (
        <div className="bg-surface border border-line rounded-2xl overflow-hidden">
          <table className="w-full text-sm" data-testid="products-table">
            <thead className="bg-bg border-b border-line text-left">
              <tr>
                <th className="py-3 px-5 font-medium text-sub uppercase text-xs tracking-wider">Product</th>
                <th className="py-3 px-5 font-medium text-sub uppercase text-xs tracking-wider">Category</th>
                <th className="py-3 px-5 font-medium text-sub uppercase text-xs tracking-wider">Price</th>
                <th className="py-3 px-5 font-medium text-sub uppercase text-xs tracking-wider">Status</th>
                <th className="py-3 px-5"></th>
              </tr>
            </thead>
            <tbody>
              {products.map((p) => (
                <tr key={p.id} className="border-b border-line last:border-0" data-testid={`product-row-${p.id}`}>
                  <td className="py-3 px-5">
                    <div className="flex items-center gap-3">
                      {p.image_url && (
                        <img
                          src={p.image_url}
                          alt={p.name}
                          className="w-10 h-10 rounded-lg object-cover border border-line"
                        />
                      )}
                      <span className="font-medium text-ink">{p.name}</span>
                    </div>
                  </td>
                  <td className="py-3 px-5 text-sub">{p.category}</td>
                  <td className="py-3 px-5 serif text-ink">${p.price.toFixed(2)}</td>
                  <td className="py-3 px-5">
                    <span className={`text-xs uppercase tracking-wider px-2 py-1 rounded-full ${p.available ? "bg-sage/15 text-sage" : "bg-line text-sub"}`}>
                      {p.available ? "Available" : "Hidden"}
                    </span>
                  </td>
                  <td className="py-3 px-5 text-right">
                    <div className="inline-flex gap-1">
                      <button
                        onClick={() => setEditing(p)}
                        className="p-2 rounded-lg hover:bg-bg text-sub hover:text-ink transition-colors"
                        data-testid={`edit-product-${p.id}`}
                      >
                        <Edit2 className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(p.id)}
                        className="p-2 rounded-lg hover:bg-bg text-sub hover:text-primary transition-colors"
                        data-testid={`delete-product-${p.id}`}
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {editing && (
        <ProductEditor
          product={editing}
          onClose={() => setEditing(null)}
          onSaved={() => {
            setEditing(null);
            load();
          }}
        />
      )}
    </div>
  );
}

function ProductEditor({ product, onClose, onSaved }) {
  const [form, setForm] = useState(product);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const isNew = !product.id;

  async function save(e) {
    e.preventDefault();
    setError("");
    setSaving(true);
    try {
      const payload = {
        name: form.name,
        category: form.category,
        price: parseFloat(form.price),
        description: form.description || "",
        image_url: form.image_url || "",
        available: !!form.available,
      };
      if (isNew) await api.createProduct(payload);
      else await api.updateProduct(product.id, payload);
      onSaved();
    } catch (err) {
      const d = err.response?.data?.detail;
      setError(typeof d === "string" ? d : "Save failed");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 bg-ink/50 backdrop-blur-sm flex items-center justify-center p-4"
      onClick={onClose}
      data-testid="product-editor"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="bg-surface w-full max-w-lg rounded-2xl shadow-2xl fade-up max-h-[95vh] overflow-y-auto"
      >
        <form onSubmit={save} className="p-8">
          <div className="flex items-start justify-between mb-6">
            <h3 className="serif text-2xl text-ink font-bold">
              {isNew ? "New product" : "Edit product"}
            </h3>
            <button type="button" onClick={onClose} className="p-2 rounded-full hover:bg-line" data-testid="editor-close-btn">
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="space-y-4">
            <AdminField label="Name" value={form.name} onChange={(v) => setForm({ ...form, name: v })} required testId="product-name" />
            <div>
              <span className="text-xs uppercase tracking-[0.2em] text-sub">Category</span>
              <select
                value={form.category}
                onChange={(e) => setForm({ ...form, category: e.target.value })}
                className="mt-2 w-full bg-bg border border-line rounded-xl px-4 py-3 text-ink focus:outline-none focus:border-primary"
                data-testid="product-category"
              >
                <option>Bread</option>
                <option>Cake</option>
                <option>Pastry</option>
              </select>
            </div>
            <AdminField
              label="Price ($)"
              value={form.price}
              type="number"
              onChange={(v) => setForm({ ...form, price: v })}
              required
              testId="product-price"
            />
            <AdminField
              label="Image URL"
              value={form.image_url}
              onChange={(v) => setForm({ ...form, image_url: v })}
              testId="product-image-url"
            />
            <div>
              <span className="text-xs uppercase tracking-[0.2em] text-sub">Description</span>
              <textarea
                value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
                rows={3}
                className="mt-2 w-full bg-bg border border-line rounded-xl px-4 py-3 text-ink focus:outline-none focus:border-primary resize-none"
                data-testid="product-description"
              />
            </div>
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={!!form.available}
                onChange={(e) => setForm({ ...form, available: e.target.checked })}
                data-testid="product-available"
              />
              <span className="text-sm text-ink">Available on storefront</span>
            </label>
          </div>

          {error && <div className="mt-4 text-sm text-primary" data-testid="editor-error">{error}</div>}

          <button
            type="submit"
            disabled={saving}
            className="mt-6 w-full bg-primary text-white hover:bg-primaryHover rounded-full py-3 font-medium transition-colors disabled:opacity-60"
            data-testid="product-save-btn"
          >
            {saving ? "Saving…" : "Save product"}
          </button>
        </form>
      </div>
    </div>
  );
}

function AdminField({ label, value, onChange, required, type = "text", testId }) {
  return (
    <label className="block">
      <span className="text-xs uppercase tracking-[0.2em] text-sub">{label}</span>
      <input
        type={type}
        step={type === "number" ? "0.01" : undefined}
        value={value}
        required={required}
        onChange={(e) => onChange(e.target.value)}
        className="mt-2 w-full bg-bg border border-line rounded-xl px-4 py-3 text-ink focus:outline-none focus:border-primary"
        data-testid={testId}
      />
    </label>
  );
}

function OrdersPanel() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    const { data } = await api.listOrders();
    setOrders(data);
    setLoading(false);
  }
  useEffect(() => { load(); }, []);

  async function changeStatus(id, status) {
    await api.updateOrderStatus(id, status);
    load();
  }

  const STATUSES = ["pending", "confirmed", "completed", "cancelled"];

  return (
    <div data-testid="orders-panel">
      <div className="mb-6">
        <h2 className="serif text-3xl font-bold text-ink">Orders</h2>
        <p className="text-sub mt-1 text-sm">Every order placed through the storefront.</p>
      </div>

      {loading ? (
        <div className="py-20 text-center text-sub">Loading…</div>
      ) : orders.length === 0 ? (
        <div className="py-20 text-center text-sub border border-dashed border-line rounded-2xl" data-testid="orders-empty">
          No orders yet.
        </div>
      ) : (
        <div className="grid gap-4">
          {orders.map((o) => (
            <div key={o.id} className="bg-surface border border-line rounded-2xl p-6" data-testid={`order-card-${o.id}`}>
              <div className="flex flex-wrap items-start justify-between gap-4 mb-4">
                <div>
                  <div className="text-xs uppercase tracking-[0.2em] text-sub">
                    #{o.id.slice(0, 8)} · {new Date(o.created_at).toLocaleString()}
                  </div>
                  <div className="serif text-xl text-ink font-semibold mt-1">{o.customer_name}</div>
                  <div className="text-sm text-sub">{o.phone} · {o.address}</div>
                  {o.notes && <div className="text-sm text-sub italic mt-1">"{o.notes}"</div>}
                </div>
                <div className="text-right">
                  <div className="serif text-2xl text-ink font-bold">${o.total.toFixed(2)}</div>
                  <select
                    value={o.status}
                    onChange={(e) => changeStatus(o.id, e.target.value)}
                    className="mt-2 bg-bg border border-line rounded-full px-3 py-1 text-xs font-medium text-ink focus:outline-none focus:border-primary"
                    data-testid={`order-status-${o.id}`}
                  >
                    {STATUSES.map((s) => (
                      <option key={s} value={s}>{s}</option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="border-t border-line pt-4 space-y-1">
                {o.items.map((i, idx) => (
                  <div key={idx} className="flex justify-between text-sm">
                    <span className="text-ink">{i.quantity} × {i.product_name}</span>
                    <span className="text-sub">${(i.price * i.quantity).toFixed(2)}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
