import { Outlet } from 'react-router-dom';
import styles from './AuthLayout.module.css';

export function AuthLayout() {
    return (
        <div className={styles.root}>
            <header className={styles.container}>
                <a href="/">
                    <span className={styles.logo}>TechFinder</span>
                </a>
            </header>
            <main className={styles.container}>
                <Outlet />
            </main>
            <footer>
                <ul className={styles.container}>
                    <li>
                        <span>TechFinder</span>
                        <span>&copy; 2025</span>
                    </li>
                    <li>
                        <a href="">Accessiblity</a>
                    </li>
                    <li>
                        <a href="">User Agreement</a>
                    </li>
                    <li>
                        <a href="">Privacy Policy</a>
                    </li>
                    <li>
                        <a href="">Cookie Policy</a>
                    </li>
                    <li>
                        <a href="">Copywright Policy</a>
                    </li>
                    <li>
                        <a href="">Brand Policy</a>
                    </li>
                    <li>
                        <a href="">Guest Controls</a>
                    </li>
                    <li>
                        <a href="">Community Guidelines</a>
                    </li>
                    <li>
                        <a href="">Language</a>
                    </li>
                </ul>
            </footer>
        </div>
    )
}