import styles from './VerifyEmail.module.css';
import { Box } from "../../components/Box/Box";
import { Input } from '../../../../components/Input/Input'; 
import { Button } from '../../../../components/Button/Button'; 
import { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { useAuthentication } from '../../contexts/AuthenticationContextProvider';


export function VerifyEmail() {
    const [errorMessage, setErrorMessage] = useState("");
    const [message, setMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const  { user, setUser } = useAuthentication();
    const navigate = useNavigate();

    useEffect(() => {
        const alreadySent = localStorage.getItem("verificationEmailSent");
        if (!alreadySent) {
            sendEmailVerificationToken();
        }
    }, []);

    const validateEmail = async (code) => {
        setMessage("");
        try {
            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/auth/verify-email?token=${code}`, 
                {
                    method: "POST",
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`,
                    },
                }
            );
            if (response.ok) {
                setErrorMessage("");
                if (user) {
                    setUser({ ...user, is_verified: true });
                }
                localStorage.removeItem("verificationEmailSent");
                navigate("/"); 
            }
            const { message } = await response.json();
            setErrorMessage(message);
        } catch (error) {
            console.log(error);
            setErrorMessage("Something went wrong, please try again.");
        } finally {
            setIsLoading(false);}
    }; 


    const sendEmailVerificationToken = async () => {
        setErrorMessage("");
        try {
            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/auth/verify-email`,
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`,
                    },
                }
            );

            if (response.ok) {
                setErrorMessage("");
                setMessage("Code sent sussessfully. Please, check your email.");
                console.log('Setting verificationEmailSent flag');
                localStorage.setItem("verificationEmailSent", "true");
                return; 
            }
            const { message } = await response.json();
            setErrorMessage(message);
        } catch (error) {
            console.log(error);
            setErrorMessage("Something went wrong, please try again.");
        } finally {
            setIsLoading(false); 
        }
      };


    return (
        <div>
            <Box>
                <h1>Verify your email</h1>
                <form onSubmit={ async (event) => {
                    event.preventDefault();
                    setIsLoading(true);
                    const code = event.currentTarget.code.value;
                    await validateEmail(code);
                    setIsLoading(false);
                }}>
                    <p>Only one step left to complete your sign up. Verify your email address.</p>
                    <Input 
                        type="text"
                        label="Verification code"
                        key="code"
                        name="code">
                    </Input>

                    {message && <p style={{color: "green"}}>{message}</p>}
                    {errorMessage && <p style={{color: "red"}}>{errorMessage}</p>}
                    <Button type="submit" disabled={isLoading}>
                        Validate email
                    </Button>
                    <Button type="button" outline disabled={isLoading} onClick={
                        ()=>sendEmailVerificationToken()}>
                        Send again
                    </Button>
                </form>
            </Box>
        </div>
        
    )
}