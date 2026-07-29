import { Link, useNavigate } from 'react-router-dom';
import { Car, LogOut, User as UserIcon, ShieldCheck } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate('/login');
  }

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/80 backdrop-blur-lg">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-2 text-slate-900">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-900 text-white">
            <Car className="h-5 w-5" />
          </div>
          <span className="text-lg font-bold tracking-tight">AutoLot</span>
        </Link>

        <div className="flex items-center gap-4">
          {user ? (
            <>
              <div className="hidden items-center gap-2 text-sm text-slate-600 sm:flex">
                {user.is_admin ? (
                  <ShieldCheck className="h-4 w-4 text-emerald-600" />
                ) : (
                  <UserIcon className="h-4 w-4" />
                )}
                <span className="font-medium text-slate-800">{user.username}</span>
                {user.is_admin && (
                  <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-xs font-medium text-emerald-700">
                    Admin
                  </span>
                )}
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-100 hover:text-slate-900"
              >
                <LogOut className="h-4 w-4" />
                <span className="hidden sm:inline">Sign out</span>
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="rounded-lg px-3 py-2 text-sm font-medium text-slate-600 transition hover:text-slate-900"
              >
                Sign in
              </Link>
              <Link
                to="/register"
                className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800"
              >
                Get started
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}