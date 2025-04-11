import styles from "./RightSidebar.module.css";
import { Button } from "../../../../components/Button/Button";

export function RightSidebar() {
    return (
        <div className={styles.root}>
            <h3>Add to your connections</h3>
            <div className={styles.items}>
                <div className={styles.item}>
                    <img src="/avatar.svg" alt="" className={styles.avatar}/>
                    <div className={styles.content}>
                      <div className={styles.name}>
                        Jane Doe
                      </div>
                      <div className={styles.title}>
                        Software Engineer at KeyCorp  
                      </div>
                      <Button
                            size="medium"
                            outline
                            className={styles.button}
                            >
                            + Connect
                      </Button>
                    </div>
                </div>
            </div>
        </div>
    )
}