const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function getToken(): string | null {
  return localStorage.getItem('access_token');
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (res.status === 204) return undefined as T;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.detail || `Request failed with status ${res.status}`);
  }
  return data as T;
}

export interface Vehicle {
  id: number;
  make: string;
  model: string;
  category: string;
  price: number;
  quantity: number;
  image_url?: string;
}

export interface AuthUser {
  id: number;
  username: string;
  email: string;
  is_admin: boolean;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  is_admin: boolean;
}

export const api = {
  register(username: string, email: string, password: string, is_admin = false) {
    return request<AuthUser>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password, is_admin }),
    });
  },
  login(username: string, password: string) {
    return request<LoginResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  },
  me() {
    return request<AuthUser>('/api/auth/me');
  },
  listVehicles() {
    return request<Vehicle[]>('/api/vehicles');
  },
  addVehicle(data: Omit<Vehicle, 'id'>) {
    return request<Vehicle>('/api/vehicles', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
  updateVehicle(id: number, data: Partial<Omit<Vehicle, 'id'>>) {
    return request<Vehicle>(`/api/vehicles/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },
  deleteVehicle(id: number) {
    return request<void>(`/api/vehicles/${id}`, { method: 'DELETE' });
  },
  searchVehicles(params: Record<string, string | number | undefined>) {
    const qs = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== '') qs.append(k, String(v));
    });
    return request<Vehicle[]>(`/api/vehicles/search?${qs.toString()}`);
  },
  purchaseVehicle(id: number, quantity = 1) {
    return request<{ id: number; quantity: number; message: string }>(
      `/api/vehicles/${id}/purchase`,
      { method: 'POST', body: JSON.stringify({ quantity }) },
    );
  },
  restockVehicle(id: number, quantity: number) {
    return request<{ id: number; quantity: number; message: string }>(
      `/api/vehicles/${id}/restock`,
      { method: 'POST', body: JSON.stringify({ quantity }) },
    );
  },
};