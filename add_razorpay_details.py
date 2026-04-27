import re

file_path = 'guest_landing_page/room_details.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add Razorpay script to head
if 'checkout.razorpay.com/v1/checkout.js' not in content:
    content = content.replace('</head>', '<script src="https://checkout.razorpay.com/v1/checkout.js"></script>\n</head>')

# Update the "Book This Room" button to use Razorpay
new_booking_script = """
    <script>
        async function initiateBooking(roomTitle, price) {
            try {
                // 1. Create Order
                const orderRes = await fetch('http://127.0.0.1:5005/api/payments/create_order', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ amount: price })
                });
                const order = await orderRes.json();

                if (!order.id) throw new Error('Order creation failed');

                // 2. Open Checkout
                const options = {
                    "key": "rzp_test_YourKeyId",
                    "amount": order.amount,
                    "currency": "INR",
                    "name": "LuxeStay",
                    "description": `Booking for ${roomTitle}`,
                    "order_id": order.id,
                    "handler": async function (response) {
                        // 3. Verify Payment
                        const verifyRes = await fetch('http://127.0.0.1:5005/api/payments/verify', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                razorpay_order_id: response.razorpay_order_id,
                                razorpay_payment_id: response.razorpay_payment_id,
                                razorpay_signature: response.razorpay_signature
                            })
                        });

                        if (verifyRes.ok) {
                            // 4. Save Booking
                            await fetch('http://127.0.0.1:5005/api/bookings', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    room_title: roomTitle,
                                    check_in: new Date().toISOString().split('T')[0], // Placeholder dates
                                    check_out: new Date(Date.now() + 86400000).toISOString().split('T')[0],
                                    guests: "1 Guest",
                                    payment_id: response.razorpay_payment_id
                                })
                            });
                            alert(`Success! Payment received for ${roomTitle}.`);
                        } else {
                            alert('Payment verification failed.');
                        }
                    },
                    "theme": { "color": "#2563eb" }
                };
                const rzp = new Razorpay(options);
                rzp.open();
            } catch (e) {
                alert('Payment failed to start.');
            }
        }

        document.addEventListener('DOMContentLoaded', async () => {
"""

# Replace the start of the script
content = content.replace("<script>\n        document.addEventListener('DOMContentLoaded', async () => {", new_booking_script)

# Update the button HTML in the template literal
content = content.replace(
    'button onclick="alert(\'Proceeding to secure checkout for ${room.title}!\')"',
    'button onclick="initiateBooking(\'${room.title}\', ${room.price})"'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Successfully added Razorpay to room details page.")
