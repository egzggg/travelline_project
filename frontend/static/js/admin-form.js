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

document.addEventListener("DOMContentLoaded", function () {
  const typeSelect = document.querySelector('select[name="element_type"]');
  const headingInput = document.getElementById("heading");
  const form = document.querySelector('form');

  function toggleFieldsForType() {
    if (!typeSelect || !form) return;

    const keepNames = ['element_type', 'position', 'text'];
    const fieldBlocks = form.querySelectorAll('.mb-3');
    const headingInput = document.getElementById('heading');

    fieldBlocks.forEach((block) => {
      const control = block.querySelector('input[name], textarea[name], select[name]');
      if (!control) return;
      const name = control.getAttribute('name');

      if (typeSelect.value === 'button') {
        if (!keepNames.includes(name)) {
          block.style.display = 'none';
        } else {
          block.style.display = '';
        }
      } else {
        block.style.display = '';
      }
    });

    if (typeSelect.value === 'button') {
      if (headingInput) {
        headingInput.value = '';
        headingInput.disabled = true;
      }
    } else {
      if (headingInput) headingInput.disabled = false;
    }
  }

  if (typeSelect) {
    typeSelect.addEventListener('change', toggleFieldsForType);
    // run on load
    toggleFieldsForType();
  }

  if (form) {
    form.addEventListener('submit', function () {
      if (typeSelect && typeSelect.value === 'button') {
        // Очистить поле heading на всякий случай
        if (headingInput) headingInput.value = '';
      }
    });
  }
});
