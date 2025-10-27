import React, { useState } from 'react';
import { auth } from '../services/api';

interface LoginProps {
  onLoginSuccess: () => void;
}

const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await auth.login(username, password);
      onLoginSuccess();
    } catch (err) {
      setError('Invalid credentials');
      console.error(err);
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#f0f2f5' }}>
      <form onSubmit={handleSubmit} style={{
        padding: '40px',
        borderRadius: '8px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        backgroundColor: '#fff',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
        width: '300px'
      }}>
        <h2 style={{ textAlign: 'center', color: '#333' }}>Login</h2>
        {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{
            padding: '10px',
            borderRadius: '4px',
            border: '1px solid #ddd',
            fontSize: '16px'
          }}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{
            padding: '10px',
            borderRadius: '4px',
            border: '1px solid #ddd',
            fontSize: '16px'
          }}
          required
        />
        <button
          type="submit"
          style={{
            padding: '10px 15px',
            borderRadius: '4px',
            border: 'none',
            backgroundColor: '#007bff',
            color: 'white',
            fontSize: '16px',
            cursor: 'pointer'
          }}
        >
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
