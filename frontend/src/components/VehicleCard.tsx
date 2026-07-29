import { ShoppingBag, Pencil, Trash2, PackagePlus } from 'lucide-react';
import type { Vehicle } from '@/lib/api';

interface VehicleCardProps {
  vehicle: Vehicle;
  isAdmin: boolean;
  onPurchase: (vehicle: Vehicle) => void;
  onEdit: (vehicle: Vehicle) => void;
  onDelete: (vehicle: Vehicle) => void;
  onRestock: (vehicle: Vehicle) => void;
}

const categoryColors: Record<string, string> = {
  Sedan: 'bg-blue-50 text-blue-700',
  SUV: 'bg-emerald-50 text-emerald-700',
  Coupe: 'bg-amber-50 text-amber-700',
  Truck: 'bg-orange-50 text-orange-700',
  Hatchback: 'bg-purple-50 text-purple-700',
  Electric: 'bg-teal-50 text-teal-700',
};

export default function VehicleCard({ vehicle, isAdmin, onPurchase, onEdit, onDelete, onRestock }: VehicleCardProps) {
  const outOfStock = vehicle.quantity <= 0;
  const badgeClass = categoryColors[vehicle.category] || 'bg-slate-100 text-slate-700';

  return (
    <div className="group flex flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white transition hover:shadow-lg hover:shadow-slate-200/60">
      <div className="relative h-44 overflow-hidden bg-gradient-to-br from-slate-100 to-slate-200">
        <div className="flex h-full items-center justify-center">
          <span className="text-5xl font-black text-slate-300 tracking-tight">
            {vehicle.make.charAt(0)}
            {vehicle.model.charAt(0)}
          </span>
        </div>
        <span className={`absolute left-3 top-3 rounded-full px-2.5 py-1 text-xs font-semibold ${badgeClass}`}>
          {vehicle.category}
        </span>
        {outOfStock && (
          <span className="absolute right-3 top-3 rounded-full bg-red-500 px-2.5 py-1 text-xs font-semibold text-white">
            Out of stock
          </span>
        )}
      </div>

      <div className="flex flex-1 flex-col p-5">
        <h3 className="text-lg font-bold text-slate-900">
          {vehicle.make} {vehicle.model}
        </h3>
        <p className="mt-1 text-2xl font-bold text-slate-900">
          ${vehicle.price.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
        </p>

        <div className="mt-3 flex items-center gap-2 text-sm">
          <span className={`flex items-center gap-1.5 rounded-lg px-2.5 py-1 font-medium ${outOfStock ? 'bg-red-50 text-red-600' : 'bg-emerald-50 text-emerald-700'}`}>
            <span className={`h-2 w-2 rounded-full ${outOfStock ? 'bg-red-500' : 'bg-emerald-500'}`} />
            {outOfStock ? '0 in stock' : `${vehicle.quantity} in stock`}
          </span>
        </div>

        <div className="mt-5 flex flex-wrap gap-2">
          <button
            onClick={() => onPurchase(vehicle)}
            disabled={outOfStock}
            className="flex flex-1 items-center justify-center gap-1.5 rounded-lg bg-slate-900 px-3 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"
          >
            <ShoppingBag className="h-4 w-4" />
            Purchase
          </button>

          {isAdmin && (
            <>
              <button
                onClick={() => onRestock(vehicle)}
                title="Restock"
                className="flex items-center justify-center rounded-lg border border-slate-200 px-3 py-2.5 text-sm font-medium text-slate-600 transition hover:bg-slate-50 hover:text-slate-900"
              >
                <PackagePlus className="h-4 w-4" />
              </button>
              <button
                onClick={() => onEdit(vehicle)}
                title="Edit"
                className="flex items-center justify-center rounded-lg border border-slate-200 px-3 py-2.5 text-sm font-medium text-slate-600 transition hover:bg-slate-50 hover:text-slate-900"
              >
                <Pencil className="h-4 w-4" />
              </button>
              <button
                onClick={() => onDelete(vehicle)}
                title="Delete"
                className="flex items-center justify-center rounded-lg border border-red-200 px-3 py-2.5 text-sm font-medium text-red-600 transition hover:bg-red-50"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}