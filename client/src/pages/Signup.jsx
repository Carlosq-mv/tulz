import Axios from "../constants/api"
import { useEffect, useState, useContext } from "react"
import FormField from "../components/FormField"
import APP_NAME from "../constants/constants"
import AlertComponent from "../components/AlertComponent"
import { useNavigate } from "react-router-dom"
import { AuthContext } from "../context/AuthProvider"


function Signup() {
  const navigate = useNavigate()
  const { currentUser, isLoggedIn } = useContext(AuthContext)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showModal, setShowModal] = useState(false)
  const [form, setForm] = useState({
    name: "",
    username: "",
    email: "",
    password: "",
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    Axios.post("/user/create-account", form)
      .then(res => {
        setForm({
          name: "",
          username: "",
          email: "",
          password: ""
        })
        console.log(res)
        setShowModal(true)
      })
      .catch(err => {
        console.log(err.response)
        if (err.response.data) {
          // Extract the error message
          const errorMessage = err.response.data.detail || "An unknown error occurred.";
          setError(errorMessage);
        }
      })
      .finally(() => {
        setLoading(false)
      })
  }

  // if user is loggedIn redirect to homepage
  if (isLoggedIn && currentUser) {
    navigate("/home")
  }
  return (
    <>
      <div className="flex items-center justify-center min-h-screen">
        <div className="card bg-base-100 w-full sm:w-2/6 shadow-xl">
          <figure className="px-8 pt-8">
            <img
              src={`/images/caldera.jpg`}
              alt="Example"
              className="rounded-xl"
            />

          </figure>
          <div className="card-body items-center text-center">
            <h2 className="card-title">Sign up to {APP_NAME}</h2>

            <form onSubmit={handleSubmit}>
              <FormField
                name="name"
                title="Name:"
                value={form.name}
                placeholder="e.g. Carlos"
                handleTextChange={(e) => setForm({ ...form, name: e.target.value })}
              />
              <FormField
                name="username"
                title="Username:"
                value={form.username}
                placeholder="e.g. barlost"
                handleTextChange={(e) => setForm({ ...form, username: e.target.value })}
              />
              <FormField
                type="email"
                name="email"
                title="Email:"
                value={form.email}
                placeholder="user@example.com"
                handleTextChange={(e) => setForm({ ...form, email: e.target.value })}
              />
              <FormField
                type="password"
                name="password"
                title="Password:"
                value={form.password}
                handleTextChange={(e) => setForm({ ...form, password: e.target.value })}
              />

              {error && <AlertComponent errorMessage={error} />}

              <p></p>
              <div className="card-actions flex justify-center">
                <div className="flex w-full flex-col border-opacity-50 pt-2">
                  <button type="submit" className="btn btn-active">
                    {loading ? <span className="loading loading-dots loading-lg"></span> : "Create Account"}
                  </button>
                  <div className="divider">OR</div>
                  <a className="text-blue-500" href="/login">Login To Account</a>
                </div>
              </div>

            </form>

            {showModal && (
              <dialog id="my_modal_1" className="modal" open>
                <div className="modal-box">
                  <h3 className="font-bold text-lg">{`Hello! Welcome to ${APP_NAME}!`}</h3>
                  <p className="py-4 text-md">
                    Congratulations! Your account has been created. You can now log in and start using our services!"
                  </p>
                  <p className="py-4 text-sm">
                    <a className="text-blue-500 font-black" href="/login">Login Here</a>
                  </p>
                  <div className="modal-action">
                    <form method="dialog">
                      <button onClick={() => setShowModal(false)} className="btn">Close</button>
                    </form>
                  </div>
                </div>
              </dialog>
            )}

          </div>
        </div>
      </div>
    </>
  )
}

export default Signup