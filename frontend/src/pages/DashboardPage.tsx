import { useEffect, useState, useCallback } from 'react';
import { Search, Plus, SlidersHorizontal, Car, AlertCircle, X } from 'lucide-react';
import { api, type Vehicle } from '@/lib/api';
import { useAuth } from '@/context/AuthContext';
import VehicleCard from '@/components/VehicleCard';
import EditVehicleModal from '@/components/EditVehicleModal';
import RestockModal from '@/components/RestockModal';

export default function DashboardPage() {
  const { user } = useAuth();
  const isAdmin = user?.is_admin ?? false;

  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [toast, setToast] = useState('');

  const [searchMake, setSearchMake] = useState('');
  const [searchModel, setSearchModel] = useState('');
  const [searchCategory, setSearchCategory] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [isSearching, setIsSearching] = useState(false);

  const [editingVehicle, setEditingVehicle] = useState<Vehicle | null>(null);
  const [restockingVehicle, setRestockingVehicle] = useState<Vehicle | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);

  const loadVehicles = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const data = await api.listVehicles();
      setVehicles(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load vehicles');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadVehicles();
  }, [loadVehicles]);

  function showToast(msg: string) {
    setToast(msg);
    setTimeout(() => setToast(''), 3000);
  }

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    setIsSearching(true);
    setError('');
    try {
      const data = await api.searchVehicles({
        make: searchMake || undefined,
        model: searchModel || undefined,
        category: searchCategory || undefined,
        min_price: minPrice ? parseFloat(minPrice) : undefined,
        max_price: maxPrice ? parseFloat(maxPrice) : undefined,
      });
      setVehicles(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed');
    } finally {
      setIsSearching(false);
    }
  }

  function clearFilters() {
    setSearchMake('');
    setSearchModel('');
    setSearchCategory('');
    setMinPrice('');
    setMaxPrice('');
    loadVehicles();
  }

  async function handlePurchase(vehicle: Vehicle) {
    try {
      const res = await api.purchaseVehicle(vehicle.id, 1);
      showToast(res.message);
      setVehicles((prev) => prev.map((v) => (v.id === vehicle.id ? { ...v, quantity: res.quantity } : v)));
    } catch (err) {
      showToast(err instanceof Error ? err.message : 'Purchase failed');
    }
  }

  async function handleDelete(vehicle: Vehicle) {
    if (!confirm(`Delete ${vehicle.make} ${vehicle.model}? This cannot be undone.`)) return;
    try {
      await api.deleteVehicle(vehicle.id);
      setVehicles((prev) => prev.filter((v) => v.id !== vehicle.id));
      showToast('Vehicle deleted');
    } catch (err) {
      showToast(err instanceof Error ? err.message : 'Delete failed');
    }
  }

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-slate-50">
      {toast && (
        <div className="fixed bottom-6 left-1/2 z-50 -translate-x-1/2 rounded-xl bg-slate-900 px-5 py-3 text-sm font-medium text-white shadow-lg">
          {toast}
        </div>
      )}

      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-slate-900">Inventory</h1>
            <p className="mt-1 text-slate-500">
              {loading ? 'Loading…' : `${vehicles.length} vehicle${vehicles.length !== 1 ? 's' : ''} available`}
            </p>
          </div>
          {isAdmin && (
            <button
              onClick={() => setShowAddForm(true)}
              className="flex items-center gap-2 rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800"
            >
              <Plus className="h-4 w-4" />
              Add vehicle
            </button>
          )}
        </div>

        {!loading && vehicles.length > 0 && (
          <div className="mb-8 overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 to-slate-700 p-8 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-300">Welcome back, {user?.username}</p>
                <h2 className="mt-1 text-2xl font-bold">Find Your Perfect Ride</h2>
                <p className="mt-2 text-slate-300">Browse our collection of {vehicles.length} vehicles</p>
              </div>
              <Car className="h-16 w-16 text-slate-500" />
            </div>
          </div>
        )}

        <form onSubmit={handleSearch} className="mb-6 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                value={searchMake}
                onChange={(e) => setSearchMake(e.target.value)}
                placeholder="Search by make…"
                className="w-full rounded-lg border border-slate-300 py-2.5 pl-10 pr-3 text-sm text-slate-900 outline-none transition focus:border-slate-900 focus:ring-2 focus:ring-slate-900/10"
              />
            </div>
            <input
              type="text"
              value={searchModel}
              onChange={(e) => setSearchModel(e.target.value)}
              placeholder="Model…"
              className="rounded-lg border border-slate-300 px-3 py-2.5 text-sm text-slate-900 outline-none transition focus:border-slate-900 focus:ring-2 focus:ring-slate-900/10 sm:w-40"
            />
            <button
              type="button"
              onClick={() => setShowFilters((s) => !s)}
              className="flex items-center justify-center gap-1.5 rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
            >
              <SlidersHorizontal className="h-4 w-4" />
              Filters
            </button>
            <button
              type="submit"
              disabled={isSearching}
              className="rounded-lg bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:opacity-60"
            >
              {isSearching ? 'Searching…' : 'Search'}
            </button>
          </div>

          {showFilters && (
            <div className="mt-4 flex flex-wrap items-end gap-3 border-t border-slate-100 pt-4">
              <div>
                <label className="mb-1 block text-xs font-medium text-slate-500">Category</label>
                <input
                  type="text"
                  value={searchCategory}
                  onChange={(e) => setSearchCategory(e.target.value)}
                  placeholder="Sedan, SUV…"
                  className="rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-900/10"
                />
              </div>
              <div>
                <label className="mb-1 block text-xs font-medium text-slate-500">Min price</label>
                <input
                  type="number"
                  value={minPrice}
                  onChange={(e) => setMinPrice(e.target.value)}
                  placeholder="0"
                  className="w-28 rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-900/10"
                />
              </div>
              <div>
                <label className="mb-1 block text-xs font-medium text-slate-500">Max price</label>
                <input
                  type="number"
                  value={maxPrice}
                  onChange={(e) => setMaxPrice(e.target.value)}
                  placeholder="100000"
                  className="w-28 rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-900/10"
                />
              </div>
              <button type="button" onClick={clearFilters} className="text-sm font-medium text-slate-500 transition hover:text-slate-900">
                Clear all
              </button>
            </div>
          )}
        </form>

        {error && (
          <div className="mb-6 flex items-center gap-2 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700">
            <AlertCircle className="h-5 w-5 flex-shrink-0" />
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex h-64 items-center justify-center">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-slate-900" />
          </div>
        ) : vehicles.length === 0 ? (
          <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-slate-300 py-20 text-center">
            <Car className="h-12 w-12 text-slate-300" />
            <p className="mt-3 text-lg font-medium text-slate-500">No vehicles found</p>
            <p className="text-sm text-slate-400">Try adjusting your search or filters</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {vehicles.map((v) => (
              <VehicleCard
                key={v.id}
                vehicle={v}
                isAdmin={isAdmin}
                onPurchase={handlePurchase}
                onEdit={setEditingVehicle}
                onDelete={handleDelete}
                onRestock={setRestockingVehicle}
              />
            ))}
          </div>
        )}
      </div>

      {showAddForm && <AddVehicleModal onClose={() => setShowAddForm(false)} onAdded={loadVehicles} />}
      <EditVehicleModal vehicle={editingVehicle} onClose={() => setEditingVehicle(null)} onSaved={loadVehicles} />
      <RestockModal vehicle={restockingVehicle} onClose={() => setRestockingVehicle(null)} onDone={loadVehicles} />
    </div>
  );
}

