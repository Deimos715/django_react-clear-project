import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthService from '../services/auth';

export default function PasswordResetRequest() {
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const onSubmit = (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        AuthService.passwordResetStart(email)
            .then(() => {
                navigate('/password/reset/sent/');
            })
            .catch((err) => {
                const msg =
                    err?.response?.data?.detail ||
                    err?.response?.data?.email?.[0] ||
                    'Не удалось отправить письмо';
                setError(msg);
            })
            .finally(() => {
                setLoading(false);
            });
    };

    return (
        <div className="container">
            <div className="recoveryPassword">
                <h1>Восстановление пароля</h1>

                <form className="w-50 mx-auto" onSubmit={onSubmit} noValidate>
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

                    {error && <p style={{ color: 'crimson' }}>{error}</p>}

                    <button type="submit" disabled={loading}>
                        {loading ? 'Отправляем...' : 'Отправить письмо'}
                    </button>
                </form>
            </div>
        </div>
    );
}