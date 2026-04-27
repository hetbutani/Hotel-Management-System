import re

file_path = 'guest_landing_page/code.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add Razorpay script to head
if 'checkout.razorpay.com/v1/checkout.js' not in content:
    content = content.replace('</head>', '<script src="https://checkout.razorpay.com/v1/checkout.js"></script>\n</head>')

# Define the new Select Room logic with Razorpay
new_select_logic = """
            card.querySelector('.select-room').addEventListener('click', async () => {
                const checkIn = document.getElementById('check-in').value;
                const checkOut = document.getElementById('check-out').value;
                const guests = document.getElementById('guest-count').value;

                if (!checkIn || !checkOut) {
                    alert('Please select check-in and check-out dates first!');
                    document.getElementById('check-in').focus();
                    return;
                }

                try {
                    // 1. Create Razorpay Order
                    const orderRes = await fetch('http://127.0.0.1:5005/api/payments/create_order', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ amount: room.price })
                    });
                    const order = await orderRes.json();

                    if (!order.id) throw new Error('Order creation failed');

                    // 2. Open Razorpay Checkout
                    const options = {
                        "key": "rzp_test_YourKeyId", // Replace with your Key ID
                        "amount": order.amount,
                        "currency": "INR",
                        "name": "LuxeStay",
                        "description": `Booking for ${room.title}`,
                        "order_id": order.id,
                        "handler": async function (response) {
                            // 3. Verify Payment on Backend
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
                                // 4. Finalize Booking in DB
                                await fetch('http://127.0.0.1:5005/api/bookings', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({
                                        room_title: room.title,
                                        check_in: checkIn,
                                        check_out: checkOut,
                                        guests: guests,
                                        payment_id: response.razorpay_payment_id
                                    })
                                });
                                alert(`Payment Successful! Your stay at ${room.title} is confirmed.`);
                            } else {
                                alert('Payment verification failed.');
                            }
                        },
                        "prefill": {
                            "name": "Guest User",
                            "email": "guest@example.com"
                        },
                        "theme": { "color": "#2563eb" }
                    };
                    const rzp = new Razorpay(options);
                    rzp.open();

                } catch (e) {
                    console.error(e);
                    alert('Error initiating payment. Please try again.');
                }
            });
"""

# Replace the old listener
old_listener_pattern = r'card\.querySelector\(\'\.select-room\'\)\.addEventListener\(\'click\', async \(\) => \{[\s\S]+?\}\s+\);\s+'
content = re.sub(old_listener_pattern, new_select_logic, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Successfully added Razorpay to landing page.")
