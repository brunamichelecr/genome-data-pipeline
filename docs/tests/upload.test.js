// Importa funções do Testing Library e matchers do jest-dom
import { screen, render } from '@testing-library/dom';
import '@testing-library/jest-dom';
import UploadComponent from '../components/UploadComponent.js';

// Teste unitário para o UploadComponent
test('botão de upload aparece com texto correto', () => {
  // Limpa o body antes de adicionar o componente
  document.body.innerHTML = '';

  // Adiciona o componente UploadComponent no DOM
  document.body.appendChild(UploadComponent());

  // Busca o botão pelo texto exibido
  const botao = screen.getByText('Enviar Genoma');

  // Verifica se o botão está presente no DOM
  expect(botao).toBeInTheDocument();

  // Verifica se o botão possui o ID correto
  expect(botao).toHaveAttribute('id', 'upload-btn');
});
