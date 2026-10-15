/* Progressive enhancement: all module content and links exist without JS. */
'use strict';
const form = document.getElementById('filters');
if (form) {
  const search = document.getElementById('search');
  const kind = document.getElementById('kind');
  const availability = document.getElementById('availability');
  const modules = Array.from(document.querySelectorAll('.module'));
  const count = document.getElementById('count');
  const empty = document.getElementById('empty');
  const normalize = value => value.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase();
  const entries = modules.map(node => ({node, text: normalize(node.textContent)}));
  function update() {
    const words = normalize(search.value).trim().split(/\s+/).filter(Boolean);
    let visible = 0;
    for (const {node, text} of entries) {
      const match = words.every(word => text.includes(word)) && (!kind.value || node.dataset.kind === kind.value) && (!availability.value || node.dataset.availability === availability.value);
      node.hidden = !match;
      if (match) visible++;
    }
    count.textContent = `${visible} / ${modules.length} Module`;
    empty.hidden = visible !== 0;
  }
  form.hidden = false;
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('input', update);
  form.addEventListener('change', update);
  form.addEventListener('reset', () => { search.value = ''; kind.value = ''; availability.value = ''; update(); });
  update();
}
