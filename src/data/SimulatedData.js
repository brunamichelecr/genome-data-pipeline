// src/data/SimulatedData.js
// Estes dados simulam a lista 'doencas' que era passada para o template Jinja.

export const simulatedDiseases = [
  { 
    id: 1, 
    name: "Doença de Alzheimer", 
    brief: "Risco genético para o desenvolvimento precoce ou tardio.", 
    desc: "A Doença de Alzheimer é uma condição neurodegenerativa. Os achados genéticos aqui apontam para variações nos genes APOE4, que estão associados a um risco elevado.", 
    percent: 85 
  },
  { 
    id: 2, 
    name: "Intolerância à Lactose", 
    brief: "Predisposição para dificuldade na digestão de laticínios na vida adulta.", 
    desc: "Variações no gene LCT que resultam na diminuição da produção de lactase após a infância. Risco muito alto.", 
    percent: 95 
  },
  { 
    id: 3, 
    name: "Doença de Parkinson", 
    brief: "Associação com genes como LRRK2 e SNCA. Necessita acompanhamento.", 
    desc: "A associação genética neste perfil é moderada. Foco em tremores, rigidez e desequilíbrio, que são sintomas clássicos da condição.", 
    percent: 45 
  },
  { 
    id: 4, 
    name: "Deficiência de Vitamina D", 
    brief: "Variações genéticas que afetam a absorção e metabolismo da vitamina D.", 
    desc: "Pode levar a problemas ósseos e imunológicos. Recomendado monitoramento dos níveis de Vitamina D e suplementação, se necessário.", 
    percent: 70 
  },
  { 
    id: 5, 
    name: "Câncer de Mama", 
    brief: "Risco baixo a moderado para formas hereditárias da doença (genes BRCA1/BRCA2).", 
    desc: "Embora haja associações, o risco geral não é considerado alto, mas o acompanhamento médico é sempre recomendado.", 
    percent: 30 
  },
];