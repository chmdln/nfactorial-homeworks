import styles from "./Messaging.module.css";
import { Outlet, useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { usePageTitle } from "../../../../hooks/usePageTitle";
import { Conversations } from "../../components/Conversations/Conversations";
import { useState, useEffect } from "react";
import { RightSidebar } from "../../../feed/components/RightSidebar/RightSidebar";


// main page for messaging 
export function Messaging() {
    usePageTitle("Messaging");
    const navigate = useNavigate(); 
    const location = useLocation();
    const [windowWidth, setWindowWidth] = useState(window.innerWidth);
    const onConversation = location.pathname.includes("conversations");

    // responsive sidebar, only show sidebar on conversations page
    useEffect(() => {
        const handleSize = () => setWindowWidth(window.innerWidth);
        window.addEventListener("resize", handleSize);
        return () => window.removeEventListener("resize", handleSize);
    }, []);

    return (
        <div className={styles.root}>
            <div className={styles.messaging}>
                <div className={styles.sidebar}
                    style={{
                        display: windowWidth >=1024 || !onConversation ? "block" : "none"
                    }}>
                    <div className={styles.header}>
                        <div>Messaging</div>
                        <button 
                            onClick={() => {
                                // new page to search for users to start a conversation, 46:04 in video
                                navigate("/messaging/conversations/new"); 
                            }}
                            className={styles.new}
                        >
                            +
                        </button>
                    </div>
                    {/* list of conversations to display */}
                    <Conversations />
                </div>

                {/* renders the conversation page, <Conversation /> */}
                <Outlet /> 
            </div>

            <div className={styles.adds}>
                <RightSidebar />
            </div>
        </div>
    ); 
}; 