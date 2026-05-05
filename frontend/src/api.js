import axios from "axios";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const client = axios.create({
  baseURL: API,
  withCredentials: true,
});

client.interceptors.request.use((config) => {
  const token = localStorage.getItem("bakery_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const api = {
  login: (email, password) => client.post("/auth/login", { email, password }),
  logout: () => client.post("/auth/logout"),
  me: () => client.get("/auth/me"),

  listProducts: (category) =>
    client.get("/products", { params: category ? { category } : {} }),
  getProduct: (id) => client.get(`/products/${id}`),
  createProduct: (data) => client.post("/products", data),
  updateProduct: (id, data) => client.put(`/products/${id}`, data),
  deleteProduct: (id) => client.delete(`/products/${id}`),

  createOrder: (data) => client.post("/orders", data),
  listOrders: () => client.get("/orders"),
  updateOrderStatus: (id, status) =>
    client.patch(`/orders/${id}/status`, { status }),
};

export default client;
