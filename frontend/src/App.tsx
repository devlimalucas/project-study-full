import { useEffect, useState } from "react";

interface Produto {
  Produto: string;
  Quantidade: number;
  Receita: number;
}

function App() {
  const [produtos, setProdutos] = useState<Produto[]>([]);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/produtos`)
      .then(res => res.json())
      .then(data => setProdutos(data))
      .catch(err => console.error("Erro ao buscar produtos:", err));
  }, []);  

  return (
    <div>
      <h1>Lista de Produtos</h1>
      <ul>
        {produtos.map((p, i) => (
          <li key={i}>
            {p.Produto} - {p.Quantidade} unidades - R$ {p.Receita}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
