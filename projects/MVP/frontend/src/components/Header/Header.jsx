import styles from "./Header.module.css";
import { NavLink } from "react-router-dom";
import { Input } from "../Input/Input";
import { useAuthentication } from "../../features/authentication/contexts/AuthenticationContextProvider";
import { useEffect, useState } from "react";
import { Profile } from "./components/Profile";

export function Header() {
    const { user } = useAuthentication(); 
    const [showProfileMenu, setShowProfileMenu] = useState(false); 
    const [showNavigationMenu, setShowNavigationMenu] = useState(window.innerWidth > 1080 ? true : false);


    useEffect(() => { 
        const handleResize = () => {
            setShowNavigationMenu(window.innerWidth > 1080 ? true : false);
        };
        window.addEventListener("resize", handleResize);
        return () => {
            // remove when comp unmounts
            window.removeEventListener("resize", handleResize);
        };
    }, []);


    return (
        <header className={styles.root}>
            <div className={styles.container}>
                <div className={styles.left}>
                    <NavLink to="/" className={styles.logo}>
                        TechFinder 
                    </NavLink>
                    <Input placeholder="Search" size={"medium"}/>
                </div>
                <div className={styles.right}>

                    <button
                        className={styles.toggle}
                        onClick={() => {
                            setShowNavigationMenu((prev) => !prev);
                            setShowProfileMenu(false);
                        }}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" fill="currentColor">
                        <path d="M0 96C0 78.3 14.3 64 32 64l384 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 128C14.3 128 0 113.7 0 96zM0 256c0-17.7 14.3-32 32-32l384 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 288c-17.7 0-32-14.3-32-32zM448 416c0 17.7-14.3 32-32 32L32 448c-17.7 0-32-14.3-32-32s14.3-32 32-32l384 0c17.7 0 32 14.3 32 32z" />
                        </svg>
                        <span>Menu</span>
                </button>

                {showNavigationMenu ? (
                    <ul className={styles.navigation}>
                        <li>
                            <NavLink
                                to="/"
                                className={({ isActive }) => (isActive ? styles.active : "")}
                                onClick={() => {
                                    setShowProfileMenu(false);
                                    if (window.innerWidth <= 1080) {
                                    setShowNavigationMenu(false);
                                    }
                                }}
                                >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    viewBox="0 0 24 24"
                                    fill="currentColor"
                                    width="24"
                                    height="24"
                                    focusable="false"
                                >
                                    <path d="M23 9v2h-2v7a3 3 0 01-3 3h-4v-6h-4v6H6a3 3 0 01-3-3v-7H1V9l11-7 5 3.18V2h3v5.09z"></path>
                                </svg>
                                <span>Home</span>
                            </NavLink>
                        </li>
                        <li className={styles.network}>
                            <NavLink
                            onClick={() => {
                                setShowProfileMenu(false);
                                if (window.innerWidth <= 1080) {
                                setShowNavigationMenu(false);
                                }
                            }}
                            to="/network"
                            className={({ isActive }) => (isActive ? styles.active : "")}
                            >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 24 24"
                                fill="currentColor"
                                focusable="false"
                            >
                                <path d="M12 16v6H3v-6a3 3 0 013-3h3a3 3 0 013 3zm5.5-3A3.5 3.5 0 1014 9.5a3.5 3.5 0 003.5 3.5zm1 2h-2a2.5 2.5 0 00-2.5 2.5V22h7v-4.5a2.5 2.5 0 00-2.5-2.5zM7.5 2A4.5 4.5 0 1012 6.5 4.49 4.49 0 007.5 2z"></path>
                            </svg>

                            <span>Network</span>
                            </NavLink>
                        </li>
                        <li className={styles.jobs}>
                            <NavLink
                            onClick={() => {
                                setShowProfileMenu(false);
                                if (window.innerWidth <= 1080) {
                                setShowNavigationMenu(false);
                                }
                            }}
                            to="/jobs"
                            className={({ isActive }) => (isActive ? styles.active : "")}
                            >
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" data-supported-dps="24x24" fill="currentColor" class="mercado-match" width="24" height="24" focusable="false">
                            <path d="M22.84 10.22L21 6h-3.95V5a3 3 0 00-3-3h-4a3 3 0 00-3 3v1H2l2.22 5.18A3 3 0 007 13h14a2 2 0 001.84-2.78zM15.05 6h-6V5a1 1 0 011-1h4a1 1 0 011 1zM7 14h15v3a3 3 0 01-3 3H5a3 3 0 01-3-3V8.54l1.3 3A4 4 0 007 14z"></path>
                            </svg>
                            {/* <div>
                                {invitations.length > 0 && !location.pathname.includes("network") ? (
                                <span className={styles.badge}>{invitations.length}</span>
                                ) : null}
                                <span>Network</span>
                            </div> */}
                            <span>Jobs</span>
                            </NavLink>
                        </li>
                        <li className={styles.messaging}>
                            <NavLink
                            onClick={() => {
                                setShowProfileMenu(false);
                                if (window.innerWidth <= 1080) {
                                setShowNavigationMenu(false);
                                }
                            }}
                            to="/messaging"
                            className={({ isActive }) => (isActive ? styles.active : "")}
                            >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 24 24"
                                fill="currentColor"
                                focusable="false"
                            >
                                <path d="M16 4H8a7 7 0 000 14h4v4l8.16-5.39A6.78 6.78 0 0023 11a7 7 0 00-7-7zm-8 8.25A1.25 1.25 0 119.25 11 1.25 1.25 0 018 12.25zm4 0A1.25 1.25 0 1113.25 11 1.25 1.25 0 0112 12.25zm4 0A1.25 1.25 0 1117.25 11 1.25 1.25 0 0116 12.25z"></path>
                            </svg>
                            {/* <div>
                                {nonReadMessagesCount > 0 && !location.pathname.includes("messaging") ? (
                                <span className={styles.badge}>{nonReadMessagesCount}</span>
                                ) : null}
                                <span>Messaging</span>
                            </div> */}
                            <span>Messaging</span>
                            </NavLink>
                        </li>
                        <li className={styles.notifications}>
                            <NavLink
                            onClick={() => {
                                setShowProfileMenu(false);
                                if (window.innerWidth <= 1080) {
                                setShowNavigationMenu(false);
                                }
                            }}
                            to="/notifications"
                            className={({ isActive }) => (isActive ? styles.active : "")}
                            >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 24 24"
                                fill="currentColor"
                                focusable="false"
                            >
                                <path d="M22 19h-8.28a2 2 0 11-3.44 0H2v-1a4.52 4.52 0 011.17-2.83l1-1.17h15.7l1 1.17A4.42 4.42 0 0122 18zM18.21 7.44A6.27 6.27 0 0012 2a6.27 6.27 0 00-6.21 5.44L5 13h14z"></path>
                            </svg>
                            {/* <div>
                                {nonReadNotificationCount > 0 ? (
                                <span className={styles.badge}>{nonReadNotificationCount}</span>
                                ) : null}
                                <span>Notications</span>
                            </div> */}
                            <span>Notifications</span>
                            </NavLink>
                        </li>
                    </ul>
                ) : null}

                {/* if we have user, render this profile component */}
                {user ? (
                    <Profile
                        setShowNavigationMenu={setShowNavigationMenu}
                        showProfileMenu={showProfileMenu}
                        setShowProfileMenu={setShowProfileMenu}
                    />
                ) : null}

                </div>
            </div>
        </header>
    )
}