document.getElementById("emailForm").addEventListener("submit", async (e) => { 
    e.preventDefault(); 
    const emailData = { 
        from: document.getElementById("from").value, 
        to: document.getElementById("to").value, 
        message: document.getElementById("message").value 
    }; 
    
    await fetch("http://localhost:5000/send", { 
        method: "POST", 
        headers: { "Content-Type": "application/json" }, 
        body: JSON.stringify(emailData) 
    }); 
    alert("Email enviado!"); 
}); 