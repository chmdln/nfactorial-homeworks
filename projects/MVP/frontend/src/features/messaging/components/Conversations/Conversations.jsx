import { useEffect, useState } from "react";
import styles from "./Conversations.module.css";
// import { request } from "../../../../utils/axios";
import { Conversation } from "../Conversation/Conversation";
import { request } from "../../../../utils/api";
import { useAuthentication } from "../../../authentication/contexts/AuthenticationContextProvider";
import { useWebSocket } from "../../../ws/WebSocketContextProvider";


// list of existing conversation displayed on main messaging page 
export function Conversations(props) {
    const [conversations, setConversations] = useState([]);
    const { user } = useAuthentication();
    const websocketClient = useWebSocket();
  
    useEffect(() => {
      const subscription = websocketClient?.subscribe(
        `/topic/users/${user?.id}/conversations`,
        (message) => {
          const conversation = JSON.parse(message.body);
          setConversations((prevConversations) => {
            const index = prevConversations.findIndex((c) => c.id === conversation.id);
            if (index === -1) {
              return [conversation, ...prevConversations];
            }
            return prevConversations.map((c) => (c.id === conversation.id ? conversation : c));
          });
        }
      );
      return () => subscription?.unsubscribe();
    }, [user?.id, websocketClient]);
  
    return (
      <div className={styles.root} {...props}>
        {conversations.map((conversation) => {
          return <Conversation key={conversation.id} conversation={conversation} />;
        })}
        {conversations.length === 0 && (
          <div
            className={styles.welcome}
            style={{
              padding: "1rem",
            }}
          >
            No conversations to display.
          </div>
        )}
      </div>
    );
  }
