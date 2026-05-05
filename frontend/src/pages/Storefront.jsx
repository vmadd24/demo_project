import React, { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import {
  Wheat,
  Clock,
  MapPin,
  ShoppingBag,
  Instagram,
  ArrowRight,
  X,
  Check,
  Minus,
  Plus,
} from "lucide-react";

const HERO_IMG =
  "https://static.prod-images.emergentagent.com/jobs/76d30b1d-406d-41e3-8062-be2acd104d8d/images/345e083bd24f52fe67d897db156ec6254e227acb1f02f2add2415f36346d8970.png";

const CATEGORIES = ["All", "Bread", "Cake", "Pastry"];

function Header() {
  return (
    <header
      className="sticky top-0 z-40 backdrop-blur-xl bg-bg/80 border-b border-line"
      data-testid="site-header"
    >
      <div className="max-w-7xl mx-auto px-6 lg:px-10 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2" data-testid="logo-link">
          <Wheat className="w-5 h-5 text-primary" strokeWidth={1.5} />
          <span className="serif text-xl font-bold tracking-tight text-ink">
            Maison Levain
          </span>
        </Link>
        <nav className="hidden md:flex items-center gap-10 text-sm text-sub font-medium">
          <a href="#catalog" className="hover:text-primary transition-colors" data-testid="nav-catalog">
            Catalogue
          </a>
          <a href="#story" className="hover:text-primary transition-colors" data-testid="nav-story">
            Our Story
          </a>
          <a href="#visit" className="hover:text-primary transition-colors" data-testid="nav-visit">
            Visit
          </a>
        </nav>
        <Link
          to="/admin/login"
          className="text-xs uppercase tracking-[0.2em] text-sub hover:text-primary transition-colors"
          data-testid="admin-link"
        >
          Admin
        </Link>
      </div>
    </header>
  );
}

function Hero() {
  return (
    <section
      className="relative overflow-hidden border-b border-line"
      data-testid="hero-section"
    >
      <div className="max-w-7xl mx-auto px-6 lg:px-10 pt-16 pb-24 lg:pt-24 lg:pb-32 grid grid-cols-1 lg:grid-cols-12 gap-10 items-end">
        <div className="lg:col-span-6 fade-up">
          <div className="text-xs font-sans uppercase tracking-[0.3em] text-sub mb-8">
            Est. 2014 · Portland, OR
          </div>
          <h1 className="serif text-5xl sm:text-6xl lg:text-7xl font-black text-ink leading-[0.95] tracking-tighter">
            Slow bread,<br />
            <span className="italic font-serif text-primary">honest</span> craft.
          </h1>
          <p className="mt-8 text-lg text-sub leading-relaxed max-w-lg">
            We wake at 3 a.m. to shape every loaf by hand. Stone-milled flour,
            wild starters, and patience — nothing more.
          </p>
          <div className="mt-10 flex flex-wrap gap-4">
            <a
              href="#catalog"
              className="bg-primary text-white hover:bg-primaryHover rounded-full px-8 py-3 font-medium transition-colors shadow-md inline-flex items-center gap-2"
              data-testid="hero-order-btn"
            >
              Order today's bake <ArrowRight className="w-4 h-4" />
            </a>
            <a
              href="#story"
              className="bg-transparent text-ink border border-ink hover:bg-ink hover:text-bg rounded-full px-8 py-3 font-medium transition-colors"
              data-testid="hero-story-btn"
            >
              Our philosophy
            </a>
          </div>
          <div className="mt-16 flex items-center gap-10 text-sm text-sub">
            <div>
              <div className="serif text-3xl text-ink">11</div>
              <div className="uppercase tracking-widest text-xs">years baking</div>
            </div>
            <div className="w-px h-10 bg-line" />
            <div>
              <div className="serif text-3xl text-ink">3am</div>
              <div className="uppercase tracking-widest text-xs">ovens on</div>
            </div>
            <div className="w-px h-10 bg-line" />
            <div>
              <div className="serif text-3xl text-ink">100%</div>
              <div className="uppercase tracking-widest text-xs">hand-shaped</div>
            </div>
          </div>
        </div>
        <div className="lg:col-span-6 fade-up" style={{ animationDelay: "150ms" }}>
          <div className="relative rounded-2xl overflow-hidden shadow-xl">
            <img
              src={HERO_IMG}
              alt="Inside Maison Levain bakery"
              className="w-full h-[60vh] lg:h-[70vh] object-cover"
              data-testid="hero-image"
            />
            <div className="absolute bottom-6 left-6 right-6 bg-bg/95 backdrop-blur-sm rounded-xl p-5 flex items-center justify-between">
              <div>
                <div className="text-xs uppercase tracking-[0.2em] text-sub">
                  Today's special
                </div>
                <div className="serif text-xl text-ink mt-1">
                  Honey Walnut Loaf
                </div>
              </div>
              <a
                href="#catalog"
                className="text-primary font-medium inline-flex items-center gap-1 hover:gap-2 transition-all"
                data-testid="hero-special-link"
              >
                View <ArrowRight className="w-4 h-4" />
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function ProductCard({ product, onOrder }) {
  return (
    <article
      className="group bg-surface rounded-2xl border border-line overflow-hidden hover:-translate-y-1 hover:shadow-lg transition-all duration-300"
      data-testid={`product-card-${product.id}`}
    >
      <div className="aspect-[4/3] overflow-hidden bg-line">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-sub">
            <Wheat className="w-10 h-10" strokeWidth={1.5} />
          </div>
        )}
      </div>
      <div className="p-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs uppercase tracking-[0.2em] text-sage font-medium">
            {product.category}
          </span>
          <span className="serif text-lg text-ink font-semibold">
            ${product.price.toFixed(2)}
          </span>
        </div>
        <h3 className="serif text-xl text-ink font-semibold mb-2">
          {product.name}
        </h3>
        <p className="text-sm text-sub leading-relaxed mb-5 line-clamp-2">
          {product.description}
        </p>
        <button
          onClick={() => onOrder(product)}
          disabled={!product.available}
          className="w-full bg-ink text-bg hover:bg-primary rounded-full py-3 font-medium transition-colors inline-flex items-center justify-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
          data-testid={`order-btn-${product.id}`}
        >
          <ShoppingBag className="w-4 h-4" />
          {product.available ? "Order this" : "Sold out"}
        </button>
      </div>
    </article>
  );
}

function OrderModal({ product, onClose }) {
  const [qty, setQty] = useState(1);
  const [form, setForm] = useState({
    customer_name: "",
    phone: "",
    address: "",
    notes: "",
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState("");

  async function submit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const { data } = await api.createOrder({
        ...form,
        items: [
          {
            product_id: product.id,
            product_name: product.name,
            quantity: qty,
            price: product.price,
          },
        ],
      });
      setSuccess(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not place order.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 bg-ink/50 backdrop-blur-sm flex items-end sm:items-center justify-center p-0 sm:p-6"
      onClick={onClose}
      data-testid="order-modal"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="bg-surface w-full sm:max-w-lg rounded-t-3xl sm:rounded-2xl overflow-hidden shadow-2xl fade-up max-h-[95vh] overflow-y-auto"
      >
        {success ? (
          <div className="p-10 text-center" data-testid="order-success">
            <div className="w-16 h-16 rounded-full bg-sage/20 flex items-center justify-center mx-auto mb-6">
              <Check className="w-8 h-8 text-sage" strokeWidth={2} />
            </div>
            <h3 className="serif text-3xl text-ink font-bold mb-3">
              Order received
            </h3>
            <p className="text-sub leading-relaxed mb-2">
              Thank you, {success.customer_name}. We'll call {success.phone} to
              confirm.
            </p>
            <p className="text-xs uppercase tracking-[0.2em] text-sub mb-8">
              Reference · {success.id.slice(0, 8)}
            </p>
            <button
              onClick={onClose}
              className="bg-primary text-white hover:bg-primaryHover rounded-full px-8 py-3 font-medium transition-colors"
              data-testid="order-success-close"
            >
              Back to shop
            </button>
          </div>
        ) : (
          <form onSubmit={submit} className="p-8">
            <div className="flex items-start justify-between mb-6">
              <div>
                <div className="text-xs uppercase tracking-[0.2em] text-sub">
                  Place an order
                </div>
                <h3 className="serif text-2xl text-ink font-bold mt-1">
                  {product.name}
                </h3>
              </div>
              <button
                type="button"
                onClick={onClose}
                className="p-2 rounded-full hover:bg-line transition-colors"
                data-testid="order-close-btn"
              >
                <X className="w-5 h-5 text-ink" />
              </button>
            </div>

            <div className="flex items-center justify-between bg-bg rounded-xl p-4 mb-6 border border-line">
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setQty(Math.max(1, qty - 1))}
                  className="w-9 h-9 rounded-full border border-line flex items-center justify-center hover:border-primary transition-colors"
                  data-testid="qty-minus"
                >
                  <Minus className="w-4 h-4" />
                </button>
                <span className="serif text-xl w-10 text-center" data-testid="qty-value">
                  {qty}
                </span>
                <button
                  type="button"
                  onClick={() => setQty(qty + 1)}
                  className="w-9 h-9 rounded-full border border-line flex items-center justify-center hover:border-primary transition-colors"
                  data-testid="qty-plus"
                >
                  <Plus className="w-4 h-4" />
                </button>
              </div>
              <div className="serif text-2xl text-ink font-bold" data-testid="order-total">
                ${(product.price * qty).toFixed(2)}
              </div>
            </div>

            <div className="space-y-4">
              <Field
                label="Your name"
                value={form.customer_name}
                onChange={(v) => setForm({ ...form, customer_name: v })}
                required
                testId="order-name"
              />
              <Field
                label="Phone"
                value={form.phone}
                onChange={(v) => setForm({ ...form, phone: v })}
                required
                testId="order-phone"
              />
              <Field
                label="Pickup / delivery address"
                value={form.address}
                onChange={(v) => setForm({ ...form, address: v })}
                required
                testId="order-address"
              />
              <Field
                label="Notes (optional)"
                value={form.notes}
                onChange={(v) => setForm({ ...form, notes: v })}
                testId="order-notes"
              />
            </div>

            {error && (
              <div className="mt-4 text-sm text-primary" data-testid="order-error">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="mt-6 w-full bg-primary text-white hover:bg-primaryHover rounded-full py-4 font-medium transition-colors disabled:opacity-60"
              data-testid="order-submit-btn"
            >
              {loading ? "Placing order…" : "Place order"}
            </button>
            <p className="mt-3 text-xs text-sub text-center">
              No payment now — we'll confirm on the phone.
            </p>
          </form>
        )}
      </div>
    </div>
  );
}

function Field({ label, value, onChange, required, testId }) {
  return (
    <label className="block">
      <span className="text-xs uppercase tracking-[0.2em] text-sub">{label}</span>
      <input
        type="text"
        value={value}
        required={required}
        onChange={(e) => onChange(e.target.value)}
        className="mt-2 w-full bg-bg border border-line rounded-xl px-4 py-3 text-ink focus:outline-none focus:border-primary transition-colors"
        data-testid={testId}
      />
    </label>
  );
}

function Catalogue({ onOrder }) {
  const [products, setProducts] = useState([]);
  const [category, setCategory] = useState("All");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api
      .listProducts(category)
      .then(({ data }) => setProducts(data))
      .finally(() => setLoading(false));
  }, [category]);

  return (
    <section id="catalog" className="py-24 lg:py-32 border-b border-line" data-testid="catalog-section">
      <div className="max-w-7xl mx-auto px-6 lg:px-10">
        <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-6 mb-12">
          <div>
            <div className="text-xs font-sans uppercase tracking-[0.3em] text-sub mb-4">
              The catalogue
            </div>
            <h2 className="serif text-4xl lg:text-5xl font-bold text-ink tracking-tight">
              Fresh out the oven
            </h2>
          </div>
          <div className="flex flex-wrap gap-2" data-testid="category-filters">
            {CATEGORIES.map((c) => (
              <button
                key={c}
                onClick={() => setCategory(c)}
                className={`px-5 py-2 rounded-full text-sm font-medium border transition-all ${
                  category === c
                    ? "bg-ink text-bg border-ink"
                    : "bg-transparent text-ink border-line hover:border-ink"
                }`}
                data-testid={`category-${c.toLowerCase()}`}
              >
                {c}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="py-20 text-center text-sub" data-testid="catalog-loading">Loading the day's bake…</div>
        ) : products.length === 0 ? (
          <div className="py-20 text-center text-sub" data-testid="catalog-empty">
            Nothing in this basket today — check back tomorrow.
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {products.map((p) => (
              <ProductCard key={p.id} product={p} onOrder={onOrder} />
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

function Story() {
  return (
    <section id="story" className="py-24 lg:py-32 border-b border-line" data-testid="story-section">
      <div className="max-w-7xl mx-auto px-6 lg:px-10 grid grid-cols-1 lg:grid-cols-12 gap-12">
        <div className="lg:col-span-4">
          <div className="text-xs font-sans uppercase tracking-[0.3em] text-sub mb-4">
            Our story
          </div>
          <h2 className="serif text-4xl lg:text-5xl font-bold text-ink tracking-tight">
            Flour, water, salt, time.
          </h2>
        </div>
        <div className="lg:col-span-7 lg:col-start-6 space-y-6 text-lg text-sub leading-relaxed">
          <p>
            Maison Levain began in the corner of a tiny rented kitchen on 14th
            Avenue, with one second-hand deck oven and a stubborn sourdough
            starter named Albert. Eleven years on, Albert is still with us —
            grumpier, yes, but still rising.
          </p>
          <p>
            We source heritage-grain flour from three regional mills, ferment
            our doughs slowly overnight, and shape every loaf by hand at dawn.
            The result is bread that keeps well, tastes alive, and makes a
            house smell like home.
          </p>
        </div>
      </div>
    </section>
  );
}

function Visit() {
  return (
    <section id="visit" className="py-24 lg:py-32" data-testid="visit-section">
      <div className="max-w-7xl mx-auto px-6 lg:px-10 grid grid-cols-1 md:grid-cols-3 gap-10">
        <InfoCard icon={<MapPin className="w-5 h-5" />} label="Find us" lines={["418 NE 14th Ave", "Portland, OR 97232"]} />
        <InfoCard icon={<Clock className="w-5 h-5" />} label="Open" lines={["Tue – Sat · 7am – 3pm", "Sunday · 8am – 1pm"]} />
        <InfoCard icon={<Instagram className="w-5 h-5" />} label="Follow" lines={["@maisonlevain", "hello@maisonlevain.co"]} />
      </div>
    </section>
  );
}

function InfoCard({ icon, label, lines }) {
  return (
    <div className="bg-surface rounded-2xl border border-line p-8" data-testid={`visit-card-${label.toLowerCase()}`}>
      <div className="flex items-center gap-3 text-sub mb-4">
        {icon}
        <span className="text-xs uppercase tracking-[0.2em]">{label}</span>
      </div>
      {lines.map((l) => (
        <div key={l} className="serif text-lg text-ink">
          {l}
        </div>
      ))}
    </div>
  );
}

function Footer() {
  return (
    <footer className="border-t border-line bg-bg" data-testid="site-footer">
      <div className="max-w-7xl mx-auto px-6 lg:px-10 py-10 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-sub">
        <div className="flex items-center gap-2">
          <Wheat className="w-4 h-4 text-primary" strokeWidth={1.5} />
          <span>© {new Date().getFullYear()} Maison Levain — Baked by hand.</span>
        </div>
        <div>Made with flour & patience.</div>
      </div>
    </footer>
  );
}

export default function Storefront() {
  const [orderingProduct, setOrderingProduct] = useState(null);

  return (
    <div className="min-h-screen bg-bg">
      <Header />
      <Hero />
      <Catalogue onOrder={setOrderingProduct} />
      <Story />
      <Visit />
      <Footer />
      {orderingProduct && (
        <OrderModal
          product={orderingProduct}
          onClose={() => setOrderingProduct(null)}
        />
      )}
    </div>
  );
}
