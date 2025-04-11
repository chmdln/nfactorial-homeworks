import styles from "./Conversation.module.css";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthentication } from "../../../authentication/contexts/AuthenticationContextProvider";
import { useParams } from "react-router-dom";
import { useWebSocket } from "../../../ws/WebSocketContextProvider";


export function Conversation(props) {
    const [conversation, setConversation] = useState(props.conversation);
    const {user} = useAuthentication();
    const ws = useWebSocket();
    const {id} = useParams(); 
    const navigate = useNavigate();
    const conversationUserToDisplay = conversation.recipient.id === user.id ? conversation.author : conversation.recipient;
    
    const unreadMessagesCount = conversation.messages.filter(
        (message) => !message.isRead && message.receiver.id === user?.id
    ).length;


    useEffect(() => {
        const subscription = ws?.subscribe(
          `/topic/conversations/${conversation.id}/messages`,
          (data) => {
            const message = JSON.parse(data.body);
            setConversation((prevConversation) => {
              const index = prevConversation.messages.findIndex((m) => m.id === message.id);
              if (index == -1) {
                return {
                  ...prevConversation,
                  messages: [...prevConversation.messages, message],
                };
              }
    
              return {
                ...prevConversation,
                messages: prevConversation.messages.map((m) => (m.id === message.id ? message : m)),
              };
            });
            return () => subscription?.unsubscribe();
          }
        );
    }, [conversation?.id, ws]);

    return (
        <button
          key={conversation.id}
          // change the background color of the selected conversation
          className={`${styles.root} ${id && Number(id) === conversation.id ? styles.selected : ""}`}
          onClick={() => navigate(`/messaging/conversations/${conversation.id}`)}
        >
          <img
            className={styles.avatar}
            src={conversationUserToDisplay.profilePicture || "/avatar.svg"}
            alt=""
          />
    
          {unreadMessagesCount > 0 && <div className={styles.unread}>{unreadMessagesCount}</div>}
    
          <div>
            <div className={styles.name}>
              {conversationUserToDisplay.firstName} {conversationUserToDisplay.lastName}
            </div>
            {/* display last message in conversation */}
            <div className={styles.content}>
              {conversation.messages[conversation.messages.length - 1]?.content}
            </div>
          </div>
        </button>
      );
}