const samples = {
  fake: "Donald Trump just couldn’t wish all Americans a Happy New Year and leave it at that. Instead, he had to give a shout out to his enemies, haters and the very dishonest fake news media.",
  real: "WASHINGTON (Reuters) - The head of a conservative Republican faction in the U.S. Congress called himself a fiscal conservative on Sunday and urged budget restraint in 2018."
};

document.querySelectorAll("[data-sample]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelector("#article").value = samples[button.dataset.sample];
  });
});
