// Listener para o evento de submit do formulário de cadastro
document.getElementById('cadastro-form').addEventListener('submit', async function (e) {
  e.preventDefault(); // Evita recarregar a página

  // Captura dos valores do formulário
  const nome = document.getElementById('nome').value.trim();
  const genero = document.getElementById('genero').value;
  const email = document.getElementById('email').value.trim();
  const senha = document.getElementById('senha').value;
  const confirmar = document.getElementById('confirmar-senha').value;
  const termos = document.getElementById('termos').checked;

  // Regex para validar senha (mínimo 8 caracteres, pelo menos 1 letra e 1 número)
  const senhaValida = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

  // ----------------------------
  // Validações básicas (Frontend)
  // ----------------------------
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

  // ----------------------------
  // Verificação de e-mail duplicado no backend
  // ----------------------------
  try {
    // CORRETO: Caminho relativo
    const verificar = await fetch(`/api/verificar-email?email=${encodeURIComponent(email)}`);
    
    // MELHORIA: Garante que o servidor retornou 200/201 antes de ler o JSON
    if (!verificar.ok) {
        // Se o servidor deu 4xx ou 5xx, trata como erro de API
        throw new Error(`Erro do servidor na verificação: ${verificar.status}`);
    }

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

  // ----------------------------
  // Envio dos dados para o backend (cadastro)
  // ----------------------------
  try {
    // ✅ CORREÇÃO FINAL: Usando caminho relativo para o POST
    const resposta = await fetch('/api/cadastro', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nome, genero, email, senha })
    });

    // MELHORIA: Lemos o JSON somente se a resposta foi bem-sucedida ou se queremos ler o erro JSON
    const resultado = await resposta.json(); 

    if (resposta.ok) {
      mostrarMensagem(resultado.mensagem || 'Cadastro realizado com sucesso!', 'success');

      // Redireciona o usuário para a página de login após 1.5s
      setTimeout(() => {
        window.location.href = '/login';
      }, 1500);
    } else {
      // Trata erros retornados pelo Flask (ex: 'E-mail já cadastrado')
      mostrarMensagem(resultado.erro || resultado.mensagem);
    }
  } catch (erro) {
    console.error('Erro ao enviar dados:', erro);
    mostrarMensagem('Erro ao conectar com o servidor. Tente novamente mais tarde.');
  }
});

// ----------------------------
// Função utilitária para exibir mensagens no frontend
// ----------------------------
function mostrarMensagem(texto, tipo = 'danger') {
  const msg = document.getElementById('mensagem-feedback');
  // Se o elemento não existir, loga um erro e sai para não travar
  if (!msg) {
    console.error("Elemento com id 'mensagem-feedback' não encontrado no HTML.");
    return;
  }
  msg.textContent = texto;
  msg.className = `alert alert-${tipo}`; // Usa classes do Bootstrap (danger, success, warning)
  msg.classList.remove('d-none'); // Torna o alerta visível
}

// ----------------------------
// Banner de cookies (UX)
// ----------------------------
document.querySelector('.cookie-banner .btn').addEventListener('click', function () {
  document.querySelector('.cookie-banner').style.display = 'none';
});