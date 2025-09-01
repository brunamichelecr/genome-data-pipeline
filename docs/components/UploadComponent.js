export default function UploadComponent() {
  // Cria o container principal do componente
  const container = document.createElement('div');

  // Cria o botão de upload
  const button = document.createElement('button');
  button.textContent = 'Enviar Genoma'; // Texto exibido no botão
  button.id = 'upload-btn';             // ID para facilitar seleção/manipulação no DOM

  // Adiciona o botão dentro do container
  container.appendChild(button);

  // Retorna o componente pronto para ser inserido no DOM
  return container;
}
