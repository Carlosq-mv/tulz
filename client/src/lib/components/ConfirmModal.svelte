<script>
  let { id, title, message, buttonName, onConfirm } = $props()
</script>

<dialog id={id} class="modal">
  <div class="modal-box">
    <h3 class="text-lg font-bold">{title}</h3>
    <p class="py-4">{message}</p>
    <div class="modal-action">
      <form method="dialog" class="flex gap-8">
        <button class="btn btn-sm btn-error">Cancel</button>
        <button class="btn btn-sm btn-warning" onclick={onConfirm}>{buttonName}</button>
      </form>
    </div>
  </div>
</dialog>