import { NavLink } from 'react-router-dom';

const Header = () => {
    return (
        <header className='header'>
            <p>header</p>
            <nav>
                {/* Добавляем ссылки для навигации ||
                to - Указываем то, что вернёт встроенная функция, адрес по которому юзер якобы переходит, 
                 для нас и движка это будет ответ для функции, фактически страницы не обновляются */}
                {/* <Link to='/home/'>Главная</Link> 
                <Link to='/account/'>Аккаунт</Link>
                <Link to='/help/'>Поддержка</Link> */}
                
                {/* Добавляем ссылки для навигации через NavLink ||
                to - тоже самое, className - Сделан тернарным оператором,
                он проверяет ссылку в URL Если она совпадает присылает true,
                и тернарник присваивает ссылке класс active для остальных inactive */}
                <NavLink to='/home/' className={({ isActive }) => (isActive ? 'active' : 'inactive')}>Главная</NavLink> 
                <NavLink to='/account/' className={({ isActive }) => (isActive ? 'active' : 'inactive')}>Аккаунт</NavLink>
                <NavLink to='/help/' className={({ isActive }) => (isActive ? 'active' : 'inactive')}>Поддержка</NavLink>
            </nav>
        </header>
    );
};

export default Header;
