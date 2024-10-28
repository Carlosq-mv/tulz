import axios from "axios"

const baseUrl = import.meta.env.VITE_REACT_APP_URL 

const Axios = axios.create({
    baseURL: baseUrl,
    withCredentials: true,
    headers: {
        "Content-Type" : "application/json"
    }
})

export default Axios