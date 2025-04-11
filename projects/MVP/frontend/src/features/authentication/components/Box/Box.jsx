
import styles from './Box.module.css';

export function Box({ children }) {
    return (
        <div className={styles.root}>
            {children}
        </div>
    )
}