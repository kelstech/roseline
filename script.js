const paymentForm = document.getElementById("paymentForm");
const contactForm = document.getElementById("contactForm");
const contactStatus = document.getElementById("contactStatus");
const year = document.getElementById("year");

year.textContent = new Date().getFullYear();

paymentForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const email = document.getElementById("email").value.trim();
  const amount = Number(document.getElementById("amount").value);
  const fullName = document.getElementById("name").value.trim();

  if (!email || !amount || !fullName) {
    alert("Please fill in all payment fields.");
    return;
  }

  const handler = PaystackPop.setup({
    key: "pk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    email,
    amount: amount * 100,
    currency: "NGN",
    ref: `RoseLine-${Date.now()}`,
    metadata: {
      custom_fields: [
        {
          display_name: "Customer Name",
          variable_name: "customer_name",
          value: fullName,
        },
      ],
    },
    callback(response) {
      alert(`Payment complete! Reference: ${response.reference}`);
      paymentForm.reset();
    },
    onClose() {
      alert("Payment window closed.");
    },
  });

  handler.openIframe();
});

contactForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const formValues = {
    name: document.getElementById("contactName").value.trim(),
    email: document.getElementById("contactEmail").value.trim(),
    subject: document.getElementById("subject").value,
    message: document.getElementById("message").value.trim(),
  };

  if (!formValues.name || !formValues.email || !formValues.subject || !formValues.message) {
    contactStatus.textContent = "Please complete all fields before sending your message.";
    return;
  }

  console.log("Complaint/Inquiry submitted:", formValues);
  contactStatus.textContent = "Thanks! Your message has been received. We'll contact you soon.";
  contactForm.reset();
});
