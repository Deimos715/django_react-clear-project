import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthService from '../services/auth';

const Login = () => {
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const onLogin = (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        AuthService.login(email, password)
            .then(() => {
                navigate('/account/');
            })
            .catch((err) => {
                const msg =
                    err?.response?.data?.detail ||
                    err?.response?.data?.non_field_errors?.[0] ||
                    'Ошибка входа';
                setError(msg);
            })
            .finally(() => {
                setLoading(false);
            });
    };

    return (
        <>
            <h1>Вход</h1>

            <form onSubmit={onLogin} style={{ maxWidth: 420 }}>
                <div style={{ marginBottom: 12 }}>
                    <label>Email</label>
                    <input
                        style={{ width: '100%', padding: 10 }}
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>

                <div style={{ marginBottom: 12 }}>
                    <label>Пароль</label>
                    <input
                        style={{ width: '100%', padding: 10 }}
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>

                {error && <p style={{ color: 'crimson' }}>{error}</p>}

                <button type="submit" disabled={loading}>
                    {loading ? 'Входим...' : 'Войти'}
                </button>
            </form>
        </>
    );
};

export default Login;
