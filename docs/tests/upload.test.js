import { screen, render } from '@testing-library/dom';
import '@testing-library/jest-dom';
import UploadComponent from '../components/UploadComponent.js';

test('botão de upload aparece com texto correto', () => {
  document.body.innerHTML = '';
  document.body.appendChild(UploadComponent());

  const botao = screen.getByText('Enviar Genoma');
  expect(botao).toBeInTheDocument();
  expect(botao).toHaveAttribute('id', 'upload-btn');
});
