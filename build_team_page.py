"""Rebuild office-bearers.html from git HEAD with filter-tab UI."""
import subprocess
import re
from bs4 import BeautifulSoup

ROOT = "C:/Users/RAHUL/OneDrive/Desktop/ISTD"
result = subprocess.run(
    ["git", "-C", ROOT, "show", "HEAD:office-bearers.html"],
    capture_output=True,
    text=True,
    encoding="utf-8",
)
html = result.stdout
soup = BeautifulSoup(html, "html.parser")

CAT_MAP = {
    "Core Team": ("core", "Core Team"),
    "Event Executives": ("event", "Event"),
    "Tech Executives": ("tech", "Tech"),
    "Design Executives": ("design", "Design"),
    "Outreach Executives": ("outreach", "Outreach"),
    "Content Executives": ("content", "Content"),
    "Dept Coordinators": ("coordinators", "Coordinators"),
    "Documentation Executives": ("documentation", "Documentation"),
}

OBS_CATS = ["Event Executives", "Tech Executives", "Design Executives", "Outreach Executives", "Content Executives"]

categories = {}
for slide in soup.find_all("div", class_="team-slide"):
    cat = slide.get("data-category")
    if cat not in CAT_MAP:
        continue
    members = []
    for m in slide.find_all("div", class_="team-member"):
        member_soup = BeautifulSoup(str(m), "html.parser")
        member = member_soup.find("div", class_="team-member")
        desc = member.find("p", class_="description")
        if desc and not member.find("a", class_="view-profile"):
            vp = member_soup.new_tag("a", href="#", **{"class": "view-profile"})
            vp.append("View Profile ")
            icon = member_soup.new_tag("i", **{"class": "fas fa-arrow-right"})
            vp.append(icon)
            desc.insert_after(vp)
        members.append(str(member_soup.find("div", class_="team-member")))
    categories[cat] = {
        "id": CAT_MAP[cat][0],
        "label": CAT_MAP[cat][1],
        "subtitle": slide.get("data-subtitle", ""),
        "members": members,
    }

FILTER_BTNS = [
    ("all", "All", True),
    ("core", "Core", False),
    ("event", "Event", False),
    ("tech", "Tech", False),
    ("design", "Design", False),
    ("outreach", "Outreach", False),
    ("content", "Content", False),
    ("coordinators", "Coordinators", False),
    ("documentation", "Docs", False),
]

def render_grid(cat_key, display="none"):
    data = categories[cat_key]
    members_html = "\n".join(f"                {m}" for m in data["members"])
    return f'''            <div class="team-category-block" data-team="{data["id"]}" id="{data["id"]}-section">
                <div class="team-category-header">
                    <span class="section-label">{data["label"].upper()}</span>
                    <h2>{cat_key}</h2>
                    <p>{data["subtitle"]}</p>
                </div>
                <div class="team-grid" id="{data["id"]}-grid">
{members_html}
                </div>
            </div>'''

filter_html = ""
for fid, label, active in FILTER_BTNS:
    cls = "filter-btn active" if active else "filter-btn"
    filter_html += f'                <button class="{cls}" data-filter="{fid}">{label}</button>\n'

core_block = render_grid("Core Team", "block")
obs_blocks = ""
for cat in OBS_CATS:
    obs_blocks += render_grid(cat) + "\n"
other_blocks = render_grid("Dept Coordinators") + "\n" + render_grid("Documentation Executives")

out = f'''<!DOCTYPE html>
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
            <span class="section-label page-hero-label">Leadership</span>
            <h1>Our Team</h1>
            <p>Meet the dedicated leaders and office bearers shaping the ISTD SVCE Student Chapter.</p>
            <div class="team-filters hero-filters">
{filter_html}            </div>
        </div>
    </section>

    <section class="section-padding bg-cream team-section">
        <div class="container">
            <div id="team-sections">
{core_block}
                <div class="team-obs-divider" data-team="obs-header">
                    <span class="section-label">Office Bearers</span>
                    <h2>Executive Teams</h2>
                    <p>Specialized wings driving events, technology, design, outreach, and content across the chapter.</p>
                </div>
{obs_blocks}{other_blocks}            </div>
        </div>
    </section>

    <footer class="footer">
        <div class="footer-container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>ISTD SVCE</h3>
                    <p>Empowering learners with quality training, leadership development, and industry exposure.</p>
                    <div class="social-icons">
                        <a href="https://www.instagram.com/istd_svce/" target="_blank" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                        <a href="https://www.linkedin.com/in/istd-student-chapter-svce-281b53378" target="_blank" aria-label="LinkedIn"><i class="fab fa-linkedin"></i></a>
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
                    <h4>Events</h4>
                    <ul>
                        <li><a href="/events.html">All Events</a></li>
                        <li><a href="/events.html">Monthly Meets</a></li>
                        <li><a href="/events.html">Event Reports</a></li>
                        <li><a href="/events.html">Annual Reports</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Contact</h4>
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
                <p>&copy; 2025 ISTD Student Chapter SVCE. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        const hamburger = document.querySelector('.hamburger');
        const navMenu = document.querySelector('.nav-menu');
        hamburger.addEventListener('click', () => {{
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        }});
        document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {{
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }}));
        window.addEventListener('scroll', () => {{
            const header = document.querySelector('.header');
            header.classList.toggle('scrolled', window.scrollY > 50);
        }});

        const OBS_IDS = ['event', 'tech', 'design', 'outreach', 'content'];
        const ALL_IDS = ['core', ...OBS_IDS, 'coordinators', 'documentation'];

        function setTeamVisibility(filter) {{
            const obsDivider = document.querySelector('[data-team="obs-header"]');
            ALL_IDS.forEach(id => {{
                const block = document.getElementById(id + '-section');
                if (!block) return;
                if (filter === 'all') {{
                    block.style.display = 'block';
                }} else {{
                    block.style.display = id === filter ? 'block' : 'none';
                }}
            }});
            if (obsDivider) {{
                obsDivider.style.display = (filter === 'all') ? 'block' : 'none';
            }}
        }}

        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                setTeamVisibility(btn.dataset.filter);
            }});
        }});

        document.querySelectorAll('.view-profile').forEach(link => {{
            link.addEventListener('click', e => e.preventDefault());
        }});

        setTeamVisibility('all');
    </script>
</body>
</html>
'''

with open(f"{ROOT}/office-bearers.html", "w", encoding="utf-8") as f:
    f.write(out)
print("Built office-bearers.html with", sum(len(c["members"]) for c in categories.values()), "members")
