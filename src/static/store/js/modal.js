const changeModal = document.getElementById('emailNotificationModal');
if (changeModal) {
  changeModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    const recipient = button.getAttribute('data-bs-config');
    const data = JSON.parse(recipient);

    const robot = document.getElementById('robot_id');
    robot.value = data.product_pk;
  });
}