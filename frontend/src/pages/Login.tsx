import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { auth } from '../services/api';

const Login: React.FC = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await auth.login(username, password);
      navigate('/');
      window.location.reload();
    } catch {
      setError('로그인에 실패했습니다. 사용자 이름과 비밀번호를 확인하세요.');
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', width: '300px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
        <h2>로그인</h2>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <input
          type="text"
          placeholder="사용자 이름"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{ marginBottom: '10px', padding: '8px' }}
        />
        <input
          type="password"
          placeholder="비밀번호"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ marginBottom: '10px', padding: '8px' }}
        />
        <button type="submit" style={{ padding: '10px' }}>로그인</button>
      </form>
    </div>
  );
};

export default Login;