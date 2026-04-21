const BOUNDS = {
    valor:          [300,  8000],
    prazo:          [7,    60],
    desconto:       [0,    20],
    relacionamento: [1,    5],
    historico:      [0,    20],
};

const LABELS = {
    valor:          "Valor (R$ 300–8.000)",
    prazo:          "Prazo (7–60 dias)",
    desconto:       "Desconto (0–20%)",
    relacionamento: "Relacionamento (1–5)",
    historico:      "Histórico de compras (0–20)",
};

const STATUS_CLASS = {
    "Alta chance":  "alta",
    "Risco":        "risco",
    "Baixa chance": "baixa",
};

function validate(fields) {
    const errors = [];
    for (const [key, [min, max]] of Object.entries(BOUNDS)) {
        const v = fields[key];
        if (v === "" || isNaN(v)) {
            errors.push(`${LABELS[key]}: valor inválido`);
        } else if (v < min || v > max) {
            errors.push(`${LABELS[key]}: deve estar entre ${min} e ${max}`);
        }
    }
    return errors;
}

function go() {
    const fields = {
        valor:          +document.getElementById("valor").value,
        prazo:          +document.getElementById("prazo").value,
        desconto:       +document.getElementById("desconto").value,
        relacionamento: +document.getElementById("relacionamento").value,
        historico:      +document.getElementById("historico").value,
    };

    const resultado = document.getElementById("resultado");
    const errors = validate(fields);

    if (errors.length) {
        resultado.className = "result erro";
        resultado.innerHTML = errors.join("<br>");
        return;
    }

    resultado.className = "result";
    resultado.textContent = "Calculando...";

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(fields),
    })
    .then(r => r.json())
    .then(d => {
        if (d.erro) {
            resultado.className = "result erro";
            resultado.textContent = Array.isArray(d.erro) ? d.erro.join(" | ") : d.erro;
            return;
        }
        const pct = (d.probabilidade * 100).toFixed(1);
        resultado.className = `result ${STATUS_CLASS[d.status] || ""}`;
        resultado.innerHTML = `${d.status}<br><span class="prob">${pct}% de aprovação</span>`;
    })
    .catch(() => {
        resultado.className = "result erro";
        resultado.textContent = "Erro ao conectar com o servidor.";
    });
}
