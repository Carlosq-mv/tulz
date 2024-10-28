import { useState } from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa";

function FormField({ name, title, type = "text", value, placeholder, handleTextChange, otherStyles, ...props }) {
  const [showPassword, setShowPassword] = useState(false)
  
  return (
    <>
      <div className="relative mt-4">
        <label className="input input-bordered flex items-center gap-2 m-4">
          {title}
          <input
            name={name}
            type={(type === "password" && showPassword) ? "text" : type}
            value={value}
            className={`w-full text-cyan-700 text-sm ${otherStyles}`}
            placeholder={placeholder}
            onChange={handleTextChange}
            {...props}
          />
          {type === "password" && (
            <button type="button" onClick={() => setShowPassword(!showPassword)} className="focus:outline-none">
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </button>
          )}
        </label>
      </div>
    </>
  )
}

export default FormField