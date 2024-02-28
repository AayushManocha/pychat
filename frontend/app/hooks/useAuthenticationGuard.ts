import { useNavigate } from "@remix-run/react";
import { use } from "chai";
import { useContext, useEffect, useState } from "react";
import { UserContext } from "~/root";

export default function useAuthenticationGuard() {
  const userContext = useContext(UserContext)
  const navigiate = useNavigate()

  if (!userContext) {
    throw new Error("useAuthenticationGuard must be used within a UserContextProvider")
  }

  useEffect(() => {
    async function checkUser() {
      const user = await userContext?.fetchUser()
      if (!user) {
        navigiate("/login")
      }
    }
    checkUser()
  }, [])
}