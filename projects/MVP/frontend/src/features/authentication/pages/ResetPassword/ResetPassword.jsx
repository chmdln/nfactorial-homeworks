import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { Box } from "../../components/Box/Box";
import { Input } from '../../../../components/Input/Input'; 
import { Button } from '../../../../components/Button/Button'; 
import styles from './ResetPassword.module.css'

export function ResetPassword() {
    const navigate = useNavigate();
    const [emailSent, setEmailSent] = useState(false);
    const [email, setEmail] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const sendPasswodResetToken = async (email) => {
        try {
            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/auth/password-reset-code`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ email }), 
                }
            );
            if (response.ok) {
                setErrorMessage("");
                setEmailSent(true);
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


    const resetPassword = async (code, password) => {
        try {
            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/auth/reset-password`, 
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ code, password }), 
                }
            );
            if (response.ok) {
                setErrorMessage("");
                navigate("/auth/login");
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
        <div className={styles.root}>
            <Box>
                <h1>Reset Password</h1>
                {
                    !emailSent ? (
                        <form 
                            onSubmit={async (e) => {
                                e.preventDefault();
                                setIsLoading(true);
                                const email = e.currentTarget.email.value;
                                await sendPasswodResetToken(email); 
                                setEmail(email); 
                                setIsLoading(false);
                            }}
                        >
                            <p>Enter your email and we'll send a verification code if it matches our records.</p>
                            <Input type="email" name="email" label="Email"/>

                            <p style={{color: "red"}}>{errorMessage}</p>
                            <Button type="submit">
                                Send Verification Code
                            </Button>
                            <Button type="button" outline onClick={()=> {navigate("/auth/login")}}>
                                Back to Login
                            </Button>
                        </form>
                    ) : (
                        <form onSubmit={async (e) => {
                            e.preventDefault();
                            setIsLoading(true);
                            const code = e.currentTarget.code.value;
                            const password = e.currentTarget.password.value;
                            await resetPassword(code, password);
                            setIsLoading(false);
                        }}>
                            <p>Enter the verification code we sent to your email and your new password.</p>
                            <Input 
                                type="text"
                                label="Verification Code" key="code"
                                name="code"
                            />
                            <Input 
                                type="password"
                                label="New Password" 
                                name="password" 
                                key="password"
                                id="password"
                            />
                            
                            <p style={{color: "red"}}>{errorMessage}</p>
                            <Button type="submit">
                                Reset password
                            </Button>
                            <Button 
                                type="button" 
                                outline 
                                onClick={()=> {
                                    setErrorMessage(""); 
                                    setEmailSent(false); 
                                }}
                            >
                                Back
                            </Button>
                        </form>
                    )
                }
            </Box>
        </div>
    )
}