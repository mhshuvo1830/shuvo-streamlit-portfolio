/* Your information and verified project links. Edit these values anytime. */
const PROFILE = {
  name: 'Md Mahamudul Hasan Shuvo',
  initials: 'MS',
  location: 'Dhaka, Bangladesh',
  email: 'mhshuvo2040@gmail.com',
  github: 'https://github.com/mhshuvo1830',
  facebook: 'https://www.facebook.com/m.h.Shuvo1830',
  linkedin: 'https://www.linkedin.com/in/md-mahamudul-hasan-shuvo-812a59266',
  bhumiguardCode: 'https://github.com/mhshuvo1830/BhumiGuard-BD',
  bhumiguardDemo: 'https://bhumiguard-bd.streamlit.app',
  pantryCode: 'https://github.com/mhshuvo1830/zero-waste-kitchenv2.0',
  routineDemo: 'https://diu-routine-b00ff.web.app',
  calculatorCode: 'https://github.com/mhshuvo1830/diu-fee-calculator'
};

// Populate your name, initials, location and university in the page.
document.querySelectorAll('[data-profile]').forEach((element) => {
  const key = element.dataset.profile;
  if (Object.prototype.hasOwnProperty.call(PROFILE, key)) {
    element.textContent = PROFILE[key];
  }
});
document.title = `${PROFILE.name} | Software Developer`;

const urlIsSafe = (value) => {
  try { const parsed = new URL(value); return ['https:', 'http:'].includes(parsed.protocol); }
  catch { return false; }
};

// Only show valid external links after they've been added to PROFILE.
document.querySelectorAll('[data-link]').forEach((link) => {
  const url = PROFILE[link.dataset.link];
  if (url && urlIsSafe(url)) {
    link.href = url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.hidden = false;
  }
});

// A mailto: link may do nothing inside an embedded Streamlit page when the
// visitor has no configured mail handler. Use Gmail's browser-based composer
// for the main CTA and give visitors a one-click copy fallback.
const emailButton = document.getElementById('email-button');
const footerEmailLink = document.getElementById('footer-email-link');
const contactEmailAddress = document.getElementById('contact-email-address');
const copyEmailButton = document.getElementById('copy-email-button');
const copyEmailFeedback = document.getElementById('copy-email-feedback');
const validEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(PROFILE.email);
if (validEmail) {
  const gmailComposeUrl = `https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(PROFILE.email)}&su=${encodeURIComponent('Hello from your portfolio')}`;
  emailButton.href = gmailComposeUrl;
  emailButton.target = '_blank';
  emailButton.rel = 'noopener noreferrer';
  emailButton.hidden = false;
  footerEmailLink.href = gmailComposeUrl;
  contactEmailAddress.textContent = PROFILE.email;
}

copyEmailButton.addEventListener('click', async () => {
  if (!validEmail) return;
  let copied = false;
  // Clipboard API can be blocked by iframe permissions. Fall back to a
  // temporary selection, then give visitors text they can copy manually.
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(PROFILE.email);
      copied = true;
    }
  } catch (_) { /* try the fallback */ }
  if (!copied) {
    const field = document.createElement('textarea');
    field.value = PROFILE.email;
    field.setAttribute('readonly', '');
    field.style.position = 'fixed';
    field.style.opacity = '0';
    field.style.left = '-9999px';
    document.body.appendChild(field);
    field.select();
    try { copied = document.execCommand('copy'); } catch (_) {}
    field.remove();
  }
  copyEmailFeedback.textContent = copied ? 'Copied!' : `Select and copy: ${PROFILE.email}`;
});

document.getElementById('current-year').textContent = new Date().getFullYear();

// Light / dark theme. Remembers the visitor's choice.
const root = document.documentElement;
const themeButton = document.querySelector('.theme-toggle');
let storedTheme = null;
try { storedTheme = localStorage.getItem('portfolio-theme'); } catch (_) {}
const initialTheme = storedTheme === 'light' || storedTheme === 'dark'
  ? storedTheme
  : window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
root.dataset.theme = initialTheme;
const updateThemeLabel = () => {
  themeButton.setAttribute('aria-label', root.dataset.theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
};
updateThemeLabel();
themeButton.addEventListener('click', () => {
  root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
  updateThemeLabel();
  try { localStorage.setItem('portfolio-theme', root.dataset.theme); } catch (_) {}
});

// Mobile navigation menu.
const menuToggle = document.querySelector('.mobile-menu-toggle');
const mobileNav = document.getElementById('mobile-nav');
const setMenuOpen = (isOpen) => {
  mobileNav.hidden = !isOpen;
  menuToggle.setAttribute('aria-expanded', String(isOpen));
  menuToggle.setAttribute('aria-label', isOpen ? 'Close navigation menu' : 'Open navigation menu');
};
menuToggle.addEventListener('click', () => setMenuOpen(mobileNav.hidden));
mobileNav.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setMenuOpen(false)));
window.addEventListener('resize', () => { if (window.innerWidth > 830) setMenuOpen(false); });

// Fix anchor navigation inside Streamlit's srcdoc iframe.
// A bare href="#about" may resolve against the parent Streamlit app URL,
// navigating the iframe away from the portfolio rather than scrolling it.
// Explicitly scroll to the section within THIS document, without reloading.
document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener('click', (event) => {
    const anchor = link.getAttribute('href').slice(1);
    if (!anchor) return;
    const target = document.getElementById(anchor);
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});
