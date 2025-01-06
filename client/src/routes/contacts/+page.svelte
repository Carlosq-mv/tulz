<script>
  import {
    getMyContacts,
    getWhoHasRequestedMe,
    getRequestsSentFromMe,
    acceptContact,
    blockContact,
    removeContact,
    rejectContact
  } from '$lib/api/contact';
  import SadUser from '$lib/components/SadUser.svelte';
  import ConfirmModal from '$lib/components/ConfirmModal.svelte';

  let myContacts = $state([]);
  let requests = $state([]);
  let requestsSent = $state([]);
  let selected = $state(null);

  function formatDate(date) {
    const d = new Date(date);
    const formattedDate = d.toLocaleDateString('en-US');
    return formattedDate;
  }

  async function handleGettingMyContacts() {
    try {
      const res = await getMyContacts();
      myContacts = res;
      console.log(res);
    } catch (error) {
      console.log(error);
    }
  }

  async function handleGettingRequestsToMe() {
    try {
      const res = await getWhoHasRequestedMe();
      requests = res;
      console.log(res);
    } catch (error) {
      console.log(error);
    }
  }

  async function handleGettingRequestsISent() {
    try {
      const res = await getRequestsSentFromMe();
      requestsSent = res;
      console.log(res);
    } catch (error) {
      console.log(error);
    }
  }

  async function handleAcceptingContact(contactId) {
    try {
      const res = await acceptContact(contactId);

      handleGettingMyContacts();
      handleGettingRequestsToMe();
      console.log(res);
    } catch (error) {
      console.log(error);
    }
  }

  async function handleRejectingContact(contactId) {
    try {
      const res = await rejectContact(contactId);

      handleGettingRequestsToMe();
      console.log(res);
    } catch (error) {
      console.log(error);
    }
  }

  async function handleRemovingContact(contactId) {
    try {
      const res = await removeContact(contactId);

      handleGettingMyContacts();
    } catch (error) {
      console.log(error);
    }
  }

  async function handleBlockingContact(contactId) {
    try {
      const res = await blockContact(contactId);

      handleGettingMyContacts();
    } catch (error) {
      console.log(error);
    }
  }

  $effect(() => {
    handleGettingMyContacts();
    handleGettingRequestsToMe();
    handleGettingRequestsISent();
  });
</script>

