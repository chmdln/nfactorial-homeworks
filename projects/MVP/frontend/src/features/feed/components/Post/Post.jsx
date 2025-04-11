import styles from "./Post.module.css";
import { use, useEffect } from "react";
import { useAuthentication } from "../../../authentication/contexts/AuthenticationContextProvider";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { Input } from "../../../../components/Input/Input";
import { TimeAgo } from "../TimeAgo/TimeAgo";
import { Comment } from "../Comment/Comment";
import { Modal } from "../Modal/Modal";

export function Post({post, setPosts}) {
    const navigate = useNavigate();
    const { user } = useAuthentication();
    const [editing, setEditing] = useState(false);
    const [showMenu, setShowMenu] = useState(false);
    const [likes, setLikes] = useState([]);
    const [comments, setComments] = useState([]);
    const [showComments, setShowComments] = useState(false);
    const [postLiked, setPostLiked] = useState(undefined);
    const [content, setContent] = useState("");

    


    useEffect(() => {
        setPostLiked(!!post.likes?.some((like) => like.user_id === user?.id));
    }, [post.likes, user?.id]);

    const like = async () => {
        // toggle the post liked state, optimistic update 
        setPostLiked((prev) => !prev);
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/feed/posts/${post.id}/like`, {
                method: postLiked ? "DELETE" : "POST",
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`
                },
            });
            if (!response.ok) {
                const { message } = await response.json();
                throw new Error(message);
            }
        } catch (error) {
            if (error instanceof TypeError) {
                console.error(error.message);
            } else {
                console.error("An error occurred while liking the post. Please, try again later.");
            }
            // revert the optimistic update, if error occurs
            setPostLiked((prev) => !prev);
        }
    };
    

    const editPost = async (formData) => {
        const  response = await fetch(`${import.meta.env.VITE_API_URL}/feed/posts/${post.id}`, {
            method: "PUT",
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,   
            },
            body: formData,
        });
        if (!response.ok) {
            const { message } = await response.json();
            throw new Error(message);
        }
        const data = await response.json();
        setPosts((prevPosts) => {
            return prevPosts.map((p) => {
                if (p.id === post.id) {
                    return data;  
                }
                return p;  
            });
        });
        setShowMenu(false);
    };


    const deletePost = async (id) => {
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/feed/posts/${id}`, {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            });
            if (!response.ok) {
                const { message } = await response.json();
                throw new Error(message);
            }
            setPosts((prevPosts) => prevPosts.filter((p) => p.id !== id));
        } catch (error) {
            console.error(error);
        }
    };


    const postComment = async (e) => {
        e.preventDefault();
        if (content.trim() === "") return;
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/feed/posts/${post.id}/comments`, {
                method: "POST",        
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
                body: JSON.stringify({ content }),
            });
            if (!response.ok) {
                const { message } = await response.json();
                throw new Error(message);
            }
            const comment = await response.json();
            setPosts((prevPosts) => {
                return prevPosts.map((p) => {
                    if (p.id === post.id) {
                        return {
                            ...p,
                            comments: [comment, ...(p.comments || [])],
                        };
                    }
                    return p;
                }
                );
            });
            setContent("");
        } catch (error) {
            if (error instanceof TypeError) {
                console.error(error.message);
            } else {
                console.error("An error occurred while posting the comment. Please, try again later.");
            }
        };
    };
           

    const deleteComment = async (id) => {
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/feed/posts/${post.id}/comments/${id}`, {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            });
            if (!response.ok) {
                const { message } = await response.json();
                throw new Error(message);
            }
            setPosts((prevPosts) => {
                return prevPosts.map((p) => {
                    if (p.id === post.id) {
                        return {
                            ...p,
                            comments: p.comments?.filter((comment) => comment.id !== id),
                        };
                    }
                    return p;
                });
            });
        } catch (error) {
            console.error(error);
        }
    };


    const editComment = async (id, content) => {    
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/feed/posts/${post.id}/comments/${id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
                body: JSON.stringify({ content }),
            });
            if (!response.ok) {
                const { message } = await response.json();
                throw new Error(message);
            }
            // optimistic update
            // find the post and update the comment
            setPosts((prevPosts => {
                return prevPosts.map((p) => {
                    if (p.id === post.id) {
                        return {
                            ...p,
                            comments: p.comments?.map((comment) => {
                                if (comment.id === id) {
                                    return {
                                        ...comment,
                                        content,
                                        updatedDate: new Date().toISOString(),
                                    };
                                }
                                return comment;
                            }),
                        };
                    }
                    return p;
                });
            }));
        } catch (error) {
            console.error(error);
        }   
    }

    return (
        <>
            <Modal 
                setShowModal={setEditing}
                onSubmit={editPost}
                showModal={editing} 
                title="Editing a post" 
                content={post.content} 
                picture={post.media_url}
            />

            <div className={styles.root}>
                
                <div className={styles.top}>
                    <div className={styles.author}>
                        <button
                            onClick={() => {
                                navigate(`/profile/${post.user.id}`);
                            }}
                            >
                            <img className={styles.avatar} src="/avatar.svg" alt=""/>
                        </button>
                        <div>
                            <div className={styles.name}>
                                {post.user.first_name + " " + post.user.last_name}
                            </div>
                            <div className={styles.title}>
                                {post.user.position + " at " + post.user.company}
                            </div>
                        
                            <TimeAgo
                                date={post.created_at}
                                edited={new Date(post.updated_at).toISOString().slice(0, 19) !== new Date(post.created_at).toISOString().slice(0, 19)}
                                className={styles.date}
                            />
                            {/* {post.updated_at ? " . Edited " : ""}     */}
                        </div>
                    </div>
                    <div>
                        {/* only show the button if the user is the author */}
                        {post.user.id == user?.id && (
                        <button
                            className={`${styles.toggle} ${showMenu ? styles.active : ""}`}
                            onClick={() => setShowMenu(!showMenu)}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 512">
                            <path d="M64 360a56 56 0 1 0 0 112 56 56 0 1 0 0-112zm0-160a56 56 0 1 0 0 112 56 56 0 1 0 0-112zM120 96A56 56 0 1 0 8 96a56 56 0 1 0 112 0z" />
                            </svg>
                        </button>
                        )}
                        {showMenu && (
                        <div className={styles.menu}>
                            <button onClick={() => setEditing(true)}>Edit</button>
                            <button onClick={() => deletePost(post.id)}>Delete</button>
                        </div>
                        )}
                    </div>
                </div>
                <div className={styles.content}>{post.content}</div>

                {post.media_url && (
                    <img
                        src={`${import.meta.env.VITE_API_URL}/${post.media_url}`}
                        alt=""
                        className={styles.picture}
                    />
                )}

                <div className={styles.stats}>
                    {likes.length > 0 ? (
                        <div className={styles.stat}>
                            <span>{postLiked ? "You " : likes[0].first_name + " " + likes[0].last_name + " "}</span>
                            {likes.length - 1 > 0 ? (
                                <span>
                                and {likes.length - 1} {likes.length - 1 === 1 ? "other" : "others"}
                                </span>
                            ) : null}{" "}
                            liked this
                        </div>
                    ) : (
                        <div></div>
                    )}

                    {post.comments.length > 0 ? (
                        <button className={styles.stat} onClick={() => setShowComments((prev) => !prev)}>
                        <span>{post.comments.length} comments</span>
                        </button>
                    ) : (
                        <div></div>
                    )}
                </div>

                <div className={styles.actions}>
                    <button
                        disabled={postLiked == undefined}
                        onClick={like}
                        className={postLiked ? styles.active : ""}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="currentColor">
                        <path d="M225.8 468.2l-2.5-2.3L48.1 303.2C17.4 274.7 0 234.7 0 192.8l0-3.3c0-70.4 50-130.8 119.2-144C158.6 37.9 198.9 47 231 69.6c9 6.4 17.4 13.8 25 22.3c4.2-4.8 8.7-9.2 13.5-13.3c3.7-3.2 7.5-6.2 11.5-9c0 0 0 0 0 0C313.1 47 353.4 37.9 392.8 45.4C462 58.6 512 119.1 512 189.5l0 3.3c0 41.9-17.4 81.9-48.1 110.4L288.7 465.9l-2.5 2.3c-8.2 7.6-19 11.9-30.2 11.9s-22-4.2-30.2-11.9zM239.1 145c-.4-.3-.7-.7-1-1.1l-17.8-20-.1-.1s0 0 0 0c-23.1-25.9-58-37.7-92-31.2C81.6 101.5 48 142.1 48 189.5l0 3.3c0 28.5 11.9 55.8 32.8 75.2L256 430.7 431.2 268c20.9-19.4 32.8-46.7 32.8-75.2l0-3.3c0-47.3-33.6-88-80.1-96.9c-34-6.5-69 5.4-92 31.2c0 0 0 0-.1 .1s0 0-.1 .1l-17.8 20c-.3 .4-.7 .7-1 1.1c-4.5 4.5-10.6 7-16.9 7s-12.4-2.5-16.9-7z" />
                        </svg>
                        <span>{postLiked == undefined ? "Loading" : postLiked ? "Liked" : "Like"}</span>
                    </button>
                    <button
                        onClick={() => {
                        setShowComments((prev) => !prev);
                        }}
                        className={showComments ? styles.active : ""}
                    >
                        <svg fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path d="M123.6 391.3c12.9-9.4 29.6-11.8 44.6-6.4c26.5 9.6 56.2 15.1 87.8 15.1c124.7 0 208-80.5 208-160s-83.3-160-208-160S48 160.5 48 240c0 32 12.4 62.8 35.7 89.2c8.6 9.7 12.8 22.5 11.8 35.5c-1.4 18.1-5.7 34.7-11.3 49.4c17-7.9 31.1-16.7 39.4-22.7zM21.2 431.9c1.8-2.7 3.5-5.4 5.1-8.1c10-16.6 19.5-38.4 21.4-62.9C17.7 326.8 0 285.1 0 240C0 125.1 114.6 32 256 32s256 93.1 256 208s-114.6 208-256 208c-37.1 0-72.3-6.4-104.1-17.9c-11.9 8.7-31.3 20.6-54.3 30.6c-15.1 6.6-32.3 12.6-50.1 16.1c-.8 .2-1.6 .3-2.4 .5c-4.4 .8-8.7 1.5-13.2 1.9c-.2 0-.5 .1-.7 .1c-5.1 .5-10.2 .8-15.3 .8c-6.5 0-12.3-3.9-14.8-9.9c-2.5-6-1.1-12.8 3.4-17.4c4.1-4.2 7.8-8.7 11.3-13.5c1.7-2.3 3.3-4.6 4.8-6.9l.3-.5z" />
                        </svg>
                        <span>Comment</span>
                    </button>
                </div>
                
                {showComments ? (
                    <div className={styles.comments}>
                        <form onSubmit={postComment}>
                            <Input
                                onChange={(e)=> setContent(e.target.value)}
                                value={content}
                                placeholder="Add a comment..."
                                name="content"
                                style={{marginBlock: 0}}
                            />
                        </form>
                        {
                            post.comments?.map((comment) => (
                                <Comment
                                    editComment={editComment}
                                    deleteComment={deleteComment}
                                    key={comment.id}
                                    comment={comment}
                                />
                            ))
                        }
                    </div>
                ) : null}
            </div>
        </>
    )
}
