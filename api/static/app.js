function go(){
fetch("/predict",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
valor:+valor.value,
prazo:+prazo.value,
desconto:+desconto.value,
relacionamento:+relacionamento.value,
historico:+historico.value
})
})
.then(r=>r.json())
.then(d=>{
resultado.innerHTML = "Probabilidade de Aprovação: " + d.probabilidade;
});
}
