import { LinksFunction } from "@remix-run/node";
import {
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
  useNavigate,
} from "@remix-run/react";

import stylesheet from './tailwind.css'
import React, { useEffect } from "react";
import { set } from "node_modules/cypress/types/lodash";
import axios from "axios";
import { Query, QueryClient, QueryClientProvider } from "@tanstack/react-query";

export const links: LinksFunction = () => [
  // { rel: "stylesheet", href: stylesheet },
  { rel: "stylesheet", href: "https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css" }

];

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body>
        {children}
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}

// Create React Context to store the user's authentication state
interface IUserContext {
  user: any;
  setUser: (user: any) => void;
  isAuthenticated: () => boolean;
  fetchUser: () => Promise<any>;
}

export const UserContext = React.createContext<IUserContext | null>(null);
const UserContextProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = React.useState<any>();

  const isAuthenticated = () => {
    return user !== null;
  }

  const fetchUser = async () => {
    return axios.get("http://localhost:8000/me", {
      withCredentials: true
    }).then(res => res.data)
      .then(res => {
        setUser(res)
        return res
      })
      .catch(err => {
        setUser(null)
        return null
      })
  }

  return (
    <UserContext.Provider value={{ user, setUser, isAuthenticated, fetchUser }}>
      {children}
    </UserContext.Provider>
  );
}

const queryClient = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <UserContextProvider>
        <Outlet />
      </UserContextProvider>
    </QueryClientProvider>
  )
}

export function HydrateFallback() {
  return <p>Loading...</p>;
}