<div>
  <div role="tablist" class="tabs tabs-lifted">
    <!-- My Contacts -->
    <input
      type="radio"
      name="my_tabs_2"
      role="tab"
      class="tab text-base"
      aria-label="Connections"
      checked="checked"
    />
    <div role="tabpanel" class="tab-content bg-base-100 border-base-300 rounded-box p-6">
      <span class="p-4 pb-6 font-black">Connections</span>
      {#if myContacts.length > 0}
        <div class="overflow-x-auto">
          <table class="table-zebra table">
            <thead>
              <tr>
                <th></th>
                <th>Name</th>
                <th>Username</th>
                <th>Date Added</th>
                <th>Options</th>
              </tr>
            </thead>

            <tbody>
              {#each myContacts as c, index}
                <tr class="text-lg">
                  <th>{index + 1}</th>
                  <td>{c.other_user.name}</td>
                  <td>{c.other_user.username}</td>
                  <td>{formatDate(c.last_updated)}</td>
                  <td>
                    <div class="dropdown">
                      <div tabindex="-1" role="button" class="btn btn-sm btn-info w-11">
                        <img src="icons/vertical-dots.svg" alt="check-mark" />
                      </div>
                      <ul
                        tabindex="-1"
                        class="dropdown-content menu bg-base-300 rounded-box z-[1] w-36 p-2 shadow"
                      >
                        <li>
                          <button
                            aria-label="block btn"
                            class="font-semibold"
                            onclick={() => {
                              selected = c.id;
                              modal_3.showModal();
                            }}
                          >
                            <img
                              src="icons/shield-alert.svg"
                              alt="shield alert"
                              class="bg-error rounded-md"
                            />
                            Block
                          </button>
                        </li>
                        <li>
                          <button
                            aria-label="remove btn"
                            class="font-semibold"
                            onclick={() => {
                              selected = c.id;
                              modal_4.showModal();
                            }}
                          >
                            <img
                              src="icons/trash.svg"
                              alt="trash can"
                              class="bg-error rounded-md"
                            />
                            Remove
                          </button>
                        </li>
                      </ul>
                    </div>
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {:else}
        <SadUser message={"No connections yet. Even the sad face is lonely... Let's fix that!"} />
      {/if}
    </div>

    <!-- Requests To Me -->
    <input
      type="radio"
      name="my_tabs_2"
      role="tab"
      class="tab text-base"
      aria-label="Requests Received"
    />
    <div role="tabpanel" class="tab-content bg-base-100 border-base-300 rounded-box p-6">
      <span class="p-4 pb-6 font-black">People Who Want to Connect</span>
      {#if requests.length > 0}
        <div class="overflow-x-auto">
          <table class="table-zebra table">
            <thead>
              <tr>
                <th></th>
                <th>Name</th>
                <th>Username</th>
                <th>Date Requested</th>
                <th>Accept</th>
                <th>Reject</th>
              </tr>
            </thead>

            <tbody>
              {#each requests as r, index}
                <tr class="text-lg">
                  <th>{index + 1}</th>
                  <td>{r.user_1.name}</td>
                  <td>{r.user_1.username}</td>
                  <td>{formatDate(r.last_updated)}</td>
                  <td>
                    <button
                      class="btn btn-sm btn-success"
                      onclick={() => {
                        selected = r.id;
                        modal_1.showModal();
                      }}
                    >
                      <img src="icons/check-mark.svg" alt="check-mark" />
                    </button>
                  </td>
                  <td>
                    <button
                      class="btn btn-sm btn-error"
                      onclick={() => {
                        selected = r.id;
                        modal_2.showModal();
                      }}
                    >
                      <img src="icons/cross.svg" alt="check-mark" />
                    </button>
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {:else}
        <SadUser message={'Nobody wants to connect with you at the moment.'} />
      {/if}
    </div>

    <!-- Requests Sent -->
    <input
      type="radio"
      name="my_tabs_2"
      role="tab"
      class="tab text-base"
      aria-label="Requests Sent"
    />
    <div role="tabpanel" class="tab-content bg-base-100 border-base-300 rounded-box p-6">
      <span class="p-4 pb-6 font-black">Requests You Sent</span>
      {#if requestsSent.length > 0}
        <div class="overflow-x-auto">
          <table class="table-zebra table">
            <thead>
              <tr>
                <th></th>
                <th>Name</th>
                <th>Username</th>
                <th>Date Requested</th>
              </tr>
            </thead>

            <tbody>
              {#each requestsSent as rs, index}
                <tr class="text-lg">
                  <th>{index + 1}</th>
                  <td>{rs.user_2.name}</td>
                  <td>{rs.user_2.username}</td>
                  <td>{formatDate(rs.last_updated)}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {:else}
        <SadUser
          message={'No requests sent? The sad face is still waiting... Maybe send a few hints?'}
        />
      {/if}
    </div>
  </div>
</div>

<ConfirmModal
  id={'modal_1'}
  title={'Say Yes to a New Connection?'}
  message={'Are you sure you want to add this user as a contact?'}
  buttonName={'Yes'}
  onConfirm={() => handleAcceptingContact(selected)}
/>
<ConfirmModal
  id={'modal_3'}
  title={'Block This Contact?'}
  message={'Are you sure you want to block this contact?'}
  buttonName={'Yes'}
  onConfirm={() => handleBlockingContact(selected)}
/>
<ConfirmModal
  id={'modal_4'}
  title={'Remove This Request?'}
  message={'Are you sure you want to remove this contact from your contacts list?'}
  buttonName={'Yes'}
  onConfirm={() => handleRemovingContact(selected)}
/>
<!-- should have different method for on confirm (handleRejectingContact) -->
<ConfirmModal
  id={'modal_2'}
  title={'Reject This Request?'}
  message={"Are you sure you want to reject this user's request to add you as a contact?"}
  buttonName={'Yes'}
  onConfirm={() => handleRejectingContact(selected)}
/>
