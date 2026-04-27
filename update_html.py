import re

file_path = 'guest_landing_page/code.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-gutter">'
end_marker = '<!-- Footer (From JSON) -->'

replacement = """<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-gutter" id="rooms-container">
    <p class="text-center col-span-full font-body-md text-on-surface-variant">Loading accommodations...</p>
</div>
</section>
</main>

<script>
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('rooms-container');
    try {
        const response = await fetch('http://localhost:5000/api/rooms/featured');
        if (!response.ok) throw new Error('Failed to fetch rooms');
        
        const rooms = await response.json();
        container.innerHTML = '';
        
        if (rooms.length === 0) {
            container.innerHTML = '<p class="text-center col-span-full font-body-md text-on-surface-variant">No accommodations available.</p>';
            return;
        }

        rooms.forEach(room => {
            const featuresHtml = room.features.map(f => `
                <span class="inline-flex items-center gap-1 bg-surface-container-low text-on-surface px-2 py-1 rounded font-label-caps text-label-caps">
                    <span class="material-symbols-outlined" style="font-size: 14px;">${f.icon}</span> ${f.text}
                </span>
            `).join('');

            const card = document.createElement('div');
            card.className = 'group bg-white rounded-xl overflow-hidden shadow-[0_2px_4px_rgba(0,0,0,0.05)] hover:shadow-[0_10px_15px_-3px_rgba(0,0,0,0.1)] transition-all duration-300 flex flex-col';
            card.innerHTML = `
                <div class="relative h-64 overflow-hidden">
                    <img alt="${room.title}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" src="${room.image_url}" />
                    <div class="absolute top-4 right-4 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-full flex items-center gap-1 shadow-sm">
                        <span class="material-symbols-outlined text-secondary-container" style="font-size: 16px; font-variation-settings: 'FILL' 1;">star</span>
                        <span class="font-label-caps text-label-caps text-on-surface font-bold">${room.rating}</span>
                    </div>
                </div>
                <div class="p-lg flex flex-col flex-grow">
                    <div class="flex justify-between items-start mb-sm">
                        <h3 class="font-h3 text-h3 text-on-surface">${room.title}</h3>
                        <div class="text-right">
                            <span class="block font-stat-value text-stat-value text-primary">$${room.price}</span>
                            <span class="font-body-sm text-body-sm text-on-surface-variant">/ night</span>
                        </div>
                    </div>
                    <p class="font-body-sm text-body-sm text-on-surface-variant mb-md line-clamp-2">${room.description}</p>
                    <div class="flex flex-wrap gap-xs mb-lg">
                        ${featuresHtml}
                    </div>
                    <div class="mt-auto pt-md border-t border-outline-variant flex justify-between items-center">
                        <a class="font-label-caps text-label-caps text-primary hover:text-surface-tint uppercase tracking-wider font-semibold transition-colors" href="#">View Details</a>
                        <button class="bg-surface-container-high text-on-surface hover:bg-surface-variant px-4 py-2 rounded-lg font-label-caps text-label-caps uppercase tracking-wider transition-colors">Select Room</button>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Error fetching rooms:', error);
        container.innerHTML = '<p class="text-center col-span-full font-body-md text-error">Failed to load accommodations. Please ensure the backend is running.</p>';
    }
});
</script>
"""

# Extract the part we want to replace
start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + replacement + '\n' + content[end_idx:]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully replaced.")
else:
    print("Markers not found.")
