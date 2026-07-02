import re

file_path = "c:\\cazalleida . com\\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. CSS
content = content.replace(
    ".cards{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}",
    ".cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:20px}"
)
content = content.replace(
    ".pack-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;align-items:stretch}",
    ".pack-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px;align-items:stretch}"
)

# 2. Add IT button
content = content.replace(
    """<button data-lang="en">EN</button>
    </div>""",
    """<button data-lang="en">EN</button>
      <button data-lang="it">IT</button>
    </div>"""
)

# 3. Species HTML
old_species = """<div class="card reveal">
        <img class="card-img" src="images/perdiz.jpg" alt="Perdiz roja">
        <div class="card-body">
          <h3 data-i18n="sp3_n">Perdiz roja</h3>
          <div class="when" data-i18n="sp3_w">Oct · Ene</div>
          <p data-i18n="sp3_d">La de toda la vida en el monte mediterráneo. Lista y rápida, no se deja engañar fácil. Una pieza muy apreciada y de las que más se disfrutan al perro.</p>
        </div>
      </div>
      <div class="card reveal">
        <img class="card-img" src="images/paloma.jpg" alt="Paloma torcaz">
        <div class="card-body">
          <h3 data-i18n="sp4_n">Tórtola y paloma</h3>
          <div class="when" data-i18n="sp4_w">Pasos de temporada</div>
          <p data-i18n="sp4_d">Pasan en sus fechas concretas, marcadas cada temporada. Días sueltos, pero muy esperados, sobre todo el paso de la paloma.</p>
        </div>
      </div>
    </div>"""

new_species = """<div class="card reveal">
        <img class="card-img" src="images/perdiz.jpg" alt="Perdiz roja">
        <div class="card-body">
          <h3 data-i18n="sp3_n">Perdiz roja</h3>
          <div class="when" data-i18n="sp3_w">Oct · Ene</div>
          <p data-i18n="sp3_d">La perdiz roja salvaje es muy escasa en nuestra zona, pero cada temporada realizamos unas cuantas sueltas para reforzar su presencia en nuestro terreno.</p>
        </div>
      </div>
      <div class="card reveal">
        <img class="card-img" src="images/paloma.jpg" alt="Paloma torcaz">
        <div class="card-body">
          <h3 data-i18n="sp4_n">Paloma zurita y torcaz</h3>
          <div class="when" data-i18n="sp4_w">Pasos de temporada</div>
          <p data-i18n="sp4_d">Estas especies son cada vez más presentes durante todo el año, siendo su momento más óptimo en la media veda en verano.</p>
        </div>
      </div>
      <div class="card reveal">
        <img class="card-img" src="images/becada.png" alt="Becada">
        <div class="card-body">
          <h3 data-i18n="sp5_n">Becada</h3>
          <div class="when" data-i18n="sp5_w">Tiempo de nevadas</div>
          <p data-i18n="sp5_d">La Becada es cada vez más frecuente en nuestro territorio siendo un ave migratoria que durante el tiempo más frío en Europa nos visitan huyendo de las fuertes nevadas que le impiden comer con su largo pico lombrices, etc.</p>
        </div>
      </div>
    </div>"""

content = content.replace(old_species, new_species)

# 4. Packs Header
old_phead = """<div class="phead reveal">
      <div class="section-eyebrow" data-i18n="pk_eyebrow">Tarifas</div>
      <h2 data-i18n="pk_title">Packs de caza</h2>
      <p data-i18n="pk_sub">Cada jornada se adapta al grupo y a las fechas. Dinos qué buscas y te pasamos precio.</p>
    </div>"""
new_phead = """<div class="phead reveal">
      <div class="section-eyebrow" data-i18n="pk_eyebrow">Tarifas</div>
      <h2 data-i18n="pk_title">Packs de caza</h2>
      <p data-i18n="pk_sub">Cada jornada se adapta al grupo y a las fechas. Dinos qué buscas y te pasamos precio.</p>
      <p data-i18n="pk_acc" style="margin-top:20px; font-weight:500; color:var(--moss)">El coto dispone de alojamiento en el centro del propio cazadero a 5 minutos.</p>
    </div>"""
