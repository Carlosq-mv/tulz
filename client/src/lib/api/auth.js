export async function login(loginData) {
  try {
    const res = await fetch('http://localhost:8000/user/login', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(loginData)
    });

    // check for non-200 status codes
    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || 'Failed to login up.');
    }

    // parse and return the response JSON
    return await res.json();
  } catch (error) {
    throw error;
  }
}

export async function signup(sigupData) {
  try {
    const res = await fetch('http://localhost:8000/user/create-account', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(sigupData)
    });

    // check for non-200 status codes
    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || 'Failed to sign up.');
    }

    // parse and return the response JSON
    return await res.json();
  } catch (error) {
    throw error;
  }
}
