document.addEventListener('DOMContentLoaded', () => {
  const cardsContainer = document.getElementById('cardsContainer');

  function criarCard(titulo, conteudo) {
    const card = document.createElement('div');
    card.className = 'card';
    const h2 = document.createElement('h2');
    h2.textContent = titulo;
    card.appendChild(h2);

    if (typeof conteudo === 'string') {
      const p = document.createElement('div');
      p.innerHTML = conteudo;
      card.appendChild(p);
    } else if (conteudo instanceof HTMLElement) {
      card.appendChild(conteudo);
    }

    return card;
  }

  async function carregarAnalise() {
    cardsContainer.innerHTML = '<p>Carregando...</p>';
    try {
      const response = await fetch('http://localhost:5000/analisar');
      const data = await response.json();
      cardsContainer.innerHTML = ''; // limpa "Carregando"

      // --- STATUS ---
      const statusDiv = document.createElement('div');
      statusDiv.className = 'status';
      statusDiv.style.backgroundColor = data.status === 'sucesso' ? '#28a745' : '#dc3545';
      statusDiv.textContent = `Status: ${data.status.toUpperCase()}`;
      cardsContainer.appendChild(criarCard('🔔 Status da Análise', statusDiv));

      // --- RESULTADO AI (cortado no "Entrada:") ---
      let output = data.output || '';
      const corte = output.indexOf('Entrada:');
      if (corte !== -1) output = output.substring(0, corte).trim();
      cardsContainer.appendChild(criarCard('📌 Resultado da AI', `<pre>${output}</pre>`));

      // --- SEÇÃO EXCLUSIVA DE EMAILS ---
      const emailsContainer = document.createElement('div');
      emailsContainer.style.display = 'flex';
      emailsContainer.style.flexDirection = 'column';
      emailsContainer.style.gap = '10px';
      emailsContainer.style.marginTop = '10px';

      const emailContagemMap = new Map();

      const emailBlocksRegex = /- ([\d\.]+) → (\d+) ocorrência(?:s)?\n([\s\S]*?)(?=\n- [\d\.]+ →|\n✅ IPs sem dados sensíveis:|$)/g;
      let match;
      while ((match = emailBlocksRegex.exec(output)) !== null) {
        const ip = match[1];
        const detalhes = match[3].trim();

        const emailRegex = /- ([\w\.\-]+@[\w\.\-]+) →\n([\s\S]*?)(?=\n   - [\w\.\-]+@|$)/g;
        let emailMatch;
        while ((emailMatch = emailRegex.exec(detalhes)) !== null) {
          const email = emailMatch[1];
          const info = emailMatch[2].trim();

          // Só conta se houver algum dado sensível
          if (!info.includes('Nenhum dado sensível detectado')) {
            const ocorrencias = (info.match(/\n/g) || []).length + 1;
            emailContagemMap.set(email, (emailContagemMap.get(email) || 0) + ocorrencias);
          }

          const emailCard = document.createElement('div');
          emailCard.className = 'card';
          emailCard.innerHTML = `
            <h2>📧 ${email} (IP: ${ip})</h2>
            <pre>${info}</pre>
          `;
          emailsContainer.appendChild(emailCard);
        }
      }

      const emailsSectionCard = criarCard('📨 Emails Vazados', emailsContainer);
      cardsContainer.appendChild(emailsSectionCard);

      // --- CARD ÚNICO DE GRÁFICOS ---
      const graficoContainer = document.createElement('div');
      graficoContainer.style.display = 'flex';
      graficoContainer.style.flexDirection = 'column';
      graficoContainer.style.gap = '20px';

      // Div pizza: tipos de vazamento
      const graficoPizzaDiv = document.createElement('div');
      graficoPizzaDiv.style.width = '100%';
      graficoPizzaDiv.style.height = '300px';
      graficoPizzaDiv.id = 'graficoTiposPizza';
      graficoContainer.appendChild(graficoPizzaDiv);

      // Div barras: quantidade de vazamentos por email
      const graficoBarrasDiv = document.createElement('div');
      graficoBarrasDiv.style.width = '100%';
      graficoBarrasDiv.style.height = '300px';
      graficoBarrasDiv.id = 'graficoEmailsBarras';
      graficoContainer.appendChild(graficoBarrasDiv);

      cardsContainer.appendChild(criarCard('📊 Gráficos de Vazamentos', graficoContainer));

      // --- PROCESSA OS GRÁFICOS ---
      const tiposMatch = output.match(/🔎 Tipos de vazamento detectados:\n([\s\S]*?)(?=\n\n|$)/);
      let tipos = [];
      let quantidades = [];
      if (tiposMatch) {
        const tiposTexto = tiposMatch[1].trim();
        const linhas = tiposTexto.split('\n');
        linhas.forEach(linha => {
          const m = linha.match(/- (.+) → (\d+) pacote/);
          if (m) {
            tipos.push(m[1]);
            quantidades.push(parseInt(m[2]));
          }
        });
      }

      google.charts.load('current', { packages: ['corechart', 'bar'] });
      google.charts.setOnLoadCallback(() => {
        // --- Pizza ---
        const dataTablePizza = new google.visualization.DataTable();
        dataTablePizza.addColumn('string', 'Tipo');
        dataTablePizza.addColumn('number', 'Quantidade');
        for (let i = 0; i < tipos.length; i++) {
          dataTablePizza.addRow([tipos[i], quantidades[i]]);
        }
        const optionsPizza = {
          pieHole: 0.4,
          backgroundColor: '#2c2c2c',
          legend: { textStyle: { color: '#f0f0f0' } },
          slices: tipos.map((_, i) => ({ color: ['#f39c12', '#e74c3c', '#3498db', '#9b59b6'][i % 4] }))
        };
        const chartPizza = new google.visualization.PieChart(graficoPizzaDiv);
        chartPizza.draw(dataTablePizza, optionsPizza);

        // --- Barras ---
        const dataTableBarras = new google.visualization.DataTable();
        dataTableBarras.addColumn('string', 'Email');
        dataTableBarras.addColumn('number', 'Ocorrências');
        for (const [email, qtd] of emailContagemMap.entries()) {
          dataTableBarras.addRow([email, qtd]);
        }
        const optionsBarras = {
          legend: { position: 'none' },
          colors: ['#f39c12'],
          backgroundColor: '#2c2c2c',
          hAxis: { textStyle: { color: '#f0f0f0' } },
          vAxis: { textStyle: { color: '#f0f0f0' } },
        };
        const chartBarras = new google.visualization.ColumnChart(graficoBarrasDiv);
        chartBarras.draw(dataTableBarras, optionsBarras);
      });

    } catch (err) {
      cardsContainer.innerHTML = `<p>Erro ao carregar a análise: ${err}</p>`;
      console.error(err);
    }
  }

  carregarAnalise();
});
