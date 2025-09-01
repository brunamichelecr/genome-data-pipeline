document.getElementById('cadastro-form').addEventListener('submit', async function (e) {
  e.preventDefault();

  const nome = document.getElementById('nome').value.trim();
  const genero = document.getElementById('genero').value;
  const email = document.getElementById('email').value.trim();
  const senha = document.getElementById('senha').value;
  const confirmar = document.getElementById('confirmar-senha').value;
  const termos = document.getElementById('termos').checked;

  const senhaValida = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

  // Validações básicas
  if (!nome || !genero || !email || !senha || !confirmar) {
    mostrarMensagem('Todos os campos são obrigatórios.');
    return;
  }

  if (!termos) {
    mostrarMensagem('Você precisa concordar com os termos de uso e política de privacidade.');
    return;
  }

  if (!senhaValida.test(senha)) {
    mostrarMensagem('A senha deve conter pelo menos 8 caracteres, incluindo letras e números.');
    return;
  }

  if (senha !== confirmar) {
    mostrarMensagem('As senhas não coincidem.');
    return;
  }

  // Verificação de e-mail duplicado
  try {
    const verificar = await fetch(`http://localhost:5000/api/verificar-email?email=${encodeURIComponent(email)}`);
    const resultadoVerificacao = await verificar.json();

    if (resultadoVerificacao.existe) {
      mostrarMensagem('Este e-mail já está cadastrado. Por favor, use outro.', 'warning');
      return;
    }
  } catch (erro) {
    console.error('Erro ao verificar e-mail:', erro);
    mostrarMensagem('Erro ao verificar e-mail. Tente novamente mais tarde.');
    return;
  }

  // Envio para o backend
  try {
    const resposta = await fetch('http://localhost:5000/api/cadastro', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nome, genero, email, senha })
    });

    const resultado = await resposta.json();

    if (resposta.ok) {
      mostrarMensagem(resultado.mensagem, 'success');
      document.getElementById('cadastro-form').reset();
    } else {
      mostrarMensagem(resultado.erro || resultado.mensagem);
    }
  } catch (erro) {
    console.error('Erro ao enviar dados:', erro);
    mostrarMensagem('Erro ao conectar com o servidor. Tente novamente mais tarde.');
  }
});

// Função para exibir mensagens estilizadas
function mostrarMensagem(texto, tipo = 'danger') {
  const msg = document.getElementById('mensagem-feedback');
  msg.textContent = texto;
  msg.className = `alert alert-${tipo}`;
  msg.classList.remove('d-none');
}
document.querySelector('.cookie-banner .btn').addEventListener('click', function () {
  document.querySelector('.cookie-banner').style.display = 'none';
});