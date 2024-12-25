<script>
  let { message, type } = $props();
</script>

<div role="alert" class={`alert mt-6 ${type?.style}`}>
  <div class="flex h-6 w-6 shrink-0 items-center stroke-current">
    <img src={type?.icon} alt="icon" />
  </div>
  <span class="text-center">{message}</span>
</div>
