import styles from "./Conversation.module.css";
import { FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Input } from "../../../../components/Input/Input";
import { request } from "../../../../utils/api";
import {
  useAuthentication,
} from "../../../authentication/contexts/AuthenticationContextProvider";
import { useWebSocket } from "../../../ws/WebSocketContextProvider";





export function Conversation() {
  const [postingMessage, setPostingMessage] = useState(false);
  const [content, setContent] = useState("");
  const [suggestingUsers, setSuggestingUsers] = useState([]);
  const [search, setSearch] = useState("");
  const [selectedUser, setSelectedUser] = useState(null);
  const [conversation, setConversation] = useState(null);
  const [conversations, setConversations] = useState([]);
  const websocketClient = useWebSocket();
  const { id } = useParams();
  const navigate = useNavigate();
  const creatingNewConversation = id === "new";
  const { user } = useAuthentication();



  useEffect(() => {
    const subscription = websocketClient?.subscribe(
      `/users/${user?.id}/conversations`,
      (message) => {
        const conversation = JSON.parse(message.body);
        console.log(conversation);
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




  useEffect(() => {
    if (id == "new") {
      setConversation(null);
      request({
        endpoint: "/networking/connections",
        method: "GET",
        onSuccess: (data) => 
          setSuggestingUsers(data.map((c) => (c.author_id === user?.id ? c.recipient : c.sender))),
        onFailure: (error) => console.log(error),
      });
    } else {
      request({
        endpoint: `/api/v1/messaging/conversations/${id}`,
        onSuccess: (data) => setConversation(data),
        onFailure: () => navigate("/messaging"),
      });
    }
  }, [id, navigate]);


  useEffect(() => {
    const subscription = websocketClient?.subscribe(
      `/topic/conversations/${conversation?.id}/messages`,
      (data) => {
        const message = JSON.parse(data.body);

        setConversation((prevConversation) => {
          if (!prevConversation) return null;
          const index = prevConversation.messages.findIndex((m) => m.id === message.id);
          if (index === -1) {
            return {
              ...prevConversation,
              messages: [...prevConversation.messages, message],
            };
          }
          return {
            ...prevConversation,
            messages: prevConversation?.messages.map((m) => (m.id === message.id ? message : m)),
          };
        });
      }
    );
    return () => subscription?.unsubscribe();
  }, [conversation?.id, websocketClient]);


  
  async function addMessageToConversation(e) {
    e.preventDefault();
    setPostingMessage(true);
    await request({
      endpoint: `/api/v1/messaging/conversations/${conversation?.id}/messages`,
      method: "POST",
      body: JSON.stringify({
        receiverId:
          conversation?.recipient.id == user?.id
            ? conversation?.author.id
            : conversation?.recipient.id,
        content,
      }),
      onSuccess: () => {},
      onFailure: (error) => console.log(error),
    });
    setPostingMessage(false);
  }

  async function createConversationWithMessage() {
    e.preventDefault();

    const message = {
      recipient_id: selectedUser?.id,
      content,
    };

    await request({
      endpoint: "/messaging/conversations",
      method: "POST",
      body: JSON.stringify(message),
      onSuccess: (conversation) => navigate(`/messaging/conversations/${conversation.id}`),
      onFailure: (error) => console.log(error),
    });
  }

  const conversationUserToDisplay =
    conversation?.recipient.id === user?.id ? conversation?.author : conversation?.recipient;

  return (
    <div className={`${styles.root} ${creatingNewConversation ? styles.new : ""}`}>
      {(conversation || creatingNewConversation) && (
        <>
          <div className={styles.header}>
            <button className={styles.back} onClick={() => navigate("/messaging")}>
              {"<"}
            </button>
          </div>
          {conversation && (
            <div className={styles.top}>
              <button onClick={() => navigate(`/profile/${conversationUserToDisplay?.id}`)}>
                <img
                  className={styles.avatar}
                  src={conversationUserToDisplay?.profilePicture || "/avatar.svg"}
                  alt=""
                />
              </button>
              <div>
                <div className={styles.name}>
                  {conversationUserToDisplay?.first_name} {conversationUserToDisplay?.last_name}
                </div>
                <div className={styles.title}>
                  {conversationUserToDisplay?.position} at {conversationUserToDisplay?.company}
                </div>
              </div>
            </div>
          )}
          {creatingNewConversation && (
            <form className={`${styles.form} ${styles.new}`} onSubmit={(e) => e.preventDefault()}>
              <p style={{ marginTop: "1rem" }}>
                Starting a new conversation {selectedUser && "with:"}
              </p>
              {!selectedUser && (
                <Input
                  disabled={suggestingUsers.length === 0}
                  type="text"
                  name="recipient"
                  placeholder="Type a name"
                  onChange={(e) => setSearch(e.target.value)}
                  value={search}
                />
              )}

              {selectedUser && (
                <div className={styles.top}>
                  <img
                    className={styles.avatar}
                    src={selectedUser.profilePicture || "/avatar.svg"}
                    alt=""
                  />
                  <div>
                    <div className={styles.name}>
                      {selectedUser.first_name} {selectedUser.last_name}
                    </div>
                    <div className={styles.title}>
                      {selectedUser.position} at {selectedUser.company}
                    </div>
                  </div>
                  <button onClick={() => setSelectedUser(null)} className={styles.close}>
                    X
                  </button>
                </div>
              )}

              
              {/* if there is no selected user and no conversation, show suggestions */}
              {!selectedUser && !conversation && (
                <div className={styles.suggestions}>
                  {suggestingUsers
                    .filter(
                      (user) => user.first_name?.includes(search) || user.last_name?.includes(search)
                    )
                    .map((user) => (
                      <button
                        key={user.id}
                        onClick={() => {
                          // redirect user to prev existing conv if found 
                          const conversation = conversations.find(
                            (c) => c.recipient.id === user.id || c.author.id === user.id
                          );
                          if (conversation) {
                            navigate(`/messaging/conversations/${conversation.id}`);
                          } else {
                            setSelectedUser(user);
                          }
                        }}
                      >
                        <img
                          className={styles.avatar}
                          src={user.profilePicture || "/avatar.svg"}
                          alt=""
                        />
                        <div>
                          <div className={styles.name}>
                            {user.first_name} {user.last_name}
                          </div>
                          <div className={styles.title}>
                            {user.position} at {user.company}
                          </div>
                        </div>
                      </button>
                    ))}
                  {suggestingUsers.length === 0 && (
                    <div style={{ padding: "1rem" }}>
                      You need to have connections to start a conversation.
                    </div>
                  )}
                </div>
              )}
            </form>
          )}
          {conversation && 
            <Messages 
              messages={conversation.messages} 
              user={user} 
              conversationId={conversation.id}
            />
          }
            <div></div>
          <form
            className={styles.form}
            onSubmit={async (e) => {
              if (!content) return;
              if (conversation) {
                await addMessageToConversation(e);
              } else {
                await createConversationWithMessage(e);
              }
              setContent("");  // clear input 
              setSelectedUser(null);
            }}>
            <input
              onChange={(e) => setContent(e.target.value)}
              value={content}
              name="content"
              className={styles.textarea}
              placeholder="Write a message..."
            />
            <button
              type="submit"
              className={styles.send}
              disabled={
                postingMessage || !content.trim() || (creatingNewConversation && !selectedUser)
              }
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="currentColor">
                <path d="M16.1 260.2c-22.6 12.9-20.5 47.3 3.6 57.3L160 376l0 103.3c0 18.1 14.6 32.7 32.7 32.7c9.7 0 18.9-4.3 25.1-11.8l62-74.3 123.9 51.6c18.9 7.9 40.8-4.5 43.9-24.7l64-416c1.9-12.1-3.4-24.3-13.5-31.2s-23.3-7.5-34-1.4l-448 256zm52.1 25.5L409.7 90.6 190.1 336l1.2 1L68.2 285.7zM403.3 425.4L236.7 355.9 450.8 116.6 403.3 425.4z" />
              </svg>
            </button>
          </form>
        </>
      )}
    </div>
  );
}