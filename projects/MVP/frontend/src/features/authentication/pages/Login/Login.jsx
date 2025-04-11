import { Box } from '../../components/Box/Box'
import { Input } from '../../../../components/Input/Input'
import { Button } from '../../../../components/Button/Button'
import {Separator} from '../../components/Separator/Separator'
import styles from './Login.module.css'
import { Link , useNavigate, useLocation} from 'react-router-dom'
import { useState } from 'react'
import { useAuthentication } from '../../contexts/AuthenticationContextProvider'


export function Login() {
    const [errorMessage, setErrorMessage] = useState("");
    const [isLoading, setLoading] = useState(false);
    const {login} = useAuthentication(); 
    const navigate = useNavigate();
    const location = useLocation(); 

    const doLogin = async (event) => {
        event.preventDefault();
        setLoading(true);
        const email = event.currentTarget.email.value;
        const password = event.currentTarget.password.value;

        try {
            await login(email, password);
            const destination = "/"; 
            navigate(destination);

        } catch (error) {
            if (error instanceof Error) {
                setErrorMessage(error.message);
            } else {
                setErrorMessage("An unknown error occurred.");
            }
        } finally {
            setLoading(false);
        }
    }


    return (
        <div>
            <Box>
                <h1>Sign in</h1>
                <p>Join the professional tech community and start networking.</p>
                <form onSubmit={doLogin}>
                    <Input 
                        type="email" 
                        id="email" 
                        label="Email" 
                        onFocus={() => setErrorMessage("")}/>

                    <Input 
                        type="password" 
                        id="password" 
                        label="Password"
                        onFocus={() => setErrorMessage("")}/>

                    {errorMessage && <p className={styles.error}>{errorMessage}</p>}
                    <Button type="submit" disabled={isLoading}>
                        {isLoading ? "Signing in..." : "Sign in"}
                    </Button>
                    <Link to='/auth/reset-password'>Forgot password?</Link>
                </form>
                <Separator>Or</Separator>
                <div className={styles.register}>
                    Not a member?
                    {" "}<Link to="/auth/signup">Join now</Link>
                </div>
                
            </Box>
        </div>
    )
}