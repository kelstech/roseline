# RoseLine Website

A responsive single-page storefront for **RoseLine** to sell glasses, frames, lenses, contact lenses, and eye accessories.

## Features

- Product category showcase for optical products.
- Paystack payment form and inline checkout integration.
- Complaints and inquiries form for customer support.
- Mobile-friendly layout.

## Run locally

Open `index.html` directly in a browser, or serve with:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080`.

## Paystack setup

1. Open `script.js`.
2. Replace `pk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` with your real Paystack public key.
3. For production, validate payment references on your backend before fulfillment.
