import re

file_path = 'guest_landing_page/code.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new rendering logic including button listeners
new_render_logic = """
        const renderRooms = (rooms) => {
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
                            <button class="view-details font-label-caps text-label-caps text-primary hover:text-surface-tint uppercase tracking-wider font-semibold transition-colors">View Details</button>
                            <button class="select-room bg-surface-container-high text-on-surface hover:bg-surface-variant px-4 py-2 rounded-lg font-label-caps text-label-caps uppercase tracking-wider transition-colors">Select Room</button>
                        </div>
                    </div>
                `;
                
                // Add event listeners
                card.querySelector('.view-details').addEventListener('click', () => {
                    window.location.href = `room_details.html?room=${encodeURIComponent(room.title)}`;
                });

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
                        const res = await fetch('http://localhost:5001/api/bookings', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                room_title: room.title,
                                check_in: checkIn,
                                check_out: checkOut,
                                guests: guests
                            })
                        });
                        if (res.ok) {
                            alert(`Success! You have successfully selected the ${room.title}. We look forward to seeing you!`);
                        } else {
                            alert('Booking failed. Please try again.');
                        }
                    } catch (e) {
                        alert('Error connecting to booking service.');
                    }
                });

                container.appendChild(card);
            });
        };

        const rooms = await response.json();
        renderRooms(rooms);
"""

# Replace the old loop in DOMContentLoaded
old_loop_pattern = r'const rooms = await response\.json\(\);\s+container\.innerHTML = \'\';\s+if \(rooms\.length === 0\) \{[\s\S]+?\}\s+rooms\.forEach\(room => \{[\s\S]+?\}\);'
content = re.sub(old_loop_pattern, new_render_logic, content)

# Also update the search callback to use renderRooms
old_search_render = r'const rooms = await response\.json\(\);\s+container\.innerHTML = \'\';\s+if \(rooms\.length === 0\) \{[\s\S]+?\}\s+// Same rendering logic as initial load\s+rooms\.forEach\(room => \{[\s\S]+?\}\);'
content = re.sub(old_search_render, 'const rooms = await response.json(); renderRooms(rooms);', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Successfully updated landing page buttons.")
