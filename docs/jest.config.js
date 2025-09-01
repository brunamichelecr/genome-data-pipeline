export default {
  // Ambiente de teste que simula um DOM (necessário para testes de componentes que manipulam o HTML)
  testEnvironment: 'jsdom',

  // Transformação de arquivos JS usando Babel
  transform: {
    "^.+\\.js$": "babel-jest"  // Todo arquivo .js será processado pelo Babel antes do teste
  }
};
