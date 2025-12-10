document.addEventListener("DOMContentLoaded", function () {
  // Auto-format numeric inputs
  const numberInputs = document.querySelectorAll('input[type="number"]');
  numberInputs.forEach((input) => {
    input.addEventListener("blur", function () {
      if (this.value) {
        this.value = parseFloat(this.value).toFixed(6);
      }
    });
  });

  // Form validation
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", function (event) {
      const cryptoSelect = document.getElementById("cryptocurrency");
      if (cryptoSelect && !cryptoSelect.value) {
        alert("Please select a cryptocurrency");
        event.preventDefault();
        return false;
      }

      // Check if at least one feature is filled
      const featureInputs = document.querySelectorAll(
        'input[name]:not([name="cryptocurrency"])'
      );
      let hasFeature = false;
      featureInputs.forEach((input) => {
        if (input.value.trim() !== "") {
          hasFeature = true;
        }
      });

      if (!hasFeature) {
        alert("Please enter at least one market feature for prediction");
        event.preventDefault();
        return false;
      }

      return true;
    });
  });

  // Add loading spinner on form submission
  const submitButtons = document.querySelectorAll('button[type="submit"]');
  submitButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const form = this.closest("form");
      if (form.checkValidity()) {
        this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        this.disabled = true;
        form.submit();
      }
    });
  });
});

// API functions
async function fetchModels() {
  try {
    const response = await fetch("/api/models");
    const data = await response.json();
    console.log("Available models:", data);
    return data;
  } catch (error) {
    console.error("Error fetching models:", error);
    return null;
  }
}

async function predictPriceAPI(cryptocurrency, features) {
  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        cryptocurrency: cryptocurrency,
        features: features,
      }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("API Error:", error);
    return { error: error.message };
  }
}
