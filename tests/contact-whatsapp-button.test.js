const assert = require('node:assert/strict');
const fs = require('node:fs');

const contactPage = fs.readFileSync('contato/index.html', 'utf8');
const contactForm = contactPage.match(/<form class="elementor-form" method="post" id="contato"[\s\S]*?<\/form>/);

assert.ok(contactForm, 'the Fale Conosco form must exist');
assert.match(contactForm[0], /<button type="submit"[\s\S]*?elementor-button-text">Enviar/, 'the normal form submit button must remain');
assert.match(contactForm[0], /id="contato-whatsapp"/, 'the Fale Conosco form must include a WhatsApp button');
assert.match(contactForm[0], /href="https:\/\/api\.whatsapp\.com\/send\?phone=551938341741"/, 'the WhatsApp button must use Inda Fire’s WhatsApp number');
assert.match(contactForm[0], /<span class="elementor-button-text">WhatsApp<\/span>/, 'the second button must be labelled WhatsApp');
assert.match(contactPage, /form-field-mensagem/, 'the page must compose a WhatsApp message from form fields');
assert.match(contactPage, /phone=551938341741&text=/, 'the page must pass the composed message to WhatsApp');

console.log('Contact WhatsApp button regression test passed.');
