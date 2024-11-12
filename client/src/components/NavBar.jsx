import React from 'react'
import APP_NAME from "../constants/constants"

function NavBar() {
  return (
    <>
      <div className="navbar bg-neutral text-neutral-content">
        <div className="navbar-start">

          <div className="dropdown">
            <ul
              tabIndex={0}
              className="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow"
            >
              <li><a>Item 1</a></li>
              <li><a>Item 3</a></li>
            </ul>
          </div>

          <a className="btn btn-ghost text-xl">{APP_NAME}</a>
        </div>

        <div className="navbar-center hidden lg:flex">
          <ul className="menu menu-horizontal px-1">
            <li><a>Item 1</a></li>
            <li><a>Item 3</a></li>
          </ul>
        </div>

        <div className="navbar-end">
          <a className="btn">Button</a>
        </div>

      </div>
    </>
  )
}

export default NavBar