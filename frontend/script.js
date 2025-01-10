document.getElementById("convert-btn").addEventListener("click", async () => {
    const inputText = document.getElementById("input").value;
    const response = await fetch("http://localhost:8080/convert", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input_text: inputText })
    });
    const data = await response.json();
    document.getElementById("output").innerText = data.output_text;
});
