import { NavLink } from 'react-router-dom';

export default function PasswordResetInvalid() {
    return (
        <div className="container">
            <div className="recoveryPassword">
                <h1>Ссылка недействительна</h1>

                <p style={{ marginTop: 12 }}>
                    Ссылка для восстановления пароля недействительна или устарела.
                    Запросите восстановление ещё раз.
                </p>

                <div style={{ marginTop: 20 }}>
                    <NavLink to="/password/reset/">Запросить письмо заново</NavLink>
                </div>
            </div>
        </div>
    );
}