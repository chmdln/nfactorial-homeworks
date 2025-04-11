import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Feed } from './features/feed/pages/Feed/Feed'
import { Login } from './features/authentication/pages/Login/Login'
import { Signup } from './features/authentication/pages/Signup/Signup'
import { ResetPassword } from './features/authentication/pages/ResetPassword/ResetPassword'
import { VerifyEmail } from './features/authentication/pages/VerifyEmail/VerifyEmail'
import './index.css'
import { AuthenticationContextProvider } from './features/authentication/contexts/AuthenticationContextProvider'
import { AuthLayout } from './features/authentication/components/AuthLayout/AuthLayout'
import { ApplicationLayout  } from './components/ApplicationLayout/ApplicationLayout'
import { Navigate } from 'react-router-dom'
import { Profile } from './components/Header/components/Profile'
import { Profile as LoginProfile } from './features/authentication/pages/Profile/Profile'
import { Messaging } from './features/messaging/pages/Messaging/Messaging'
import { Conversation } from './features/messaging/pages/Conversation/Conversation'


const router = createBrowserRouter([
  {
    element: <AuthenticationContextProvider />,
    children: [
      {
        path: "/",
        element: <ApplicationLayout />,
        children: [
          {
            index: true,
            element: <Feed />
          },
          // {
          //   path: "posts/:id",
          //   element: <PostPage />,
          // },
          {
            path: "network",
            element: <div>Network</div>,
            // children: [
            //   {
            //     index: true,
            //     element: <Navigate to="invitations" />,
            //   },
            //   {
            //     path: "invitations",
            //     element: <Invitations />,
            //   },
            //   {
            //     path: "connections",
            //     element: <Connections />,
            //   },
            // ],
          },
          {
            path: "jobs",
            element: <div>Jobs</div>,
          },
          {
            path: "messaging",
            element:<Messaging />,
            children: [
              {
                path: "conversations/:id",
                element: <Conversation />,
              },
            ],
          },
          {
            path: "notifications",
            element: <div>Notifications</div>
          },
          {
            path: "profile/:id",
            element: <div>Profile</div>
          },
          // {
          //   path: "profile/:id/posts",
          //   element: <Posts />,
          // },
          {
            path: "settings",
            element: <div>Settings</div>
          }
        ],
      },
      {
        path: "/auth", 
        element: <AuthLayout />,
        children: [
          {
            path: "login",
            element: <Login />
          },
          {
            path: "signup",
            element: <Signup />
          },
          {
            path: "reset-password",
            element: <ResetPassword />
          },
          {
            path: "verify-email",
            element: <VerifyEmail />
          },
          {
            path: "profile",
            element: <LoginProfile /> 
          }
        ]
      },
      {
        path: "*",
        element: <Navigate to="/" />
      }
    ]
  }
])


createRoot(document.getElementById('root')).render(
  // <StrictMode>
  <>
    <RouterProvider router={router} />
      <div>
      </div>
  </>
  // </StrictMode>
)
