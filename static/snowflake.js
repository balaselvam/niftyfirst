function random(num) {
  return Math.floor(Math.random() * num);
}

const snowflakesContainer = document.getElementById("snowflakes-container");

for (let i = 0; i < 50; i++) {
  const snowflake = document.createElement("div");
  snowflake.className = "snowflake";
  snowflake.style.setProperty("--left", `${random(100)}vw`);
  snowflake.style.setProperty("--left-ini", `${random(20) - 10}vw`);
  snowflake.style.setProperty("--left-end", `${random(20) - 10}vw`);
  snowflake.style.setProperty("--speed", `${10 + random(100)}s`);
  snowflake.style.setProperty("--size", `${random(5) * 0.07}vw`);
  snowflake.style.setProperty("--delay", `-${random(15)}s`);
  snowflakesContainer.appendChild(snowflake);
}
