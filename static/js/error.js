fetch("https://naas.isalman.dev/no")
.then(r => r.json())
.then(d => new Promise(resolve => setTimeout(() => resolve(d), 1000)))
.then(d => {
    document.getElementById("reason").textContent = d.reason;
});