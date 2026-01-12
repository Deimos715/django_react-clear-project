import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import AuthService from '../services/auth';

export default function PasswordResetConfirm() {
    const navigate = useNavigate();
    const { uidb64, token } = useParams();

    const [p1, setP1] = useState('');
    const [p2, setP2] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const onSubmit = (e) => {
        e.preventDefault();
        setError('');

        if (!p1 || !p2) {
            setError('Заполните оба поля пароля');
            return;
        }

        setLoading(true);

        AuthService.passwordResetConfirm(uidb64, token, p1, p2)
            .then(() => {
                navigate('/password/reset/success/');
            })
            .catch((err) => {
                const data = err?.response?.data;

                // DRF ошибки: {field: [msg]} или detail/token
                if (data && typeof data === 'object') {
                    const msg =
                        data?.detail ||
                        data?.token ||
                        data?.new_password1?.[0] ||
                        data?.new_password2?.[0] ||
                        'Не удалось изменить пароль';
                    setError(msg);
                } else {
                    setError('Не удалось изменить пароль');
                }
            })
            .finally(() => {
                setLoading(false);
            });
    };

    return (
        <div className="container">
            <div className="recoveryPassword">
                <h1>Установите новый пароль</h1>

                {error && <p style={{ color: 'crimson', marginTop: 12 }}>{error}</p>}

                <form className="w-50 mx-auto" onSubmit={onSubmit} noValidate>
                    <div className="requiredFieldAndPassword" style={{ width: '100%' }}>
                        <input
                            type="password"
                            placeholder="Новый пароль"
                            value={p1}
                            onChange={(e) => setP1(e.target.value)}
                        />
                    </div>

                    <div className="requiredFieldAndPassword" style={{ width: '100%' }}>
                        <input
                            type="password"
                            placeholder="Повторите новый пароль"
                            value={p2}
                            onChange={(e) => setP2(e.target.value)}
                        />
                    </div>

                    <button type="submit" disabled={loading} style={{ marginTop: 20 }}>
                        {loading ? 'Сохраняем...' : 'Сменить пароль'}
                    </button>
                </form>
            </div>
        </div>
    );
}