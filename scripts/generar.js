const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer-core");

const ROOT = "/vercel/share/v0-project";
const TEMPLATE = path.join(ROOT, "autorizacion-caza-conejo.html");
const LOGO = path.join(ROOT, "images", "logo-cazalleida-sm.png");
const OUTDIR = path.join(ROOT, "pdfs");
const CHROME =
  process.env.HOME + "/.agent-browser/browsers/chrome-150.0.7871.46/chrome";

const CAZADORES = [
  [1, "Benito Gili Florensa", "40898319H"],
  [2, "Juan Francisco de la Cruz Sanchez Plana", "40876029S"],
  [3, "Ferran Galcerà Solé", "47936701-D"],
  [4, "Miquel Galcerà Altés", "78575149-L"],
  [5, "Enric Cabré Solá", "40834218H"],
  [6, "Antonio Sunalla Raimat", "40838458A"],
  [7, "Jordi Sans Pascuet", "40841054T"],
  [8, "Josep Cots Pelegri", "40847530J"],
  [9, "Francisco Zarza Garcia", "39699060W"],
  [10, "Victor Manuel Zarza Garcia", "39699767L"],
  [11, "Yeray Zarza Callejón", "49316079P"],
  [12, "Miquel Angel Rodriguez", "46719456Q"],
  [13, "Miquel Jaldo Pelegrino", "46518981D"],
  [14, "Miquel Jaldo Delpino", "49288378E"],
  [15, "Jesus Jaldo Pelegrina", "46537187E"],
  [16, "Emilio Useno Castno", "37323935H"],
  [17, "Jose Bernal Marnenda", "43500907-H"],
  [18, "Abel Bernal Galvez", "53033535C"],
  [19, "Diego Jose Galena Quisano", "39473017-A"],
  [20, "José A. Galcera Gea", "39728517L"],
  [21, "Juan Antonio Fdez. Suarez", "39675622R"],
  [22, "Sebastian Hervás Soriano", "39854673C"],
  [23, "Adrian Fdez Izquierdo", "49647703H"],
  [24, "Llorenç Ruiz Sala", "34758374S"],
  [25, "Jose A. Rodriguez Sanchez", "43499011P"],
  [26, "Juan Corominas de Dios", "77260203Y"],
  [27, "Inga Ermolova", "47918378V"],
  [28, "Manuel Castillo Lopez", "4498318P"],
  [29, "Carlos Castillo Leon", "77795483F"],
  [30, "Joaquin Feixo Fannagoldo", "06643116"],
  [31, "Ramón Vidal Sabaté", "40880798T"],
  [32, "Jordi Vidal García", "39938597V"],
  [33, "Jorge Vidal Miró", "39874279F"],
  [34, "Josep María Reves", "78050679H"],
  [35, "Sergio Valera Guerrero", "39888316Z"],
  [36, "Iker Valera Gisbert", "39940528Q"],
  [37, "Juan Varela Ortiz", "25912415V"],
  [38, "Sebastian Altemir Riba", "53332504N"],
  [39, "Sebastia Ros Barbera", "40864924L"],
  [40, "Adriá Ros Pujol", "78089599E"],
  [41, "Francesc Sánchez Besora", "46723855E"],
];

function slug(txt) {
  return txt
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^A-Za-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function esc(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function buildTemplate() {
  let html = fs.readFileSync(TEMPLATE, "utf8");
  const b64 = fs.readFileSync(LOGO).toString("base64");
  html = html.replace(
    'src="images/logo-cazalleida.png"',
    `src="data:image/png;base64,${b64}"`
  );
  html = html.replace(
    '<div class="barra">',
    '<div class="barra" style="display:none">'
  );
  return html;
}

async function main() {
  const only = process.argv[2];
  fs.mkdirSync(OUTDIR, { recursive: true });
  const base = buildTemplate();
  const list = only === "test" ? CAZADORES.slice(0, 1) : CAZADORES;

  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: "shell",
    args: ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
  });
  const page = await browser.newPage();

  for (const [num, nombre, dni] of list) {
    let doc = base
      .replace(
        /(<span class="valor" data-field="nombre">)[^<]*(<\/span>)/,
        `$1${esc(nombre)}$2`
      )
      .replace(
        /(<span class="valor" data-field="dni">)[^<]*(<\/span>)/,
        `$1${esc(dni)}$2`
      );
    await page.setContent(doc, { waitUntil: "networkidle0" });
    const file = path.join(
      OUTDIR,
      `${String(num).padStart(2, "0")}-${slug(nombre)}.pdf`
    );
    await page.pdf({
      path: file,
      format: "A4",
      printBackground: true,
      margin: { top: "0", right: "0", bottom: "0", left: "0" },
    });
    console.log("OK", path.basename(file));
  }

  await browser.close();
  console.log("TOTAL", list.length);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
