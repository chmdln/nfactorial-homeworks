import styles from "./ApplicationLayout.module.css";
import { Outlet } from "react-router-dom";
import { Header } from "../Header/Header";

export function ApplicationLayout() {
    return (
        <div className={styles.root}>
            <Header />
            <main className={styles.container}>
                <Outlet />
            </main>
        </div>
    )
}