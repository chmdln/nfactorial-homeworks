import styles from "./Profile.module.css";
import { useAuthentication } from "../../../features/authentication/contexts/AuthenticationContextProvider";
import { Button } from "../../Button/Button";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";



export function Profile({ showProfileMenu, setShowProfileMenu, setShowNavigationMenu }) {
    const { logout, user } = useAuthentication();
    // const ref = useRef(null);
    const navigate = useNavigate();

    return (
        <div className={styles.root}>
            <button
                className={styles.toggle}
                onClick={() => {
                    setShowProfileMenu((prev) => !prev);
                    if (window.innerWidth <= 1080) {
                        setShowNavigationMenu(false);
                    }
                }}
                >
                <img
                    className={styles.avatar}
                    src={
                    user?.profilePicture
                        ? `${import.meta.env.VITE_API_URL}/api/v1/storage/${user?.profilePicture}`
                        : "/avatar.svg"
                    }
                    alt=""
                />
                <div className={styles.name}>
                    <div>{user?.first_name + " " + user?.last_name?.charAt(0) + "."}</div>
                </div>
            </button>

            {showProfileMenu ? (
                <div className={styles.menu}>
                    <div className={styles.content}>
                        <img
                            className={`${styles.left} ${styles.avatar}`}
                            src={
                                user?.profilePicture
                                ? `${import.meta.env.VITE_API_URL}/api/v1/storage/${user?.profilePicture}`
                                : "/avatar.svg"
                            }
                            alt=""
                        />
                        <div className={styles.right}>
                            <div className={styles.name}>
                                {user?.first_name + " " + user?.last_name}
                            </div>
                            <div className={styles.title}>
                                {user?.position + " at " + user?.company}
                            </div>
                        </div>
                    </div>
                    <div className={styles.links}>
                        <Button
                        size="small"
                        className={styles.button}
                        outline
                        onClick={() => {
                            setShowProfileMenu(false);
                            navigate("/profile/" + user?.id);
                        }}
                        >
                            View Profile
                        </Button>
                        <Link
                        to="/auth/logout"
                        onClick={(e) => {
                            e.preventDefault();
                            logout();
                        }}
                        >
                            Sign Out
                        </Link>
                    </div>
                </div>
            ) : null}
        </div>
    )
}