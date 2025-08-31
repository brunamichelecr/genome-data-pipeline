// js/cadastro.js

document.getElementById('cadastro-form').addEventListener('submit', function (e) {
  const senha = document.getElementById('senha').value;
  const confirmar = document.getElementById('confirmar-senha').value;
  const termos = document.getElementById('termos').checked;
  const senhaValida = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

  if (!termos) {
    e.preventDefault();
    alert('Você precisa concordar com os termos de uso e política de privacidade.');
    return;
  }

  if (!senhaValida.test(senha)) {
    e.preventDefault();
    alert('A senha deve conter pelo menos 8 caracteres, incluindo letras e números.');
    return;
  }

  if (senha !== confirmar) {
    e.preventDefault();
    alert('As senhas não coincidem.');
    return;
  }
});

document.querySelector('.cookie-banner .btn').addEventListener('click', function () {
  document.querySelector('.cookie-banner').style.display = 'none';
});