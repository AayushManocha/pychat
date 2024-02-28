import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import useAuthenticationGuard from "~/hooks/useAuthenticationGuard";


export default function Index() {
  const auth = useAuthenticationGuard()
  const { isLoading, isError, data } = useQuery({
    queryKey: ["chats"],
    queryFn: async () => {
      const res = await axios.get("http://localhost:8000/chat", { withCredentials: true })
      return res.data
    }
  })

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div>Error</div>

  return (
    <div>
      <h1>Messages</h1>
      {JSON.stringify(data)}
    </div>
  );
}
