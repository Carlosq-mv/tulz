export async function addContact(contact) {
  try {
    const res = await fetch('http://localhost:8000/contact/add-contact', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(contact)
    })

    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Failed to get my contacts.')
    }
    return await res.json()
  } catch (error) {
    throw error
  }
}

export async function getMyContacts() {
  try {
    const res = await fetch('http://localhost:8000/contact/my-contacts', {
      method: 'GET',
      credentials: 'include'
    })

    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Failed to get my contacts.')
    }
    return await res.json()
  } catch (error) {
    throw error
  }
}


export async function getWhoHasRequestedMe() {
  try {
    const res = await fetch('http://localhost:8000/contact/requests-to-me', {
      method: 'GET',
      credentials: 'include'
    })

    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Failed to get my contacts.')
    }
    return await res.json()
  } catch (error) {
    throw error
  }
}

export async function getRequestsSentFromMe() {
  try {
    const res = await fetch('http://localhost:8000/contact/requests-sent', {
      method: 'GET',
      credentials: 'include'
    })

    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Failed to get my contacts.')
    }
    return await res.json()
  } catch (error) {
    throw error
  }
}

export async function acceptContact(contactId) {
  try {
    const res = await fetch(`http://localhost:8000/contact/accept-contact/${contactId}`, {
      method: 'PUT',
      credentials: 'include'
    })

    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Failed to get my contacts.')
    }
    return await res.json()
  } catch (error) {
    throw error
  }
}

export async function rejectContact(contactId) {
  try {
    const res = await fetch(`http://localhost:8000/contact/reject-contact/${contactId}`, {
      method: 'PUT',
      credentials: 'include'
    })

    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Failed to get my contacts.')
    }
    return await res.json()
  } catch (error) {
    throw error
  }
}

export async function blockContact(contactId) {
  try {
    const res = await fetch(`http://localhost:8000/contact/block-contact/${contactId}`, {
      method: 'PUT',
      credentials: 'include'
    })

    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Failed to get my contacts.')
    }
    return await res.json()
  } catch (error) {
    throw error
  }
}

export async function removeContact(contactId) {
  try {
    const res = await fetch(`http://localhost:8000/contact/remove-contact/${contactId}`, {
      method: 'PUT',
      credentials: 'include'
    })

    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Failed to get my contacts.')
    }
    return await res.json()
  } catch (error) {
    throw error
  }
}