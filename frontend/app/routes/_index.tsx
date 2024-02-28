import ChatList from "~/components/ChatList";
import useAuthenticationGuard from "~/hooks/useAuthenticationGuard";


export default function Index() {
  useAuthenticationGuard()

  return (
    <div style={{ height: '100%' }}>
      <h1>Messages</h1>
      <ChatList />
    </div>
  );
}
