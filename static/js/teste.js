// const emailInput = document.getElementById("email_recuperacao");
// const form = document.getElementById("formCadastro");
//
// form.addEventListener("submit", async (e) => {
//     e.preventDefault();
//
//     const email = emailInput.value;
//
//     // Verifica se o email já existe
//     const response = await fetch("/verificar-email", {
//         method: "POST",
//         headers: {"Content-Type": "application/json"},
//         body: JSON.stringify({email_recuperacao: email})
//     });
//     const data = await response.json();
//
//     if(data.existe){
//         alert("Este email já está cadastrado!");
//         return; // impede o envio do formulário
//     }
//
//     // Se não existe, envia o formulário normalmente
//     form.submit();
// });