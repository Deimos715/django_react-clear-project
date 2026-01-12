import { NavLink } from 'react-router-dom';
import AuthService from '../services/auth';

export default function PasswordChangeSuccess() {
    const isAuth = AuthService.isAuthenticated();

    return (
        <div className="container">
            <div className="recoveryPassword">
                <h1>Пароль успешно изменён</h1>

                <p style={{ marginTop: 12 }}>
                    Ваш пароль обновлён. Теперь вы можете продолжить работу в личном кабинете.
                </p>

                <div style={{ marginTop: 20 }}>
                    {isAuth ? (
                        <NavLink to="/account/">
                            Перейти в аккаунт
                        </NavLink>
                    ) : (
                        <NavLink to="/login/">
                            Войти
                        </NavLink>
                    )}
                </div>
            </div>
        </div>
    );
}