function AddVehicleModal({ onClose, onAdded }: { onClose: () => void; onAdded: () => void }) {
  const [form, setForm] = useState({ make: '', model: '', category: '', price: '', quantity: '', image_url: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await api.addVehicle({
        make: form.make,
        model: form.model,
        category: form.category,
        price: parseFloat(form.price),
        quantity: parseInt(form.quantity, 10),
        image_url: form.image_url || undefined,
      });
      onAdded();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add vehicle');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4 backdrop-blur-sm" onClick={onClose}>
      <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl" onClick={(e) => e.stopPropagation()}>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-bold text-slate-900">Add new vehicle</h2>
          <button onClick={onClose} className="rounded-lg p-1.5 text-slate-400 transition hover:bg-slate-100 hover:text-slate-700">
            <X className="h-5 w-5" />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <FormField label="Make" value={form.make} onChange={(v) => setForm({ ...form, make: v })} />
            <FormField label="Model" value={form.model} onChange={(v) => setForm({ ...form, model: v })} />
            <FormField label="Category" value={form.category} onChange={(v) => setForm({ ...form, category: v })} />
            <FormField label="Price ($)" type="number" value={form.price} onChange={(v) => setForm({ ...form, price: v })} />
            <FormField label="Quantity" type="number" value={form.quantity} onChange={(v) => setForm({ ...form, quantity: v })} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Image URL (optional)</label>
            <input
              type="text"
              value={form.image_url}
              onChange={(e) => setForm({ ...form, image_url: e.target.value })}
              placeholder="https://images.unsplash.com/..."
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 outline-none transition focus:border-slate-900 focus:ring-2 focus:ring-slate-900/10"
            />
          </div>
          {error && <div className="rounded-lg bg-red-50 px-3.5 py-2.5 text-sm text-red-700">{error}</div>}
          <div className="flex gap-3 pt-2">
            <button type="button" onClick={onClose} className="flex-1 rounded-lg border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-700 transition hover:bg-slate-50">
              Cancel
            </button>
            <button type="submit" disabled={loading} className="flex-1 rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:opacity-60">
              {loading ? 'Adding…' : 'Add vehicle'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function FormField({ label, value, onChange, type = 'text' }: { label: string; value: string; onChange: (v: string) => void; type?: string }) {
  return (
    <div>
      <label className="mb-1 block text-sm font-medium text-slate-700">{label}</label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required
        step={type === 'number' ? 'any' : undefined}
        min={type === 'number' ? '0' : undefined}
        className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 outline-none transition focus:border-slate-900 focus:ring-2 focus:ring-slate-900/10"
      />
    </div>
  );
}