import re
from bs4 import BeautifulSoup

with open('C:/Users/RAHUL/OneDrive/Desktop/ISTD/office-bearers.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

slides = soup.find_all('div', class_='team-slide')
categories_to_keep = ['Event Executives', 'Design Executives', 'Tech Executives', 'Content Executives', 'Outreach Executives']
category_map = {}

for slide in slides:
    cat = slide.get('data-category')
    if cat in categories_to_keep:
        members = slide.find_all('div', class_='team-member')
        category_map[cat] = []
        for m in members:
            # Extract data
            img = m.find('img')
            img_src = img['src'] if img else ''
            name_el = m.find('h3')
            name = name_el.text.strip() if name_el else ''
            
            pos_el = m.find('p', class_='position')
            pos = pos_el.text.strip() if pos_el else ''
            
            desc_el = m.find('p', class_='description')
            desc = desc_el.text.strip() if desc_el else ''
            
            socials = m.find_all('a', class_='social-link')
            social_links = []
            for s in socials:
                classes = s.get('class', [])
                icon_class = 'fa-instagram' if 'instagram' in classes else 'fa-linkedin'
                social_links.append({'href': s.get('href', ''), 'icon': icon_class})
            
            badges = []
            details_el = m.find('p', class_='member-details')
            if details_el:
                badge_els = details_el.find_all('span')
                for b in badge_els:
                    badges.append(b.text.strip())
            
            category_map[cat].append({
                'name': name,
                'image': img_src,
                'position': pos,
                'description': desc,
                'socials': social_links,
                'badges': badges
            })

new_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Our Team - ISTD STUDENT CHAPTER</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link rel="stylesheet" href="assets/css/style.css">
    <link rel="icon" href="assets/images/favicon.jpeg">
</head>
<body>
    <!-- Header/Navigation -->
    <header class="header">
        <nav class="navbar">
            <div class="nav-container">
                <div class="logo">
                    <h2><img src="assets/images/logo istd.png" alt="ISTD Logo">ISTD SVCE</h2>
                </div>
                <ul class="nav-menu">
                    <li><a href="/" class="nav-link">Home</a></li>
                    <li><a href="/about.html" class="nav-link">About</a></li>
                    <li><a href="/events.html" class="nav-link">Events</a></li>
                    <li><a href="/office-bearers.html" class="nav-link active">Team</a></li>
                </ul>
                <div class="nav-auth">
                    <a href="https://docs.google.com/forms/d/e/1FAIpQLScLQasdYzA80VnhOAEFHTIybjhXHRBCYOCBLn8u8AofKQaRXw/viewform?usp=header" target="_blank">
                        <button class="auth-btn">Login / Register</button>
                    </a> 
                </div>
                <div class="hamburger"><span></span><span></span><span></span></div>
            </div>
        </nav>
    </header>

    <section class="page-hero">
        <div class="container">
            <h1>Office Bearers</h1>
            <p>Meet the dedicated team of executives shaping the ISTD SVCE Student Chapter.</p>
            
            <div class="team-filters" style="margin-top: 2rem;">
"""
cat_ids = {'Event Executives': 'event', 'Tech Executives': 'tech', 'Design Executives': 'design', 'Outreach Executives': 'outreach', 'Content Executives': 'content'}
first = True
for cat in categories_to_keep:
    active_cls = 'active' if first else ''
    new_html += f'                <button class="filter-btn {active_cls}" onclick="filterTeam(\'{cat_ids[cat]}\')">{cat.split()[0]}</button>\n'
    first = False

new_html += """            </div>
        </div>
    </section>

    <section class="section-padding bg-cream">
        <div class="container">
"""

first = True
for cat in categories_to_keep:
    display_style = 'grid' if first else 'none'
    first = False
    new_html += f'            <div class="team-grid" id="{cat_ids[cat]}-grid" style="display: {display_style};">\n'
    for m in category_map.get(cat, []):
        new_html += f'''                <div class="team-member">
                    <div class="member-photo">
                        <img src="{m['image']}" alt="{m['name']}">
                        <div class="social-overlay">
                            <div class="social-links">
'''
        for s in m['socials']:
            if s['href']:
                new_html += f'                                <a href="{s["href"]}" target="_blank" class="social-link"><i class="fab {s["icon"]}"></i></a>\n'
        new_html += f'''                            </div>
                        </div>
                    </div>
                    <div class="member-info">
                        <h3>{m['name']}</h3>
                        <p class="position">{m['position']}</p>
'''
        if m['badges']:
            new_html += '                        <p class="member-details">'
            for b in m['badges']:
                new_html += f'<span class="dept-badge">{b}</span> '
            new_html += '</p>\n'
            
        new_html += f'''                        <p class="description">{m['description']}</p>
                    </div>
                </div>
'''
    new_html += '            </div>\n'

new_html += """        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>ISTD SVCE</h3>
                    <p>Empowering learners worldwide with quality training and development programs.</p>
                    <div class="social-icons">
                        <a href="https://www.instagram.com/istd_svce/" target="_blank"><i class="fab fa-instagram"></i></a>
                        <a href="https://www.linkedin.com/in/istd-student-chapter-svce-281b53378" target="_blank"><i class="fab fa-linkedin"></i></a>
                    </div>
                </div>
                <div class="footer-section">
                    <h4>Quick Links</h4>
                    <ul>
                        <li><a href="/">Home</a></li>
                        <li><a href="/about.html">About Us</a></li>
                        <li><a href="/events.html">Events</a></li>
                        <li><a href="/office-bearers.html">Our Team</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Get In Touch</h4>
                    <div class="contact-item">
                        <i class="fas fa-envelope"></i>
                        <span>istd@svce.ac.in</span>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-phone"></i>
                        <span>+91 89409 63521</span>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-map-marker-alt"></i>
                        <span>SVCE Campus, Chennai</span>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 ISTD Student Chapter SVCE. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        // Hamburger menu
        const hamburger = document.querySelector('.hamburger');
        const navMenu = document.querySelector('.nav-menu');

        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Header scroll effect
        window.addEventListener('scroll', () => {
            const header = document.querySelector('.header');
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });

        // Filter team members
        function filterTeam(category) {
            // Update active button
            const buttons = document.querySelectorAll('.filter-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            // Hide all grids
            const grids = document.querySelectorAll('.team-grid');
            grids.forEach(grid => {
                grid.style.display = 'none';
            });

            // Show selected grid
            const selectedGrid = document.getElementById(category + '-grid');
            if (selectedGrid) {
                selectedGrid.style.display = 'grid';
            }
        }
    </script>
</body>
</html>
"""

with open('C:/Users/RAHUL/OneDrive/Desktop/ISTD/office-bearers.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print('Successfully wrote 25 office-bearers HTML.')
