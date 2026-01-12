import { NavLink } from 'react-router-dom';

export default function PasswordResetSuccess() {
    return (
        <div className="container">
            <div className="recoveryPassword">
                <h1>Пароль успешно изменён</h1>

                <p style={{ marginTop: 12 }}>
                    Теперь вы можете войти с новым паролем.
                </p>

                <div style={{ marginTop: 20 }}>
                    <NavLink to="/login/">Войти</NavLink>
                </div>
            </div>
        </div>
    );
}