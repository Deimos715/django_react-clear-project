import { NavLink, useNavigate } from 'react-router-dom';
import AuthService from '../services/auth';

const Header = () => {
    const navigate = useNavigate();

    const isAuth = AuthService.isAuthenticated();

    const onLogout = () => {
        AuthService.logout()
            .finally(() => {
                navigate('/login/');
            });
    };

    return (
        <header className='header'>
            <p>header</p>

            <nav>
                <NavLink to='/home/' className={({ isActive }) => (isActive ? 'active' : 'inactive')}>
                    Главная
                </NavLink>

                {/* Аккаунт показываем только авторизованным */}
                {isAuth && (
                    <>
                        <NavLink
                            to='/account/'
                            className={({ isActive }) => (isActive ? 'active' : 'inactive')}
                        >
                            Аккаунт
                        </NavLink>

                        <NavLink
                            to='/password/change/'
                            className={({ isActive }) => (isActive ? 'active' : 'inactive')}
                            style={{ marginLeft: 12 }}
                        >
                            Сменить пароль
                        </NavLink>
                    </>
                )}

                <NavLink to='/help/' className={({ isActive }) => (isActive ? 'active' : 'inactive')}>
                    Поддержка
                </NavLink>

                {/* Справа: Вход / Регистрация / Выход */}
                {!isAuth ? (
                    <>
                        <NavLink
                            to='/login/'
                            className={({ isActive }) => (isActive ? 'active' : 'inactive')}
                        >
                            Вход
                        </NavLink>

                        <NavLink
                            to='/register/'
                            className={({ isActive }) => (isActive ? 'active' : 'inactive')}
                            style={{ marginLeft: 12 }}
                        >
                            Регистрация
                        </NavLink>
                    </>
                ) : (
                    <button type="button" onClick={onLogout} style={{ marginLeft: 12 }}>
                        Выход
                    </button>
                )}
            </nav>
        </header>
    );
};

export default Header;
