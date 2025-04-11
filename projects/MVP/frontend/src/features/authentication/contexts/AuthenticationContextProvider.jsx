import { createContext, useContext } from 'react';
import {useLocation, Outlet, Navigate} from 'react-router-dom';
import {useEffect, useState} from 'react';
import { Loader } from '../../../components/Loader/Loader';

const AuthenticationContext = createContext(null);

export function useAuthentication() {
    return useContext(AuthenticationContext);
}

export function AuthenticationContextProvider() {
    const location = useLocation();
    const [user, setUser] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    const isOnAuthPage =
    location.pathname === "/auth/login" ||
    location.pathname === "/auth/signup" ||
    location.pathname === "/auth/reset-password"; 

    const login = async (email, password) => {
        const response = await fetch(import.meta.env.VITE_API_URL + "/auth/login", 
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email, password }),
        });
          
        if (response.ok) {
            const { access_token } = await response.json();
            localStorage.setItem("token", access_token);
            await fetchUser();
            
        } else {
            let errorMessage = "An unknown error occurred. Please, try again.";
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorMessage;
            } catch (err) {
                console.error("Failed to parse error response:", err);
            }
            throw new Error(errorMessage);
        }
      };

      
    const signup = async (email, password) => {
        const response = await fetch(import.meta.env.VITE_API_URL + "/auth/signup",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
            const { access_token } = await response.json();
            localStorage.setItem("token", access_token);
        }
        
        else {
            let errorMessage = "An unknown error occurred. Please, try again.";
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorMessage; 
            } catch (err) {
                console.error("Failed to parse error response:", err);
            }
            throw new Error(errorMessage);
        }
      };
    
    const logout = () => {
        localStorage.removeItem("token");
        setUser(null);
    }

    const fetchUser = async () => {
        try {
            const response = await fetch(import.meta.env.VITE_API_URL + "/users/me", {
                headers: {
                  Authorization: `Bearer ${localStorage.getItem("token")}`,
                }}
              );
            
            if (!response.ok) {
                throw new Error("Authentication failed");
            }
            const user = await response.json();
            setUser(user);
        } catch (error) {
            console.error(error);
        }
        finally {
            setIsLoading(false);
        }
    };


    // get the user when the page is loaded 
    useEffect(() => {
        if (user) {
          return;
        }
        setIsLoading(true);
        fetchUser();
      }, [user, location.pathname]);

    if (isLoading) {
        return <Loader />;
    }

    if (!isLoading && !user && !isOnAuthPage) {
        return <Navigate to="/auth/login" state={{ from: location.pathname }} />;
      }
    
    if (user && user.is_verified === false && location.pathname !== "/auth/verify-email") {
    return <Navigate to="/auth/verify-email" />;
    }

    if (user && user.is_verified === true && location.pathname === "/auth/verify-email") {
      console.log("here1");
      return <Navigate to="/" />;
      }

    if (
      user &&
      user.is_verified &&
      !user.is_profile_complete &&
      !location.pathname.includes("/auth/profile")
    ) {
      return <Navigate to={`/auth/profile/`} />;
    }

    if (
      user &&
      user.is_verified &&
      user.is_profile_complete &&
      location.pathname.includes("/auth/profile/")
    ) {
      console.log("here2");
      return <Navigate to="/" />;
    }

    if (user && isOnAuthPage) {
      return <Navigate to={location.state?.from || "/"} />;
    }
 
    

    return (
        <AuthenticationContext.Provider value={{
            setUser,
            user, 
            login, 
            signup,
            logout
        }}> 
            <Outlet />
        </AuthenticationContext.Provider>
    )
}
