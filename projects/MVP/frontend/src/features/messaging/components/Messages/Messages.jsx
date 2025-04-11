import styles from "./Messages.module.css";
import { Message } from "../Message/Message";

export function Messages({messages, user, conversationId}) {
    return (    
        <div className={styles.root}>
            {messages.map((message) => (
                <Message 
                    key={message.id} 
                    message={message} 
                    user={user} 
                />
            ))}
        </div>
    );  
}