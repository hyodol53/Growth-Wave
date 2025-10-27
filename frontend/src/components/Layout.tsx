import React from 'react';
import { Link } from 'react-router-dom';
import { auth } from '../services/api';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const handleLogout = () => {
    auth.logout();
    window.location.reload();
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <header style={{ backgroundColor: '#333', color: 'white', padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>Growth-Wave</div>
        <nav>
          <Link to="/" style={{ color: 'white', textDecoration: 'none', marginRight: '1rem' }}>Home</Link>
          <Link to="/profile" style={{ color: 'white', textDecoration: 'none', marginRight: '1rem' }}>Profile</Link>
          <button onClick={handleLogout} style={{ background: 'none', border: '1px solid white', color: 'white', padding: '0.5rem 1rem', borderRadius: '4px', cursor: 'pointer' }}>Logout</button>
        </nav>
      </header>

      <div style={{ display: 'flex', flex: 1 }}>
        <aside style={{ width: '200px', backgroundColor: '#f4f4f4', padding: '1rem', borderRight: '1px solid #ddd' }}>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            <li style={{ marginBottom: '0.5rem' }}><Link to="/" style={{ textDecoration: 'none', color: '#333' }}>Dashboard</Link></li>
            <li style={{ marginBottom: '0.5rem' }}><Link to="/evaluations" style={{ textDecoration: 'none', color: '#333' }}>Evaluations</Link></li>
            <li style={{ marginBottom: '0.5rem' }}><Link to="/reports" style={{ textDecoration: 'none', color: '#333' }}>Reports</Link></li>
            <li style={{ marginBottom: '0.5rem' }}><Link to="/admin" style={{ textDecoration: 'none', color: '#333' }}>Admin</Link></li>
          </ul>
        </aside>

        <main style={{ flex: 1, padding: '1rem' }}>
          {children}
        </main>
      </div>

      <footer style={{ backgroundColor: '#333', color: 'white', textAlign: 'center', padding: '1rem', marginTop: 'auto' }}>
        &copy; 2025 Growth-Wave. All rights reserved.
      </footer>
    </div>
  );
};

export default Layout;
