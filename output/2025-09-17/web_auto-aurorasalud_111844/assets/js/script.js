// script.js — utilidades mínimas
(function(){
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  const form = document.getElementById('contact-form');
  const msg = document.getElementById('form-msg');
  if (form && msg) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const ok = form.checkValidity();
      msg.textContent = ok ? '¡Gracias! Te responderemos pronto.' : 'Revisá los campos obligatorios.';
    });
  }
})();