content = content.replace(old_phead, new_phead)

# 5. Add 2 new Packs
old_pack_end = """<li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 13l4 4L19 7"/></svg><span data-i18n="pk3_l4">El pack estrella para los franceses</span></li>
        </ul>
        <a href="#contact" class="btn btn-outline" data-i18n="pk_cta">Pide precio →</a>
      </div>

    </div>"""

new_pack_end = """<li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 13l4 4L19 7"/></svg><span data-i18n="pk3_l4">El pack estrella para los franceses</span></li>
        </ul>
        <a href="#contact" class="btn btn-outline" data-i18n="pk_cta">Pide precio →</a>
      </div>

      <div class="pack reveal">
        <div class="tier" data-i18n="pk4_tier">Temporada</div>
        <h3 data-i18n="pk4_name">Tarjeta de temporada</h3>
        <div class="dur" data-i18n="pk4_dur">3 días a la semana</div>
        <ul>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 13l4 4L19 7"/></svg><span data-i18n="pk4_l1">Caza jueves, sábados, domingos y festivos</span></li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 13l4 4L19 7"/></svg><span data-i18n="pk4_l2">Acceso regular durante toda la temporada</span></li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 13l4 4L19 7"/></svg><span data-i18n="pk4_l3">Ideal para el cazador habitual</span></li>
        </ul>
        <a href="#contact" class="btn btn-outline" data-i18n="pk_cta">Pide precio →</a>
      </div>

      <div class="pack reveal">
        <div class="tier" data-i18n="pk5_tier">A medida</div>
        <h3 data-i18n="pk5_name">Pase de día</h3>
        <div class="dur" data-i18n="pk5_dur">Días sueltos</div>
        <ul>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 13l4 4L19 7"/></svg><span data-i18n="pk5_l1">Caza en nuestra área privada</span></li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 13l4 4L19 7"/></svg><span data-i18n="pk5_l2">Precio variable según las especies a cazar</span></li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 13l4 4L19 7"/></svg><span data-i18n="pk5_l3">Flexibilidad total para tu escapada</span></li>
        </ul>
        <a href="#contact" class="btn btn-outline" data-i18n="pk_cta">Pide precio →</a>
      </div>

    </div>"""
content = content.replace(old_pack_end, new_pack_end)

# 6. Contact CTA
content = content.replace(
    """<h2 data-i18n="ct_title">Cuéntanos y <em>preparamos tu jornada</em></h2>
      <p class="lead" data-i18n="ct_p">Dinos qué quieres cazar y cuándo. Te respondemos con disponibilidad y precio, sin compromiso.</p>""",
    """<h2 data-i18n="ct_title">Cuéntanos y <em>preparamos tu jornada</em></h2>
      <p class="lead" data-i18n="ct_p">Contacta con nosotros y preparamos tu cacería a medida para ti o tu grupo.</p>"""
)

# 7. T object
old_t_start = "const T={"
old_t_end = "};"

t_pattern = re.compile(r"const T=\{.*?\n  \};", re.DOTALL)

