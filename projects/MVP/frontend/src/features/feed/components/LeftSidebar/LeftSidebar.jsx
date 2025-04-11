import styles from "./LeftSidebar.module.css";
import { useAuthentication } from "../../../authentication/contexts/AuthenticationContextProvider";

export function LeftSidebar() {
    const { user } = useAuthentication();
    return (
        <div className={styles.root}>
            <div className={styles.cover}>
                <img src="/cover.jpeg" alt="Cover"/>
            </div>
            <div className={styles.avatar}>
                <img src= "/avatar.svg" alt=""
                />
            </div>
            <div className={styles.name}>
                {user?.first_name + " " + user?.last_name}
            </div>
            <div className={styles.title}>
                {user?.position + " at " + user?.company}
            </div>
            <div className={styles.info}>
                <div className={styles.item}>
                    <div className={styles.label}>Profile views</div>
                    <div className={styles.value}>
                        1,234
                    </div>
                </div>
                <div className={styles.item}>
                    <div className={styles.label}>Connections</div>
                    <div className={styles.value}>
                        4,567
                    </div>
                </div>
            </div>
        </div>
    );
}; 