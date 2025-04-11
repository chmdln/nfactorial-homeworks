import styles from "./Comment.module.css";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { useAuthentication } from "../../../authentication/contexts/AuthenticationContextProvider";
import { Input } from "../../../../components/Input/Input";
import { TimeAgo } from "../TimeAgo/TimeAgo";


export function Comment({comment, deleteComment, editComment}) {
    const navigate = useNavigate();
    const { user } = useAuthentication();
    const [editing, setEditing] = useState(false);
    const [showActions, setShowActions] = useState(false);
    const [commentContent, setCommentContent] = useState(comment.content);


    return (
        <div key={comment.id} className={styles.root}>
            {!editing ? (
                <>
                <div className={styles.header}>
                    <button
                        onClick={() => {
                            navigate(`/profile/${comment.user.id}`);
                        }}
                        className={styles.user}
                    >
                        <img
                            className={styles.avatar}
                            src={comment.user?.profilePicture || "/avatar.svg"}
                            alt=""
                        />
                        <div>
                            <div className={styles.name}>
                            {comment.user.first_name + " " + comment.user.last_name}
                            </div>
                            <div className={styles.title}>
                            {comment.user.position + " at " + comment.user.company}
                            </div>
                            <TimeAgo date={comment.created_at} edited={!!comment.updated_at} />
                        </div>
                    </button>
                    {comment.user.id == user?.id && (
                        <button
                            className={`${styles.action} ${showActions ? styles.active : ""}`}
                            onClick={() => setShowActions(!showActions)}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 512">
                            <path d="M64 360a56 56 0 1 0 0 112 56 56 0 1 0 0-112zm0-160a56 56 0 1 0 0 112 56 56 0 1 0 0-112zM120 96A56 56 0 1 0 8 96a56 56 0 1 0 112 0z" />
                            </svg>
                        </button>
                    )}

                    {showActions && (
                    <div className={styles.actions}>
                        <button onClick={() => setEditing(true)}>Edit</button>
                        <button onClick={() => deleteComment(comment.id)}>Delete</button>
                    </div>
                    )}
                </div>
                <div className={styles.content}>{comment.content}</div>
                </>
            ) : (
                <form
                    onSubmit={async (e) => {
                        e.preventDefault();
                        await editComment(comment.id, commentContent);
                        setEditing(false);
                        setShowActions(false);
                    }}
                >
                    <Input
                        type="text"
                        value={commentContent}
                        onChange={(e) => {setCommentContent(e.target.value);}}
                        placeholder="Edit your comment"
                    />
                </form>
            )}
        </div>
    )
}