new_t = """const T={
    es:{nav_where:"El coto",nav_species:"La caza",nav_contact:"Contacto",
      hero_eyebrow:"Coto privado · Caza menor",
      hero_title:'Descubre la mejor zona<br>de caza de <em>Cataluña</em><span class="place">Les Garrigues, Lleida</span>',
      hero_sub:"Más de 3.000 hectáreas de monte, pinares y siembras: el conejo manda todo el año y, en otoño, llega el zorzal. Caza tradicional, a tu ritmo.",
      hero_cta1:"Solicita tu jornada →",hero_cta2:"Conoce el coto",scroll:"Desliza",
      where_eyebrow:"Dónde estamos",where_title:"En el corazón de Les Garrigues",
      where_p1:"Nuestro coto está en el término de Granyena de les Garrigues. Una finca privada de monte bajo, pinares y campos de siembra.",
      where_ha_num:"+3.000",where_ha_txt:"hectáreas<br>de terreno privado",
      where_p2:"Llegar es fácil: estamos a un paso de las grandes ciudades, pero rodeados de campo de verdad.",
      map_title:"A tiro de piedra",map_lead:"Tiempo en coche",
      sp_title:"Qué se caza aquí",sp_sub:"Especies cinegéticas más habituales en nuestra zona.",
      sp_star:"El rey",sp1_n:"Conejo",sp1_w:"Casi todo el año",sp1_d:"En los últimos cinco años se ha multiplicado muchísimo. Hay tanto conejo que en verano nos toca hacer descaste para evitar daños en la agricultura.",
      sp2_n:"Zorzal",sp2_w:"Oct · Feb",sp2_d:"Ave migratoria que llega cada otoño buscando la aceituna. Lleida cae en plena ruta de paso, así que cuando entran lo hacen por miles. Es lo que más ilusión le hace al cazador francés.",
      sp3_n:"Perdiz roja",sp3_w:"Oct · Ene",sp3_d:"La perdiz roja salvaje es muy escasa en nuestra zona, pero cada temporada realizamos unas cuantas sueltas para reforzar su presencia en nuestro terreno.",
      sp4_n:"Paloma zurita y torcaz",sp4_w:"Pasos de temporada",sp4_d:"Estas especies son cada vez más presentes durante todo el año, siendo su momento más óptimo en la media veda en verano.",
      sp5_n:"Becada",sp5_w:"Tiempo de nevadas",sp5_d:"La Becada es cada vez más frecuente en nuestro territorio siendo un ave migratoria que durante el tiempo más frío en Europa nos visitan huyendo de las fuertes nevadas que le impiden comer con su largo pico lombrices, etc.",
      jor_eyebrow:"Un día en el coto",jor_title:"Cómo es cazar aquí",
      jor_p:"Se sale temprano, con la escarcha todavía en los olivos. Un guía que conoce el terreno palmo a palmo te lleva a los mejores puestos. A media mañana, un alto para almorzar. Por la tarde, otra vuelta hasta que cae el sol. Sin prisas.",
      nav_gallery:"Galería",
      gal_eyebrow:"Galería",gal_title:"El coto en imágenes",
      ct_eyebrow:"Contacto",ct_title:'Cuéntanos y <em>preparamos tu jornada</em>',
      ct_p:"Contacta con nosotros y preparamos tu cacería a medida para ti o tu grupo.",
      ct_wa:"Escríbenos por WhatsApp",
      ct_f_name:"Nombre",ct_f_phone:"Teléfono",ct_f_email:"Email",ct_f_prey:"Qué quieres cazar",ct_f_dates:"Fechas aproximadas",ct_f_msg:"Mensaje",
      opt_conejo:"Conejo",opt_zorzal:"Zorzal",opt_perdiz:"Perdiz",opt_mixto:"Mixto",
      ct_send:"Enviar solicitud →",ct_note:"Te responderemos lo antes posible. No compartimos tus datos.",
      ct_ok:"¡Gracias! Hemos recibido tu solicitud. Te contestamos enseguida.",
      nav_packs:"Tarifas",
      pk_eyebrow:"Tarifas",pk_title:"Packs de caza",pk_sub:"Cada jornada se adapta al grupo y a las fechas. Dinos qué buscas y te pasamos precio.",
      pk_acc:"El coto dispone de alojamiento en el centro del propio cazadero a 5 minutos.",
      pk_pop:"El más popular",pk_cta:"Pide precio →",
      pk1_tier:"Un día",pk1_name:"Jornada de caza",pk1_dur:"Ideal para una escapada",
      pk1_l1:"Guía que conoce el terreno",pk1_l2:"Acceso a las +3.000 ha del coto",pk1_l3:"Conejo, perdiz o zorzal según la fecha",
      pk2_tier:"2–3 días",pk2_name:"Escapada de fin de semana",pk2_dur:"Caza, alojamiento y buena mesa",
      pk2_l1:"Varias jornadas guiadas",pk2_l2:"Alojamiento y pensión completa",pk2_l3:"Sitio para los perros y el material",pk2_l4:"Te echamos una mano con licencia y seguro",
      pk3_tier:"5–6 días",pk3_name:"Semana de zorzal",pk3_dur:"En plena migración de otoño",
      pk3_l1:"Los mejores días del paso",pk3_l2:"Pensión completa y alojamiento",pk3_l3:"Pensado para grupos de cazadores",pk3_l4:"El pack estrella para los franceses",
      pk4_tier:"Temporada",pk4_name:"Tarjeta de temporada",pk4_dur:"3 días a la semana",
      pk4_l1:"Caza jueves, sábados, domingos y festivos",pk4_l2:"Acceso regular durante toda la temporada",pk4_l3:"Ideal para el cazador habitual",
      pk5_tier:"A medida",pk5_name:"Pase de día",pk5_dur:"Días sueltos",
      pk5_l1:"Caza en nuestra área privada",pk5_l2:"Precio variable según las especies a cazar",pk5_l3:"Flexibilidad total para tu escapada",
      foot:"Coto privado de caza menor · Temporada 2025–2026"},
    fr:{nav_where:"Le territoire",nav_species:"La chasse",nav_contact:"Contact",
      hero_eyebrow:"Réserve privée · Petit gibier",
      hero_title:'Découvrez la meilleure zone<br>de chasse de <em>Catalogne</em><span class="place">Les Garrigues, Lérida</span>',
      hero_sub:"Plus de 3 000 hectares de garrigue, de pinèdes et de cultures : le lapin règne toute l'année et, à l'automne, arrive la grive. Une chasse traditionnelle, à votre rythme.",
      hero_cta1:"Demandez votre séjour →",hero_cta2:"Découvrir le territoire",scroll:"Défiler",
      where_eyebrow:"Où nous trouver",where_title:"Au cœur des Garrigues",
      where_p1:"Notre territoire se situe sur la commune de Granyena de les Garrigues. Une propriété privée de garrigue, de pinèdes et de champs cultivés.",
      where_ha_num:"+3 000",where_ha_txt:"hectares<br>de terrain privé",
      where_p2:"Facile d'accès : à deux pas des grandes villes, mais en pleine campagne.",
      map_title:"À deux pas",map_lead:"Temps en voiture",
      sp_title:"Ce que l'on chasse ici",sp_sub:"Les espèces cynégétiques les plus présentes chez nous.",
      sp_star:"Le roi",sp1_n:"Lapin",sp1_w:"Presque toute l'année",sp1_d:"Il s'est multiplié énormément ces cinq dernières années. Il y en a tellement qu'en été nous devons réguler la population pour éviter les dégâts dans les cultures.",
      sp2_n:"Grive",sp2_w:"Oct · Fév",sp2_d:"Oiseau migrateur qui arrive chaque automne pour les olives. Lleida est en plein couloir de passage : quand elles entrent, c'est par milliers. C'est ce qui fait le plus rêver le chasseur français.",
      sp3_n:"Perdrix rouge",sp3_w:"Oct · Jan",sp3_d:"La perdrix rouge sauvage se fait rare dans notre région, mais chaque saison nous effectuons quelques lâchers pour renforcer sa présence sur notre territoire.",
      sp4_n:"Pigeon colombin et ramier",sp4_w:"Passages de saison",sp4_d:"Ces espèces sont de plus en plus présentes tout au long de l'année, leur période optimale étant la demi-saison en été.",
      sp5_n:"Bécasse",sp5_w:"Période de neige",sp5_d:"La bécasse est de plus en plus fréquente sur notre territoire, étant un oiseau migrateur qui nous rend visite pendant les périodes les plus froides en Europe, fuyant les fortes chutes de neige qui l'empêchent de manger des vers de terre avec son long bec.",
      jor_eyebrow:"Une journée sur le territoire",jor_title:"Comment on chasse ici",
      jor_p:"On part tôt, alors que le givre couvre encore les oliviers. Un guide qui connaît le terrain par cœur vous mène aux meilleurs postes. En milieu de matinée, une pause pour casser la croûte. L'après-midi, une nouvelle sortie jusqu'au coucher du soleil. Sans précipitation.",
      nav_gallery:"Galerie",
      gal_eyebrow:"Galerie",gal_title:"Le territoire en images",
      ct_eyebrow:"Contact",ct_title:'Écrivez-nous et <em>on prépare votre séjour</em>',
      ct_p:"Contactez-nous et nous préparerons une chasse sur mesure pour vous ou votre groupe.",
      ct_wa:"Écrivez-nous sur WhatsApp",
      ct_f_name:"Nom",ct_f_phone:"Téléphone",ct_f_email:"Email",ct_f_prey:"Que voulez-vous chasser",ct_f_dates:"Dates approximatives",ct_f_msg:"Message",
      opt_conejo:"Lapin",opt_zorzal:"Grive",opt_perdiz:"Perdrix",opt_mixto:"Mixte",
      ct_send:"Envoyer la demande →",ct_note:"Nous vous répondrons au plus vite. Vos données restent confidentielles.",
      ct_ok:"Merci ! Nous avons bien reçu votre demande. On revient vers vous très vite.",
      nav_packs:"Tarifs",
      pk_eyebrow:"Tarifs",pk_title:"Formules de chasse",pk_sub:"Chaque sortie s'adapte au groupe et aux dates. Dites-nous ce que vous cherchez et on vous fait un prix.",
      pk_acc:"Le domaine dispose d'un hébergement au centre même du territoire de chasse, à 5 minutes.",
      pk_pop:"Le plus demandé",pk_cta:"Demander le prix →",
      pk1_tier:"Une journée",pk1_name:"Journée de chasse",pk1_dur:"Idéale pour une échappée",
      pk1_l1:"Un guide qui connaît le terrain",pk1_l2:"Accès aux +3 000 ha du territoire",pk1_l3:"Lapin, perdrix ou grive selon la date",
      pk2_tier:"2–3 jours",pk2_name:"Week-end de chasse",pk2_dur:"Chasse, logement et bonne table",
      pk2_l1:"Plusieurs sorties guidées",pk2_l2:"Logement et pension complète",pk2_l3:"De la place pour les chiens et le matériel",pk2_l4:"On vous aide pour le permis et l'assurance",
      pk3_tier:"5–6 jours",pk3_name:"Semaine de la grive",pk3_dur:"En pleine migration d'automne",
      pk3_l1:"Les meilleurs jours du passage",pk3_l2:"Pension complète et logement",pk3_l3:"Pensé pour les groupes de chasseurs",pk3_l4:"La formule phare pour les Français",
      pk4_tier:"Saison",pk4_name:"Carte de saison",pk4_dur:"3 jours par semaine",
      pk4_l1:"Chasse les jeudis, samedis, dimanches et jours fériés",pk4_l2:"Accès régulier pendant toute la saison",pk4_l3:"Idéal pour le chasseur régulier",
      pk5_tier:"Sur mesure",pk5_name:"Pass journalier",pk5_dur:"Jours isolés",
      pk5_l1:"Chassez dans notre domaine privé",pk5_l2:"Prix variable selon les espèces",pk5_l3:"Flexibilité totale pour votre séjour",
      foot:"Réserve privée de petit gibier · Saison 2025–2026"},
    en:{nav_where:"The estate",nav_species:"The hunt",nav_contact:"Contact",
      hero_eyebrow:"Private estate · Small game",
      hero_title:'Discover the finest<br>small-game hunting in <em>Catalonia</em><span class="place">Les Garrigues, Lleida</span>',
      hero_sub:"Over 3,000 hectares of scrubland, pine woods and farmland: rabbit all year round and thrush in autumn. Traditional hunting, at your own pace.",
      hero_cta1:"Request your stay →",hero_cta2:"Explore the estate",scroll:"Scroll",
      where_eyebrow:"Where we are",where_title:"In the heart of Les Garrigues",
      where_p1:"Our estate sits in Granyena de les Garrigues. A private ground of scrubland, pine woods and farmland.",
      where_ha_num:"+3,000",where_ha_txt:"hectares<br>of private land",
      where_p2:"Easy to reach: a short drive from the big cities, yet surrounded by real countryside.",
      map_title:"A stone's throw away",map_lead:"By car",
      sp_title:"What you'll hunt here",sp_sub:"The game species you'll most often find in our area.",
      sp_star:"The king",sp1_n:"Rabbit",sp1_w:"Almost all year",sp1_d:"It has boomed over the last five years. There's so much of it that in summer we have to thin the population to keep it from damaging the crops.",
      sp2_n:"Thrush",sp2_w:"Oct · Feb",sp2_d:"A migratory bird that arrives every autumn for the olives. Lleida sits right on the migration route, so when they come in, they come in their thousands. It's what French hunters look forward to most.",
      sp3_n:"Red partridge",sp3_w:"Oct · Jan",sp3_d:"Wild red partridge is quite scarce in our area, but every season we carry out a few releases to reinforce its presence on our land.",
      sp4_n:"Stock dove & wood pigeon",sp4_w:"Seasonal passage",sp4_d:"These species are increasingly present all year round, being at their best during the summer half-season.",
      sp5_n:"Woodcock",sp5_w:"Snow season",sp5_d:"The woodcock is increasingly frequent in our territory. It is a migratory bird that visits us during the coldest periods in Europe, fleeing from heavy snowfalls that prevent it from eating earthworms with its long beak.",
      jor_eyebrow:"A day on the estate",jor_title:"What hunting here feels like",
      jor_p:"You set out early, frost still on the olive trees. A guide who knows the ground inside out takes you to the best spots. Mid-morning, a break to eat. In the afternoon, another round until the sun goes down. No rush.",
      nav_gallery:"Gallery",
      gal_eyebrow:"Gallery",gal_title:"The estate in pictures",
      ct_eyebrow:"Contact",ct_title:'Tell us and <em>we\\'ll plan your day</em>',
      ct_p:"Contact us and we will prepare a tailor-made hunting experience for you or your group.",
      ct_wa:"Message us on WhatsApp",
      ct_f_name:"Name",ct_f_phone:"Phone",ct_f_email:"Email",ct_f_prey:"What you want to hunt",ct_f_dates:"Approximate dates",ct_f_msg:"Message",
      opt_conejo:"Rabbit",opt_zorzal:"Thrush",opt_perdiz:"Partridge",opt_mixto:"Mixed",
      ct_send:"Send request →",ct_note:"We'll reply as soon as we can. We never share your data.",
      ct_ok:"Thanks! We've received your request and will get back to you shortly.",
      nav_packs:"Rates",
      pk_eyebrow:"Rates",pk_title:"Hunting packages",pk_sub:"Every outing is tailored to your group and dates. Tell us what you're after and we'll quote you.",
      pk_acc:"The estate offers accommodation right in the center of the hunting ground, just 5 minutes away.",
      pk_pop:"Most popular",pk_cta:"Get a price →",
      pk1_tier:"One day",pk1_name:"Day hunt",pk1_dur:"Great for a quick escape",
      pk1_l1:"A guide who knows the ground",pk1_l2:"Access to the 3,000+ ha estate",pk1_l3:"Rabbit, partridge or thrush by season",
      pk2_tier:"2–3 days",pk2_name:"Weekend escape",pk2_dur:"Hunting, lodging and good food",
      pk2_l1:"Several guided outings",pk2_l2:"Lodging and full board",pk2_l3:"Room for the dogs and the gear",pk2_l4:"We help with the licence and insurance",
      pk3_tier:"5–6 days",pk3_name:"Thrush week",pk3_dur:"At the peak of the autumn migration",
      pk3_l1:"The best days of the passage",pk3_l2:"Full board and lodging",pk3_l3:"Made for groups of hunters",pk3_l4:"The flagship package for French hunters",
      pk4_tier:"Season",pk4_name:"Season Card",pk4_dur:"3 days a week",
      pk4_l1:"Hunt on Thursdays, Saturdays, Sundays and holidays",pk4_l2:"Regular access throughout the season",pk4_l3:"Ideal for the regular hunter",
      pk5_tier:"Custom",pk5_name:"Day Pass",pk5_dur:"Single days",
      pk5_l1:"Hunt in our private area",pk5_l2:"Price varies depending on the species",pk5_l3:"Total flexibility for your getaway",
      foot:"Private small-game estate · 2025–2026 season"},
    it:{nav_where:"La riserva",nav_species:"La caccia",nav_contact:"Contatti",
      hero_eyebrow:"Riserva privata · Piccola selvaggina",
      hero_title:'Scopri la migliore zona<br>di caccia in <em>Catalogna</em><span class="place">Les Garrigues, Lleida</span>',
      hero_sub:"Oltre 3.000 ettari di macchia, pinete e coltivazioni: il coniglio regna tutto l'anno e, in autunno, arriva il tordo. Caccia tradizionale, al tuo ritmo.",
      hero_cta1:"Richiedi la tua giornata →",hero_cta2:"Scopri la riserva",scroll:"Scorri",
      where_eyebrow:"Dove siamo",where_title:"Nel cuore delle Garrigues",
      where_p1:"La nostra riserva si trova nel comune di Granyena de les Garrigues. Una tenuta privata di macchia, pinete e campi coltivati.",
      where_ha_num:"+3.000",where_ha_txt:"ettari<br>di terreno privato",
      where_p2:"Facile da raggiungere: a un passo dalle grandi città, ma immersi nella vera campagna.",
      map_title:"A due passi",map_lead:"Tempo in auto",
      sp_title:"Cosa si caccia qui",sp_sub:"Le specie venatorie più comuni nella nostra zona.",
      sp_star:"Il re",sp1_n:"Coniglio",sp1_w:"Quasi tutto l'anno",sp1_d:"Negli ultimi cinque anni si è moltiplicato tantissimo. C'è così tanto coniglio che in estate dobbiamo fare abbattimenti per evitare danni all'agricoltura.",
      sp2_n:"Tordo",sp2_w:"Ott · Feb",sp2_d:"Uccello migratore che arriva ogni autunno in cerca di olive. Lleida si trova in piena rotta migratoria, quindi quando entrano lo fanno a migliaia. È ciò che più fa sognare il cacciatore francese.",
      sp3_n:"Pernice rossa",sp3_w:"Ott · Gen",sp3_d:"La pernice rossa selvatica è molto scarsa nella nostra zona, ma ogni stagione effettuiamo alcuni rilasci per rafforzare la sua presenza nel nostro terreno.",
      sp4_n:"Colombella e colombaccio",sp4_w:"Passi stagionali",sp4_d:"Queste specie sono sempre più presenti tutto l'anno, con il loro momento ottimale nella mezza stagione in estate.",
      sp5_n:"Beccaccia",sp5_w:"Tempo di nevicate",sp5_d:"La beccaccia è sempre più frequente nel nostro territorio. È un uccello migratore che durante i periodi più freddi in Europa ci visita fuggendo dalle forti nevicate che le impediscono di mangiare lombrichi con il suo lungo becco.",
      jor_eyebrow:"Una giornata nella riserva",jor_title:"Com'è cacciare qui",
      jor_p:"Si esce presto, con la brina ancora sugli ulivi. Una guida che conosce il terreno palmo a palmo ti porta nelle migliori postazioni. A metà mattinata, una pausa per pranzare. Nel pomeriggio, un altro giro fino al tramonto. Senza fretta.",
      nav_gallery:"Galleria",
      gal_eyebrow:"Galleria",gal_title:"La riserva in immagini",
      ct_eyebrow:"Contatti",ct_title:'Scrivici e <em>prepariamo la tua giornata</em>',
      ct_p:"Contattaci e prepariamo la tua caccia su misura per te o per il tuo gruppo.",
      ct_wa:"Scrivici su WhatsApp",
      ct_f_name:"Nome",ct_f_phone:"Telefono",ct_f_email:"Email",ct_f_prey:"Cosa vuoi cacciare",ct_f_dates:"Date approssimative",ct_f_msg:"Messaggio",
      opt_conejo:"Coniglio",opt_zorzal:"Tordo",opt_perdiz:"Pernice",opt_mixto:"Misto",
      ct_send:"Invia richiesta →",ct_note:"Ti risponderemo il prima possibile. Non condividiamo i tuoi dati.",
      ct_ok:"Grazie! Abbiamo ricevuto la tua richiesta. Ti risponderemo a breve.",
      nav_packs:"Tariffe",
      pk_eyebrow:"Tariffe",pk_title:"Pacchetti di caccia",pk_sub:"Ogni giornata si adatta al gruppo e alle date. Dicci cosa cerchi e ti forniremo il prezzo.",
      pk_acc:"La riserva dispone di alloggi nel centro della stessa zona di caccia, a soli 5 minuti.",
      pk_pop:"Il più popolare",pk_cta:"Richiedi prezzo →",
      pk1_tier:"Un giorno",pk1_name:"Giornata di caccia",pk1_dur:"Ideale per una fuga",
      pk1_l1:"Guida che conosce il terreno",pk1_l2:"Accesso ai +3.000 ha della riserva",pk1_l3:"Coniglio, pernice o tordo a seconda del periodo",
      pk2_tier:"2–3 giorni",pk2_name:"Fuga di fine settimana",pk2_dur:"Caccia, alloggio e buona cucina",
      pk2_l1:"Diverse giornate guidate",pk2_l2:"Alloggio e pensione completa",pk2_l3:"Spazio per i cani e l'attrezzatura",pk2_l4:"Ti aiutiamo con licenza e assicurazione",
      pk3_tier:"5–6 giorni",pk3_name:"Settimana del tordo",pk3_dur:"In piena migrazione autunnale",
      pk3_l1:"I migliori giorni di passo",pk3_l2:"Pensione completa e alloggio",pk3_l3:"Pensato per gruppi di cacciatori",pk3_l4:"Il pacchetto di punta per i francesi",
      pk4_tier:"Stagione",pk4_name:"Tessera stagionale",pk4_dur:"3 giorni a settimana",
      pk4_l1:"Caccia il giovedì, sabato, domenica e festivi",pk4_l2:"Accesso costante durante la stagione",pk4_l3:"Ideale per i cacciatori più assidui",
      pk5_tier:"Su misura",pk5_name:"Pass giornaliero",pk5_dur:"Giornate singole",
      pk5_l1:"Caccia nella nostra area privata",pk5_l2:"Prezzo variabile a seconda delle specie",pk5_l3:"Massima flessibilità",
      foot:"Riserva privata di piccola selvaggina · Stagione 2025–2026"}
  };"""

content = re.sub(t_pattern, new_t, content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated index.html")
