import styles from './Separator.module.css';

export function Separator({children}) {
    return (
        <div className={styles.root}>
            {children}
        </div>
    )
}