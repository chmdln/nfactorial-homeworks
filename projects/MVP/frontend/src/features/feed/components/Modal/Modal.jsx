import styles from './Modal.module.css'
import { useState, useRef } from 'react';
import { Input } from '../../../../components/Input/Input';
import { Button } from '../../../../components/Button/Button';


export function Modal({
    setShowModal,
    showModal,
    title,
    onSubmit,
    content,
    picture,
}) {

    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const textareaRef = useRef(null);
    const [preview, setPreview] = useState(picture);
    const [file, setFile] = useState();

    if (!showModal) return null;


    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        const content = e.currentTarget.content.value;
        const formData = new FormData();
    
        if (file) {
          formData.append("uploaded_file", file);
        }
    
        if (!content) {
          setError("Content is required");
          setIsLoading(false);
          return;
        }
    
        formData.append("content", content);
    
        try {
          await onSubmit(formData);
          setPreview(undefined);
          setShowModal(false);
        } catch (error) {
          if (error instanceof Error) {
            setError(error.message);
          } else {
            setError("An error occurred. Please try again later.");
          }
        } finally {
          setIsLoading(false);
        }
      };

    
    const handleImageChange = (e) => {
      setError("");
      const selectedFile = e.target.files?.[0];
  
      if (!selectedFile) return;
  
      if (!selectedFile.type.startsWith("image/")) {
        setError("Please select an image file");
        return;
      }
  
      setFile(selectedFile);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
  
      reader.readAsDataURL(selectedFile);
    };
    

    return (
        <div className={styles.root}>
          <div className={styles.modal}>
            <div className={styles.header}>
              <h3 className={styles.title}>{title}</h3>
              <button className={styles.close} onClick={() => setShowModal(false)}>
                X
              </button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className={styles.body}>
                <textarea
                  placeholder="What do you want to talk about?"
                  onFocus={() => setError("")}
                  onChange={() => setError("")}
                  name="content"
                  ref={textareaRef}
                  defaultValue={content}
                />
              
                {!preview ? (
                  <Input
                    onFocus={() => setError("")}
                    accept="image/*"
                    onChange={(e) => handleImageChange(e)}
                    placeholder="Image URL (optional)"
                    name="picture"
                    type="file"
                    style={{
                      marginBlock: 0,
                    }}
                  />
                ) : (
                  <div className={styles.preview}>
                    <button
                      className={styles.cancel}
                      type="button"
                      onClick={() => {
                        setPreview(undefined); 
                      }}
                    >
                      X
                    </button>
                    <img src={`${import.meta.env.VITE_API_URL}/${preview}`} alt="Preview" className={styles.preview} />
                  </div>
                )}
              </div>
              {error && <div className={styles.error}>{error}</div>}
              <div className={styles.footer}>
                <Button size="medium" type="submit" disabled={isLoading}>
                  Post
                </Button>
              </div>
            </form>
          </div>
        </div>
      );
}