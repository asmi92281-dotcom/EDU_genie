const endpoints = {
  qa: "/qa",
  explain: "/explain",
  quiz: "/quiz",
  summarize: "/summarize",
  learn: "/learn/recommendations",
};

const task = document.getElementById("task");
const input = document.getElementById("inputText");
const submit = document.getElementById("submitBtn");
const clear = document.getElementById("clearBtn");
const status = document.getElementById("status");
const resultCard = document.getElementById("resultCard");
const result = document.getElementById("result");
const copyBtn = document.getElementById("copyBtn");

const placeholders = {
  qa: "Example: Which is the largest ocean?",
  explain: "Example: Explain the Pythagoras theorem simply.",
  quiz: "Paste a topic or passage to create 3 MCQs.",
  summarize: "Paste a long educational passage to summarize.",
  learn: "Example: SQL",
};

task.addEventListener("change", () => { input.placeholder = placeholders[task.value]; });
clear.addEventListener("click", () => { input.value = ""; result.innerHTML = ""; resultCard.classList.add("hidden"); status.textContent = ""; });
copyBtn.addEventListener("click", async () => {
  await navigator.clipboard.writeText(result.innerText);
  status.textContent = "Copied to clipboard.";
});

function renderQuiz(data) {
  return data.questions.map((q, i) => `
    <article class="quiz-question">
      <h3>${i + 1}. ${escapeHtml(q.question)}</h3>
      ${q.options.map((o, j) => `<div class="option">${String.fromCharCode(65+j)}. ${escapeHtml(o)}</div>`).join("")}
      <p class="correct">Answer: ${escapeHtml(q.correct_answer)}</p>
      ${q.explanation ? `<p>${escapeHtml(q.explanation)}</p>` : ""}
    </article>`).join("");
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[c]));
}

submit.addEventListener("click", async () => {
  const text = input.value.trim();
  if (!text) { status.textContent = "Please enter some text first."; return; }
  submit.disabled = true;
  status.textContent = "Generating...";
  resultCard.classList.remove("hidden");
  result.textContent = "";
  try {
    const response = await fetch(endpoints[task.value], {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Request failed.");
    result.innerHTML = task.value === "quiz" ? renderQuiz(data) : escapeHtml(data.result || "No result returned.");
    status.textContent = "Done.";
  } catch (error) {
    result.innerHTML = `<p class="error">${escapeHtml(error.message)}</p>`;
    status.textContent = "Something went wrong.";
  } finally {
    submit.disabled = false;
  }
});
