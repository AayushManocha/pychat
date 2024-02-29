import { Outlet } from "@remix-run/react";
import ChatList from "~/components/ChatList";

export default function Chats() {
  return (
    <div style={{ height: '100%' }}>
      <h1>Messages</h1>
      <div style={{ display: 'flex', flexDirection: 'row' }}>
        <ChatList />
        <div style={{ border: '2px red solid', width: '100%' }}>
          <Outlet />
        </div>
      </div>
    </div>
  );
}