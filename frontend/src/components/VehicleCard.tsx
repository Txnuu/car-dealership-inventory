import { ShoppingBag, Pencil, Trash2, PackagePlus } from 'lucide-react';
import { useState } from 'react';
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

const carImages: Record<string, string> = {
  'Toyota Camry': 'https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=400&h=250&fit=crop',
  'Toyota RAV4': 'https://images.unsplash.com/photo-1568844293986-ca4c5c3b1c1c?w=400&h=250&fit=crop',
  'Honda Civic': 'https://images.unsplash.com/photo-1606611013016-969c19ba27b8?w=400&h=250&fit=crop',
  'Ford Mustang': 'https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?w=400&h=250&fit=crop',
  'BMW X5': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400&h=250&fit=crop',
};

const defaultImages: Record<string, string> = {
  Sedan: 'https://images.unsplash.com/photo-1550355291-bbee04a92027?w=400&h=250&fit=crop',
  SUV: 'https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=400&h=250&fit=crop',
  Coupe: 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&h=250&fit=crop',
  Truck: 'https://images.unsplash.com/photo-1583267746897-2cf415887172?w=400&h=250&fit=crop',
  Hatchback: 'https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=400&h=250&fit=crop',
  Electric: 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=400&h=250&fit=crop',
};

export default function VehicleCard({ vehicle, isAdmin, onPurchase, onEdit, onDelete, onRestock }: VehicleCardProps) {
  const [imgError, setImgError] = useState(false);
  const outOfStock = vehicle.quantity <= 0;
  const badgeClass = categoryColors[vehicle.category] || 'bg-slate-100 text-slate-700';
  
  const carKey = `${vehicle.make} ${vehicle.model}`;
  const imageUrl = vehicle.image_url || carImages[carKey] || defaultImages[vehicle.category] || 'https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=400&h=250&fit=crop';

  return (
    <div className="group flex flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white transition hover:shadow-lg hover:shadow-slate-200/60 hover:-translate-y-0.5">
      <div className="relative h-48 overflow-hidden">
        {!imgError ? (
          <img
            src={imageUrl}
            alt={`${vehicle.make} ${vehicle.model}`}
            className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
            onError={() => setImgError(true)}
          />
        ) : (
          <div className="flex h-full items-center justify-center bg-gradient-to-br from-slate-100 to-slate-200">
            <span className="text-5xl font-black text-slate-300 tracking-tight">
              {vehicle.make.charAt(0)}{vehicle.model.charAt(0)}
            </span>
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
        <span className={`absolute left-3 top-3 rounded-full px-2.5 py-1 text-xs font-semibold ${badgeClass}`}>
          {vehicle.category}
        </span>
        {outOfStock && (
          <span className="absolute right-3 top-3 rounded-full bg-red-500 px-2.5 py-1 text-xs font-semibold text-white shadow-sm">
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