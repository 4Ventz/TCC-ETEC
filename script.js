const inputOriginal = document.getElementById("Original");
const traduzido = document.getElementById("Traduzido");

inputOriginal.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        enviarCodigo();
    }
});

const OPENAI_API_KEY = "";

function enviarCodigo() {
    var eCodigo = inputOriginal.value;

    fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: "Bearer " + OPENAI_API_KEY,
        },
        body: JSON.stringify({
            model: "gpt-3.5-turbo",
            messages: [{ role: "user", content: eCodigo }],
        }),
    })
        .then((response) => response.json())
        .then((json) => {
            if (traduzido.value) traduzido.value += "\n";

            if (json.error?.message) {
                traduzido.value += `Error: ${json.error.message}`;
            } else if (json.choices?.[0].message?.content) {
                var text = json.choices[0].message.content || "Sem resposta";

                traduzido.value += text;
            }

            traduzido.scrollTop = traduzido.scrollHeight;
        })
        .catch((error) => console.error("Erro:", error))
        .finally(() => {
            inputOriginal.value = "";
            inputOriginal.disabled = false;
            inputOriginal.focus();
        });

    if (traduzido.value) traduzido.value += "\n\n\n";

    traduzido.value += `Eu: ${eCodigo}`;
    inputOriginal.value = "Carregando...";
    inputOriginal.disabled = true;
}
