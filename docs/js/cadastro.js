document.getElementById('cadastro-form').addEventListener('submit', async function (e) {
  e.preventDefault();

  const nome = document.getElementById('nome').value.trim();
  const genero = document.getElementById('genero').value;
  const email = document.getElementById('email').value.trim();
  const senha = document.getElementById('senha').value;
  const confirmar = document.getElementById('confirmar-senha').value;
  const termos = document.getElementById('termos').checked;

  const senhaValida = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

  // Validações
  if (!termos) {
    alert('Você precisa concordar com os termos de uso e política de privacidade.');
    return;
  }

  if (!senhaValida.test(senha)) {
    alert('A senha deve conter pelo menos 8 caracteres, incluindo letras e números.');
    return;
  }

  if (senha !== confirmar) {
    alert('As senhas não coincidem.');
    return;
  }

  if (!nome || !genero || !email || !senha) {
    alert('Todos os campos são obrigatórios.');
    return;
  }

  // Envio para o backend Python
  try {
    const resposta = await fetch('http://localhost:5000/api/cadastro', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nome, genero, email, senha })
    });

    const resultado = await resposta.json();

    if (resposta.ok) {
      alert(resultado.mensagem);
      document.getElementById('cadastro-form').reset();
    } else {
      alert(resultado.erro || resultado.mensagem);
    }
  } catch (erro) {
    console.error('Erro ao enviar dados:', erro);
    alert('Erro ao conectar com o servidor. Tente novamente mais tarde.');
  }
});

document.querySelector('.cookie-banner .btn').addEventListener('click', function () {
  document.querySelector('.cookie-banner').style.display = 'none';
});