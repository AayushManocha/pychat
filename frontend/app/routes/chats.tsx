import { Outlet } from "@remix-run/react";
import ChatList from "~/components/ChatList";
import useAuthenticationGuard from "~/hooks/useAuthenticationGuard";

export default function Chats() {
  useAuthenticationGuard()
  return (
    <div style={{ height: '100%' }}>
      <h1>Messages</h1>
      <div style={{ display: 'flex', flexDirection: 'row' }}>
        <ChatList />
        <div style={{ width: '100%' }}>
          <Outlet />
        </div>
      </div>
    </div>
  );
}