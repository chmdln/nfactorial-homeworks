import { Box } from '../../components/Box/Box'
import { Input } from '../../../../components/Input/Input'
import { Button } from '../../../../components/Button/Button'; 
import {Separator} from '../../components/Separator/Separator'
import styles from './Signup.module.css'
import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { useAuthentication } from '../../contexts/AuthenticationContextProvider'


export function Signup() {
    const [errorMessage, setErrorMessage] = useState("");
    const { signup } = useAuthentication();
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const doSignup = async (event) => {
        event.preventDefault();
        setIsLoading(true);
        const email = event.currentTarget.email.value;
        const password = event.currentTarget.password.value;
        console.log(email, password);

        try {
            await signup(email, password);
            navigate("/");

        } catch (error) {
            if (error instanceof Error) {
                const cleanMessage = error.message.replace(/^\d+:\s*/, "");  
                setErrorMessage(cleanMessage);
            } else {
                setErrorMessage("An unknown error occurred.");
            }
        } finally {
            setIsLoading(false);
        }   
    }


    return (
        <div>
            <Box>
                <h1>Sign up</h1>
                <p>Make the most of your professional life</p>
                <form onSubmit={doSignup}>
                    <Input type="email" id="email" label="Email"/>
                    <Input type="password" id="password" label="Password"/>
                    {errorMessage && <p className={styles.error}>{errorMessage}</p>}
                    <Button type="submit" disabled={isLoading}>Agree & Join</Button>
                </form>
                <Separator>Or</Separator>
                <div className={styles.register}>
                    Already a member?
                    {" "}<Link to="/auth/login">Sign in</Link>
                </div>
                
            </Box>
        </div>
    )
}