import { useEffect, useState } from 'react';
import StartDataService from '../services/home';


const Home = () => {
    const [message, setMessage] = useState('');

    useEffect(() => {
        StartDataService.getStartMessage()
        .then((res) => {
            setMessage(res.data.message);
        })
        .catch((err) => {
            console.error(err);
            setMessage('Ошибка при запросе к API');
        });
    }, []);

    return (
        <>
        <h1>Home</h1>
        <p>{message}</p>
        </>
    );
    };

    export default Home;
