import React from 'react'

function FormField({ name, title, type = "text", value, placeholder, handleTextChange, otherStyles, ...props }) {
  return (
    <>
      <label className="input input-bordered flex items-center gap-2 m-4">
        {title}
        <input 
          name={name}
          type={type} 
          value={value} 
          className={`w-full text-cyan-700 text-sm ${otherStyles}`}
          placeholder={placeholder}
          onChange={handleTextChange} 
          {...props}
        />
      </label>
    </>
  )
}

export default FormField