import re

file_path = 'guest_landing_page/code.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

contact_html = """
<!-- Contact Section -->
<section class="py-xxl bg-white dark:bg-slate-950" id="contact">
    <div class="max-w-7xl mx-auto px-8">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
            <div>
                <h2 class="text-h2 font-h2 text-on-surface mb-6">Get in Touch</h2>
                <p class="text-body-lg text-on-surface-variant mb-10 leading-relaxed">
                    Have questions about our suites or amenities? Our concierge team is available 24/7 to assist you with your booking or any special requests.
                </p>
                
                <div class="space-y-6">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center shrink-0">
                            <span class="material-symbols-outlined text-blue-600">location_on</span>
                        </div>
                        <div>
                            <h4 class="font-bold text-slate-900">Our Location</h4>
                            <p class="text-slate-500">123 Luxury Way, Coastal Paradise, CP 90210</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center shrink-0">
                            <span class="material-symbols-outlined text-blue-600">call</span>
                        </div>
                        <div>
                            <h4 class="font-bold text-slate-900">Phone</h4>
                            <p class="text-slate-500">+1 (555) LUX-STAY</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center shrink-0">
                            <span class="material-symbols-outlined text-blue-600">mail</span>
                        </div>
                        <div>
                            <h4 class="font-bold text-slate-900">Email</h4>
                            <p class="text-slate-500">concierge@luxestay.com</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="bg-slate-50 dark:bg-slate-900 p-10 rounded-3xl border border-slate-100 dark:border-slate-800 shadow-sm">
                <form id="contact-form" class="space-y-5">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                        <div>
                            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-2">Name</label>
                            <input type="text" id="contact-name" required class="w-full bg-white dark:bg-slate-800 border-none rounded-xl px-4 py-3 text-slate-700 focus:ring-2 focus:ring-blue-500 transition-all">
                        </div>
                        <div>
                            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-2">Email</label>
                            <input type="email" id="contact-email" required class="w-full bg-white dark:bg-slate-800 border-none rounded-xl px-4 py-3 text-slate-700 focus:ring-2 focus:ring-blue-500 transition-all">
                        </div>
                    </div>
                    <div>
                        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-2">Subject</label>
                        <input type="text" id="contact-subject" required class="w-full bg-white dark:bg-slate-800 border-none rounded-xl px-4 py-3 text-slate-700 focus:ring-2 focus:ring-blue-500 transition-all">
                    </div>
                    <div>
                        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-2">Message</label>
                        <textarea id="contact-message" rows="4" required class="w-full bg-white dark:bg-slate-800 border-none rounded-xl px-4 py-3 text-slate-700 focus:ring-2 focus:ring-blue-500 transition-all"></textarea>
                    </div>
                    <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-xl shadow-lg shadow-blue-100 transition-all transform active:scale-[0.98]">
                        Send Message
                    </button>
                </form>
            </div>
        </div>
    </div>
</section>

<script>
document.getElementById('contact-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = e.target.querySelector('button');
    const originalText = btn.innerText;
    
    const data = {
        name: document.getElementById('contact-name').value,
        email: document.getElementById('contact-email').value,
        subject: document.getElementById('contact-subject').value,
        message: document.getElementById('contact-message').value
    };

    btn.innerText = 'Sending...';
    btn.disabled = true;

    try {
        const response = await fetch('http://127.0.0.1:5001/api/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert('Thank you! Your message has been sent to our concierge.');
            e.target.reset();
        } else {
            alert('Something went wrong. Please try again.');
        }
    } catch (error) {
        alert('Server error. Please check if the backend is running.');
    } finally {
        btn.innerText = originalText;
        btn.disabled = false;
    }
});
</script>
"""

marker = '<!-- Footer (From JSON) -->'
if marker in content:
    content = content.replace(marker, contact_html + "\n" + marker)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully added Contact section.")
else:
    print("Footer marker not found.")
