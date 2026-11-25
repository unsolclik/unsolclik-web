// Galeries privades per triar fotos. Cada família té un codi difícil d'endevinar.
// Enllaç per enviar: https://unsolclik.github.io/unsolclik-web/tria.html#CODI
// Per afegir-ne una: python3 tools/nova-familia.py "Nom" carpeta-amb-fotos
window.TRIA_CONFIG = {
  whatsapp: "34639234492",
  pick: 20,          // fotos incloses al pack
  extra: 2,          // € per foto extra
  all: 20,           // € per quedar-se totes les de la galeria
  days: 5            // dies per triar
};

window.FAMILIES = {
  "demo": {
    name: "Família Demo",
    pick: 6,
    deadline: "2026-12-31",
    folder: "fotos/jb",
    photos: ["jb-01.jpg","jb-02.jpg","jb-03.jpg","jb-04.jpg","jb-05.jpg","jb-06.jpg","jb-07.jpg","jb-08.jpg","jb-09.jpg","jb-10.jpg","jb-11.jpg","jb-12.jpg","jb-13.jpg"]
  }
  // NOVES FAMÍLIES A SOTA
};
