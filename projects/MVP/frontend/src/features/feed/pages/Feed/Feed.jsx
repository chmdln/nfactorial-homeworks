import styles from './Feed.module.css';
import { useAuthentication } from '../../../authentication/contexts/AuthenticationContextProvider';
import { RightSidebar } from '../../components/RightSidebar/RightSidebar';
import { LeftSidebar } from '../../components/LeftSidebar/LeftSidebar';
import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Button } from '../../../../components/Button/Button';
import { Post } from '../../components/Post/Post';
import { Modal } from '../../components/Modal/Modal';
import { Loader } from '../../../../components/Loader/Loader';


export function Feed() {
    const { user, logout } = useAuthentication();
    const navigate = useNavigate();
    const [showPostingModal, setShowPostingModal] = useState(false);
    const [feedContent, setFeedContent] = useState("all");
    const [posts, setPosts] = useState([]);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/feed` + (feedContent === "connections" ? "" : "/posts"),
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${localStorage.getItem("token")}`,
                        },
                    }
                );
            if (!response.ok) {
                const { message } = await response.json();
                throw new Error(message);
            }

            const data = await response.json();
            setPosts(data);
            
            } catch (error) {
                if (error instanceof Error) {
                    setError(error.message);
                } else {
                    setError("An unknown error occurred. Please, try again later.");
                }
            }
        };

        fetchPosts();
    }, [feedContent]);

    const handlePost = async (formData) => {
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/feed/posts`, {
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
                body: formData,
            });

   
            if (!response.ok) {
                const { message } = await response.json();
                throw new Error(message);
            }

            const post = await response.json();
            setPosts([post, ...posts]); // Add the new post to the beginning of the feed
            setFeedContent("all"); 

        } catch (error) {
            setError(error.message || "An unknown error occurred. Please, try again later.");
        }
    };

    return (
        <div className={styles.root}>
          <div className={styles.left}>
            <LeftSidebar user={user} />
          </div>
          <div className={styles.center}>
            <div>
                <div className={styles.posting}>
                <button
                    onClick={() => {
                    navigate(`/profile/${user?.id}`);
                    }}
                >
                    <img
                    className={`${styles.top} ${styles.avatar}`}
                    src={
                        user?.profilePicture
                        ? `${import.meta.env.VITE_API_URL}/api/v1/storage/${user?.profilePicture}`
                        : "/avatar.svg"
                    }
                    alt=""
                    />
                </button>
                <Button outline onClick={() => setShowPostingModal(true)}>
                    Start a post
                </Button>
                <Modal
                    title="Creating a post"
                    onSubmit={handlePost}
                    showModal={showPostingModal}
                    setShowModal={setShowPostingModal}
                />
                </div>
                <div className={styles.header}>
                    <button 
                        className={feedContent==="all" ? styles.active : ""}
                        onClick={()=>setFeedContent("all")}
                    >
                        All
                    </button>
                    <button
                        className={feedContent==="connections" ? styles.active : ""}
                        onClick={()=>setFeedContent("connections")}
                    >
                        Feed 
                    </button>
                </div>
            </div>
            
            {error && <div className={styles.error}>{error}</div>}

            {loading ? (
            <Loader isInline />
            ) : (
            <div className={styles.feed}>
                {posts.map((post) => (
                <Post key={post.id} post={post} setPosts={setPosts} />
                ))}
                {posts.length === 0 && (
                <p>Start connecting with people to build a feed that matters to you.</p>
                )}
            </div>
            )}
          </div>
          <div className={styles.right}>
            <RightSidebar />
          </div>
        </div>
      );
}
