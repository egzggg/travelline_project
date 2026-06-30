function updatePreview() {
  const heading = document.getElementById("heading");
  const text = document.getElementById("text");
  const link = document.getElementById("link");

  const previewHeading = document.querySelectorAll("#preview-heading");
  const previewText = document.querySelectorAll("#preview-text");

  if (heading) {
    previewHeading.forEach((item) => {
      item.innerText = heading.value || "Заголовок";
    });
  }

  if (text) {
    previewText.forEach((item) => {
      item.innerText = text.value || "Текст";
    });
  }

  const previewLink = document.getElementById("preview-link");

  if (link && previewLink) {
    previewLink.href = link.value;
    previewLink.innerText = link.value;
  }
}

function previewImage(event) {
  const image = document.getElementById("preview-image");
  const file = event.target.files[0];

  if (file && image) {
    image.src = URL.createObjectURL(file);
    image.style.display = "block";
  }
}
