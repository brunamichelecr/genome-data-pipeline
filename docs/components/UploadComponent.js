export default function UploadComponent() {
  const container = document.createElement('div');
  const button = document.createElement('button');
  button.textContent = 'Enviar Genoma';
  button.id = 'upload-btn';
  container.appendChild(button);
  return container;
}