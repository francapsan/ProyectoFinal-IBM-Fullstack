// Interactive enhancements for dealerships app
document.addEventListener('DOMContentLoaded', function () {
  // Dynamic Car Model Filter based on Car Make selection
  const makeSelect = document.getElementById('car_make');
  const modelSelect = document.getElementById('car_model');

  if (makeSelect && modelSelect) {
    makeSelect.addEventListener('change', function () {
      const selectedMake = this.value;
      const options = modelSelect.querySelectorAll('option');

      options.forEach(opt => {
        if (!opt.value) return; // Keep "Seleccionar Modelo" default
        const optMake = opt.getAttribute('data-make');
        if (!selectedMake || optMake === selectedMake) {
          opt.style.display = 'block';
        } else {
          opt.style.display = 'none';
        }
      });

      // Reset selection if hidden
      const currentSelected = modelSelect.options[modelSelect.selectedIndex];
      if (currentSelected && currentSelected.style.display === 'none') {
        modelSelect.value = '';
      }
    });
  }

  // Auto-dismiss alerts after 6 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 6000);
  });
});
