import re

file_path = "c:\\cazalleida . com\\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CSS
old_css_cards = """  .species .head{text-align:center;max-width:620px;margin:0 auto 60px}
  .species .head h2{font-size:clamp(30px,4vw,48px);margin-bottom:16px}
  .species .head p{opacity:.75;font-weight:300;font-size:17px}
  .cards{display:grid;grid-template-columns:repeat(5,1fr);gap:16px}
  .card{background:rgba(244,239,227,.05);border:1px solid rgba(244,239,227,.12);border-radius:18px;overflow:hidden;transition:.3s}"""

new_css_cards = """  .species .head{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;margin-bottom:40px;text-align:left}
  .species .head .text{max-width:620px}
  .species .head h2{font-size:clamp(30px,4vw,48px);margin-bottom:12px}
  .species .head p{opacity:.75;font-weight:300;font-size:17px}
  .slider-controls{display:flex;gap:12px;flex:none}
  .slider-btn{width:48px;height:48px;border-radius:50%;background:rgba(244,239,227,.08);border:1px solid rgba(244,239,227,.15);color:var(--cream);cursor:pointer;display:flex;align-items:center;justify-content:center;transition:.3s}
  .slider-btn:hover{background:var(--gold);color:var(--moss);border-color:var(--gold);transform:scale(1.1)}
  .slider-btn svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}
  .cards{display:flex;gap:24px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;padding-bottom:30px;scrollbar-width:none;-ms-overflow-style:none}
  .cards::-webkit-scrollbar{display:none}
  .card{flex:0 0 calc(33.333% - 16px);min-width:310px;scroll-snap-align:start;background:rgba(244,239,227,.05);border:1px solid rgba(244,239,227,.12);border-radius:20px;overflow:hidden;transition:.4s}"""

content = content.replace(old_css_cards, new_css_cards)

old_css_media = """  @media(max-width:880px){
    nav .links{display:none}
    .where .grid{grid-template-columns:1fr;gap:44px}
    .contact .grid{grid-template-columns:1fr;gap:40px}
    .gal-grid{column-count:2}
    .pack-grid{grid-template-columns:1fr;max-width:440px;margin:0 auto}
    .cards{grid-template-columns:1fr 1fr}
    header{padding:16px 20px}
    .wrap{padding:0 20px}
  }
  @media(max-width:540px){.cards{grid-template-columns:1fr}.gal-grid{column-count:1}.lead-form .row{grid-template-columns:1fr}}"""

new_css_media = """  @media(max-width:880px){
    nav .links{display:none}
    .where .grid{grid-template-columns:1fr;gap:44px}
    .contact .grid{grid-template-columns:1fr;gap:40px}
    .gal-grid{column-count:2}
    .pack-grid{grid-template-columns:1fr;max-width:440px;margin:0 auto}
    .species .head{flex-direction:column;align-items:flex-start}
    .slider-controls{display:none} /* Hide buttons on mobile, swipe is better */
    header{padding:16px 20px}
    .wrap{padding:0 20px}
  }
  @media(max-width:540px){
    .card{flex:0 0 85%}
    .gal-grid{column-count:1}
    .lead-form .row{grid-template-columns:1fr}
  }"""

content = content.replace(old_css_media, new_css_media)

# 2. Update HTML
old_html_species = """    <div class="head reveal">
      <h2 data-i18n="sp_title">Qué se caza aquí</h2>
      <p data-i18n="sp_sub">Especies cinegéticas más habituales en nuestra zona.</p>
    </div>
    <div class="cards">"""

new_html_species = """    <div class="head reveal">
      <div class="text">
        <h2 data-i18n="sp_title">Qué se caza aquí</h2>
        <p data-i18n="sp_sub">Especies cinegéticas más habituales en nuestra zona.</p>
      </div>
      <div class="slider-controls">
        <button class="slider-btn prev" id="spPrev" aria-label="Anterior"><svg viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg></button>
        <button class="slider-btn next" id="spNext" aria-label="Siguiente"><svg viewBox="0 0 24 24"><path d="M9 18l6-6-6-6"/></svg></button>
      </div>
    </div>
    <div class="cards" id="spCards">"""

content = content.replace(old_html_species, new_html_species)

# Increase image height on cards to make them pop more
content = content.replace(".card-img{width:100%;height:180px;object-fit:cover;display:block;transition:.5s}", ".card-img{width:100%;height:220px;object-fit:cover;display:block;transition:.6s}")

# 3. Add JS for slider
old_js = """  // ---- formulario (demo, sin servidor todavía) ----"""
new_js = """  // ---- slider ----
  const spCards = document.getElementById('spCards');
  if(spCards) {
    document.getElementById('spPrev').onclick = () => spCards.scrollBy({left: -350, behavior: 'smooth'});
    document.getElementById('spNext').onclick = () => spCards.scrollBy({left: 350, behavior: 'smooth'});
  }

  // ---- formulario (demo, sin servidor todavía) ----"""

content = content.replace(old_js, new_js)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Slider and animations added successfully.")
