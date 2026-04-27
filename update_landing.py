import re

file_path = 'guest_landing_page/code.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Admin link in Nav
content = content.replace('href="../admin_dashboard/code.html">Admin</a>', 'href="../auth/login.html">Admin</a>')

# 2. Add Testimonials section before the footer
testimonials_html = """
<!-- Testimonials Section -->
<section class="py-xxl bg-slate-50 dark:bg-slate-900/30" id="testimonials">
    <div class="max-w-container-max mx-auto px-6 lg:px-lg">
        <div class="text-center mb-xl">
            <h2 class="font-h2 text-h2 text-on-surface mb-sm">What Our Guests Say</h2>
            <p class="font-body-md text-body-md text-on-surface-variant max-w-2xl mx-auto">Real stories from travelers who have experienced the LuxeStay standard of excellence.</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-gutter" id="reviews-container">
            <!-- Reviews will load here -->
            <p class="text-center col-span-full text-slate-400">Loading guest stories...</p>
        </div>
    </div>
</section>

<script>
// Append to existing script or add new one
document.addEventListener('DOMContentLoaded', async () => {
    // Reviews Fetching Logic
    const reviewsContainer = document.getElementById('reviews-container');
    try {
        const response = await fetch('http://localhost:5001/api/reviews');
        const reviews = await response.json();
        reviewsContainer.innerHTML = '';
        
        reviews.forEach(review => {
            const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
            const card = document.createElement('div');
            card.className = 'bg-white dark:bg-slate-800 p-lg rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 flex flex-col h-full';
            card.innerHTML = `
                <div class="text-secondary-container mb-4 text-xl">${stars}</div>
                <p class="font-body-md text-slate-600 dark:text-slate-300 italic mb-6 flex-grow">"${review.content}"</p>
                <div class="flex items-center gap-4">
                    <img src="${review.avatar}" class="w-12 h-12 rounded-full object-cover">
                    <div>
                        <h4 class="font-bold text-slate-800 dark:text-white">${review.name}</h4>
                        <p class="text-xs text-slate-500 uppercase tracking-wider font-semibold">${review.role}</p>
                    </div>
                </div>
            `;
            reviewsContainer.appendChild(card);
        });
    } catch (e) {
        reviewsContainer.innerHTML = '<p class="text-center col-span-full text-red-400">Unable to load reviews.</p>';
    }
});
</script>
"""

footer_marker = '<!-- Footer (From JSON) -->'
if footer_marker in content:
    content = content.replace(footer_marker, testimonials_html + "\n" + footer_marker)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated landing page.")
else:
    print("Footer marker not found.")
