import { createContext, useState, useEffect } from "react"
import Axios from "../constants/api"

const AuthContext = createContext()

const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [currentUser, setCurrentUser] = useState(null)
  const [loading, setLoading] = useState(false)

  const fetchUser = async () => {
    setLoading(true)
    try {
      const res = await Axios.get("/user/current-user")
      // res.data is formatted already
      const user = res.data
      console.log(user)
      if (user) {
        setCurrentUser(user)
        setIsLoggedIn(user.is_logged_in)
      } else {
        setCurrentUser(null)
        setIsLoggedIn(false)
      }
    } catch (err) {
      console.log(err.response)
      setCurrentUser(null)
      setIsLoggedIn(false)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchUser()
  }, [])

  return (
    <AuthContext.Provider
      value={{ setIsLoggedIn, isLoggedIn, setCurrentUser, currentUser, fetchUser, loading }}
    >
      {children}
    </AuthContext.Provider>
  )
}
export { AuthContext, AuthProvider }
