import styles from "./Loader.module.css";

export function Loader() {
    return (
      <div className={styles.root}>
        <img className={styles.loaderImg} src="/logo.svg" alt="Loading..." />
        <div className={styles.container}>
            <div className={styles.content}></div>
        </div>
      </div>
    );
  }
