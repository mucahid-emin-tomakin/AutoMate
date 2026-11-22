// Mücahid Emin Tomakin - https://mucahid-emin-tomakin.vercel.app/
// DeepForge - https://github.com/mucahid-emin-tomakin/AutoMate/tree/main/ChromeExtension/DeepForge/
// content.js

// ============================================================================
// 1. KONFIGURATION, DEBUG & UTILS
// ============================================================================
const DF_DEBUG = true;
const PDF_PAGE_TIMEOUT_MS = 60000;
const PDF_PAGE_SETTLE_MS = 850;
const PDF_DISCOVERY_MAX_MS = 120000;
const PDF_DISCOVERY_STABLE_MS = 6500;
const BEFOREPRINT_DELAY_MS = 1500;
const DIAGRAM_READY_TIMEOUT_MS = 30000;
const AFTERPRINT_DELAY_MS = 500;
const TOAST_DURATION_ERROR_MS = 6000;
const TOAST_DURATION_WARNING_MS = 4000;
const TOC_MAX_LABEL_LENGTH = 60;
const NON_CAPTURABLE_EXTENSIONS = new Set([
  'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg', 'bmp', 'ico', 'tif', 'tiff',
  'mp3', 'mp4', 'wav', 'ogg', 'mov', 'avi', 'mkv', 'webm', 'flac',
  'zip', 'rar', '7z', 'tar', 'gz',
  'docx', 'xlsx', 'pptx', 'doc', 'xls', 'ppt', 'odt', 'ods', 'odp' ]);
const DF_SELECTORS = {
  message: '.ds-message',
  userQuestion: '.fbb737a4',
  aiMarkdown: '.ds-message .ds-markdown:not(.ds-think-content .ds-markdown)',
  cotContainer: '.ds-message .ds-think-content',
  attachmentName: '.e70accd6',
  attachmentSize: '.dc832104',
  attachmentCard: '._25c7358.dafb6286, ._25c7358, .dafb6286',
  pdfPage: '.react-pdf__Page',
  pdfCanvas: '.react-pdf__Page__canvas',
  codeBlock: '.md-code-block',
  codeLang: '.d813de27',
  sourceBlock: '.f93f59e4',
  chatTitle: '.f8d1e4c0 .afa34042, .f8d1e4c0' };
const SETTINGS_DEFAULTS = {
  autoExport: false,
  notifyNewMessages: true,
  exportWebReferences: true };
function dfLog(...args) {
  if (DF_DEBUG) console.log('[DeepForge] ', ...args); }
function dfWarn(message, ...rest) {
  if (DF_DEBUG) console.warn('[DeepForge-Warning] ', message, ...rest);
  if (typeof message === 'string') showToast('warning', message); }
function dfError(message, ...rest) {
  if (DF_DEBUG) console.error('[DeepForge-Error] ', message, ...rest);
  if (typeof message === 'string') showToast('error', message); }
function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms)); }
function sanitizeFilename(str) {
  return String(str ?? '').replace(/[/\\?%*:|"<>]/g, '-'); }
function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;'); }
function isDeepSeekChatPage() {
  return window.location.hostname === 'chat.deepseek.com'; }
function isExtensionContextValid() {
  try {
    return Boolean(chrome?.runtime?.id); } 
    catch {
    return false; } }
async function getSettings() {
  if (!isExtensionContextValid()) {
    dfLog('getSettings: Extension-Kontext ungültig, nutze Standard-Einstellungen.');
    return { ...SETTINGS_DEFAULTS }; }
  try {
    if (chrome?.storage?.sync) {
      const stored = await chrome.storage.sync.get(SETTINGS_DEFAULTS);
      dfLog('getSettings: Einstellungen aus chrome.storage.sync geladen.', stored);
      return { ...SETTINGS_DEFAULTS, ...stored }; } } 
    catch (e) {
    dfWarn('Fallback auf Standard-Einstellungen:', e); }
  dfLog('getSettings: Nutze Standard-Einstellungen.');
  return { ...SETTINGS_DEFAULTS }; }
// ============================================================================
// 2. UI FEEDBACK (TOAST & LOADING OVERLAY)
// ============================================================================
let dfToastContainer = null;
const DF_RAINBOW_GRADIENT =
  '#ff0055, #ff8800, #ffdd00, #00ff88, #00ddff, #8800ff, #ff00cc, #ff0055';
function clearToasts() {
  const existing = document.querySelectorAll('#df-toast-container, [id^="df-toast"], [class*="df-toast"]');
  dfLog('clearToasts:', { removedCount: existing.length, hadContainer: Boolean(dfToastContainer) });
  existing.forEach((el) => el.remove());
  dfToastContainer = null; }
function showToast(type, message) {
  if (!document.body) {
    dfWarn('showToast abgebrochen: document.body nicht verfügbar.', { type, message });
    return; }
  if (!dfToastContainer || !document.body.contains(dfToastContainer)) {
    dfToastContainer = document.createElement('div');
    dfToastContainer.id = 'df-toast-container';
    dfToastContainer.style.cssText = `
      position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
      z-index: 2147483647; display: flex; flex-direction: column;
      align-items: center; gap: 18px; pointer-events: none;`;
    document.body.appendChild(dfToastContainer);
    dfLog('showToast: dfToastContainer neu erstellt.'); }
  const icon = type === 'error' ? '❌' : '⚠️';
  const toast = document.createElement('div');
  toast.style.cssText = `
    position: relative; display: inline-flex; opacity: 0;
    transform: translateY(-20px) scale(0.85);
    transition: opacity 0.35s ease, transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    pointer-events: auto; cursor: pointer;`;
  const rainbow = document.createElement('div');
  rainbow.style.cssText = `
    position: absolute; inset: -11px; border-radius: 25px;
    background: conic-gradient(from var(--df-angle), ${DF_RAINBOW_GRADIENT});
    animation: df-rainbow-rotate 4s linear infinite;
    filter: url(#df-electric); z-index: -1; pointer-events: none;`;
  const inner = document.createElement('div');
  inner.style.cssText = `
    display: flex; align-items: center; justify-content: center; gap: 16px;
    padding: 14px 32px; background: #000000; border-radius: 14px;
    min-width: 260px; max-width: 500px;`;
  const makeIcon = () => {
    const span = document.createElement('span');
    span.textContent = icon;
    span.style.cssText = 'flex-shrink: 0; font-size: 22px; line-height: 1;';
    return span; };
  const text = document.createElement('span');
  text.textContent = message;
  text.style.cssText = `
    font-family: 'BlackChancery', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 20px; font-weight: 700;
    background: linear-gradient(90deg, ${DF_RAINBOW_GRADIENT});
    background-size: 200% 100%; -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: df-text-rainbow 4s linear infinite; text-align: center;
    line-height: 1.3; word-break: break-word; letter-spacing: 0.03em; flex: 1;
    filter: drop-shadow(0 1px 3px rgba(0,0,0,0.9)) drop-shadow(0 0 8px rgba(0,0,0,0.6));`;
  inner.append(makeIcon(), text, makeIcon());
  toast.append(rainbow, inner);
  dfToastContainer.appendChild(toast);
  dfLog('showToast angezeigt:', { type, message, containerChildren: dfToastContainer.children.length });
  requestAnimationFrame(() => {
    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0) scale(1)'; });
  let dismissed = false;
  let autoTimer = null;
  const dismiss = (reason = 'timeout') => {
    if (dismissed) return;
    dismissed = true;
    if (autoTimer) clearTimeout(autoTimer);
    dfLog('showToast ausgeblendet:', { type, message, reason });
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-20px) scale(0.85)';
    setTimeout(() => toast.remove(), 350); };
  toast.addEventListener('click', () => dismiss('click'));
  autoTimer = setTimeout(() => dismiss('timeout'), type === 'error' ? TOAST_DURATION_ERROR_MS : TOAST_DURATION_WARNING_MS); }
function showExportingOverlay(message) {
  if (document.getElementById('deepseek-export-loading')) {
    dfLog('showExportingOverlay: Overlay bereits vorhanden, aktualisiere Text.', message);
    updateExportingOverlay(message);
    return; }
  if (!document.body) {
    dfWarn('showExportingOverlay abgebrochen: document.body nicht verfügbar.', message);
    return; }
  const overlay = document.createElement('div');
  overlay.id = 'deepseek-export-loading';
  const box = document.createElement('div');
  box.className = 'deepseek-export-loading-box';
  const spinner = document.createElement('div');
  spinner.className = 'deepseek-export-loading-spinner';
  const text = document.createElement('div');
  text.className = 'deepseek-export-loading-text';
  text.id = 'deepseek-export-loading-text';
  text.textContent = message || 'Export wird vorbereitet';
  box.append(spinner, text);
  overlay.appendChild(box);
  document.body.appendChild(overlay);
  dfLog('showExportingOverlay erstellt:', text.textContent); }
function updateExportingOverlay(message) {
  const el = document.getElementById('deepseek-export-loading-text');
  if (el) {
    el.textContent = message;
    dfLog('updateExportingOverlay:', String(message ?? '').replace(/\s+/g, ' ').trim()); } 
    else {
    dfLog('updateExportingOverlay: Ziel-Element nicht gefunden.', message); } }
function hideExportingOverlay() {
  const overlay = document.getElementById('deepseek-export-loading');
  if (overlay) {
    overlay.remove();
    dfLog('hideExportingOverlay: Overlay entfernt.'); } 
    else {
    dfLog('hideExportingOverlay: Kein Overlay aktiv.'); } }
// ============================================================================
// 3. EXTENSION UI (SVG-FILTER & EXPORT-BUTTON)
// ============================================================================
const ELECTRIC_FILTER_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute;pointer-events:none;overflow:visible;">
  <defs>
    <filter id="df-electric" x="-50%" y="-50%" width="200%" height="200%" color-interpolation-filters="sRGB">
      <feTurbulence type="turbulence" baseFrequency="0.06" numOctaves="3" result="noise1" seed="1"/>
      <feOffset in="noise1" dx="0" dy="0" result="offsetNoise1">
        <animate attributeName="dy" values="60; 0" dur="1.4s" repeatCount="indefinite" calcMode="linear"/>
      </feOffset>
      <feTurbulence type="turbulence" baseFrequency="0.06" numOctaves="3" result="noise2" seed="1"/>
      <feOffset in="noise2" dx="0" dy="0" result="offsetNoise2">
        <animate attributeName="dy" values="0; -60" dur="1.4s" repeatCount="indefinite" calcMode="linear"/>
      </feOffset>
      <feTurbulence type="turbulence" baseFrequency="0.06" numOctaves="3" result="noise1" seed="2"/>
      <feOffset in="noise1" dx="0" dy="0" result="offsetNoise3">
        <animate attributeName="dx" values="60; 0" dur="1.4s" repeatCount="indefinite" calcMode="linear"/>
      </feOffset>
      <feTurbulence type="turbulence" baseFrequency="0.06" numOctaves="3" result="noise2" seed="2"/>
      <feOffset in="noise2" dx="0" dy="0" result="offsetNoise4">
        <animate attributeName="dx" values="0; -60" dur="1.4s" repeatCount="indefinite" calcMode="linear"/>
      </feOffset>
      <feComposite in="offsetNoise1" in2="offsetNoise2" result="part1"/>
      <feComposite in="offsetNoise3" in2="offsetNoise4" result="part2"/>
      <feBlend in="part1" in2="part2" mode="color-dodge" result="combinedNoise"/>
      <feDisplacementMap in="SourceGraphic" in2="combinedNoise" scale="30" xChannelSelector="R" yChannelSelector="B"/>
    </filter>
  </defs>
</svg>`;
function injectElectricFilters() {
  if (document.getElementById('deepforge-electric-filters')) {
    dfLog('injectElectricFilters: Bereits im DOM vorhanden.');
    return; }
  if (!document.body) {
    dfWarn('injectElectricFilters abgebrochen: document.body nicht verfügbar.');
    return; }
  const svgDoc = new DOMParser().parseFromString(ELECTRIC_FILTER_SVG, 'image/svg+xml');
  const parserError = svgDoc.querySelector('parsererror');
  if (parserError) {
    dfError('injectElectricFilters: SVG-Parserfehler.', parserError.textContent);
    return; }
  const svgEl = document.importNode(svgDoc.documentElement, true);
  svgEl.id = 'deepforge-electric-filters';
  document.body.appendChild(svgEl);
  dfLog('injectElectricFilters: SVG-Filter erfolgreich injiziert.'); }
function injectExportButton() {
  if (document.getElementById('deepseek-export-btn')) {
    dfLog('injectExportButton: Button bereits im DOM vorhanden.');
    return; }
  if (!document.body) {
    dfWarn('injectExportButton abgebrochen: document.body nicht verfügbar.');
    return; }
  const container = document.createElement('div');
  container.id = 'deepseek-export-container';
  container.className = 'deepseek-export-container';
  const exportButton = document.createElement('button');
  exportButton.id = 'deepseek-export-btn';
  exportButton.className = 'deepseek-export-btn';
  exportButton.type = 'button';
  ['df-sheet-1', 'df-sheet-2', 'df-sheet-3'].forEach((cls) => {
    const sheet = document.createElement('span');
    sheet.className = `df-sheet ${cls}`;
    exportButton.appendChild(sheet); });
  const buttonText = document.createElement('span');
  buttonText.textContent = 'Export Chat As';
  const arrowIcon = document.createElement('span');
  arrowIcon.className = 'arrow-icon';
  arrowIcon.textContent = '⮟';
  exportButton.append(buttonText, arrowIcon);
  const dropdownMenu = document.createElement('div');
  dropdownMenu.id = 'deepseek-export-dropdown';
  dropdownMenu.className = 'deepseek-export-dropdown';
  dropdownMenu.style.display = 'none';
  const setDropdownOpen = (open, reason = 'toggle') => {
    dropdownMenu.style.display = open ? 'block' : 'none';
    arrowIcon.style.transform = open ? 'rotate(180deg)' : 'rotate(0deg)';
    dfLog('Export-Dropdown Status geändert:', { open, reason }); };
  const options = [
    { label: 'JSON', format: 'json' },
    { label: 'MD', format: 'markdown' },
    { label: 'TXT', format: 'text' },
    { label: 'HTML', format: 'html' } ];
  options.forEach(({ label, format }) => {
    const option = document.createElement('div');
    option.className = 'deepseek-export-option';
    option.tabIndex = 0;
    const textSpan = document.createElement('span');
    textSpan.className = 'option-text';
    textSpan.textContent = label;
    option.appendChild(textSpan);
    const triggerExport = (e) => {
      e.preventDefault();
      e.stopPropagation();
      dfLog('Export-Option ausgewählt:', { label, format });
      setDropdownOpen(false, `option:${format}`);
      exportChat(format); };
    option.addEventListener('click', triggerExport);
    option.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') triggerExport(e); });
    dropdownMenu.appendChild(option); });
  exportButton.addEventListener('click', (e) => {
    e.stopPropagation();
    setDropdownOpen(dropdownMenu.style.display !== 'block', 'button-click'); });
  dropdownMenu.addEventListener('click', (e) => e.stopPropagation());
  if (!document.documentElement.dataset.dfOutsideClickAttached) {
    document.documentElement.dataset.dfOutsideClickAttached = '1';
    document.addEventListener('click', () => {
      const menu = document.getElementById('deepseek-export-dropdown');
      const arrow = document.querySelector('#deepseek-export-btn .arrow-icon');
      if (menu && menu.style.display === 'block') {
        menu.style.display = 'none';
        if (arrow) arrow.style.transform = 'rotate(0deg)';
        dfLog('Export-Dropdown Status geändert:', { open: false, reason: 'outside-click' }); } }); }
  const btnWrapper = document.createElement('div');
  btnWrapper.className = 'df-btn-wrapper';
  const rainbowBg = document.createElement('div');
  rainbowBg.className = 'df-rainbow-bg';
  btnWrapper.append(rainbowBg, exportButton);
  container.append(btnWrapper, dropdownMenu);
  document.body.appendChild(container);
  dfLog('injectExportButton: Export-Button und Dropdown erfolgreich injiziert.');
  addExportStyles(); }
function addExportStyles() {
  if (document.getElementById('deepseek-export-styles')) {
    dfLog('addExportStyles: Stylesheet bereits eingebunden.');
    return; }
  if (!isExtensionContextValid()) {
    dfWarn('addExportStyles abgebrochen: Extension-Kontext ungültig.');
    return; }
  const head = document.head || document.documentElement;
  if (!head) {
    dfWarn('addExportStyles abgebrochen: Kein <head> gefunden.');
    return; }
  const href = chrome.runtime.getURL('styles.css');
  const link = document.createElement('link');
  link.id = 'deepseek-export-styles';
  link.rel = 'stylesheet';
  link.type = 'text/css';
  link.href = href;
  link.addEventListener('load', () => dfLog('addExportStyles: styles.css erfolgreich geladen.', href));
  link.addEventListener('error', (err) => dfWarn('addExportStyles: Fehler beim Laden von styles.css.', { href, err }));
  head.appendChild(link);
  dfLog('addExportStyles: <link> für styles.css eingefügt.', href); }
// ============================================================================
// 4. DIAGRAMM-VORBEREITUNG (MERMAID / CODE-TABS)
// ============================================================================
const MERMAID_KEYWORD_RE =
  /(^|\n)\s*(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram(?:-v2)?|erDiagram|journey|gantt|pie|mindmap|timeline|quadrantChart|gitGraph)\b/i;
function isTabSelected(tab) {
  if (!(tab instanceof HTMLElement)) return false;
  return tab.getAttribute('aria-selected') === 'true' || tab.classList.contains('ds-segmented-button--selected'); }
function isDiagramCodeBlock(block) {
  if (!(block instanceof HTMLElement)) return false;
  const tabText = (block.querySelector('[role="tablist"]')?.textContent || '').trim();
  if (/diagram|mermaid/i.test(tabText)) return true;
  if (block.querySelector('svg.mermaid-svg, .mermaid-svg')) return true;
  const preText = (block.querySelector('pre')?.textContent || '').trim();
  return MERMAID_KEYWORD_RE.test(preText); }
function getDiagramBlocks(root = document) {
  return Array.from(root.querySelectorAll(DF_SELECTORS.codeBlock)).filter(isDiagramCodeBlock); }
function isDiagramCodeBlockReady(block) {
  if (!(block instanceof HTMLElement)) return false;
  if (block.querySelector('.ds-loading')) return false;
  if ((block.querySelector('pre')?.textContent || '').trim()) return true;
  return Boolean(block.querySelector('svg.mermaid-svg, .mermaid-svg')); }
function waitForCondition(predicate, root, timeoutMs = 2500) {
  if (predicate()) return Promise.resolve(true);
  const targetRoot = root instanceof Node ? root : (document.body || document.documentElement);
  if (!targetRoot) {
    dfWarn('waitForCondition: Kein gültiger DOM-Root zum Beobachten gefunden.');
    return Promise.resolve(false); }
  return new Promise((resolve) => {
    let settled = false;
    let observer = null;
    const finish = (ok) => {
      if (settled) return;
      settled = true;
      clearTimeout(timerId);
      observer?.disconnect();
      resolve(ok); };
    const timerId = setTimeout(() => finish(Boolean(predicate())), timeoutMs);
    observer = new MutationObserver(() => {
      if (predicate()) finish(true); });
    observer.observe(targetRoot, { childList: true, subtree: true, characterData: true, attributes: true }); }); }
function triggerTab(tab) {
  if (!(tab instanceof HTMLElement)) return;
  const label = (tab.textContent || '').trim();
  dfLog('triggerTab:', label || tab.className);
  try { tab.click(); } catch {} ['pointerdown', 'mousedown', 'mouseup'].forEach((type) => {
    try {
      tab.dispatchEvent(new MouseEvent(type, { bubbles: true, cancelable: true, view: window })); } 
    catch {} }); }
async function waitForDiagramBlocksReady(timeoutMs = 10000) {
  const initialBlocks = getDiagramBlocks();
  dfLog('waitForDiagramBlocksReady Start:', { count: initialBlocks.length, timeoutMs });
  if (initialBlocks.length === 0) return true;
  const t0 = Date.now();
  const checkAll = () => {
    const blocks = getDiagramBlocks();
    return blocks.length === 0 || blocks.every(isDiagramCodeBlockReady); };
  const ready = await waitForCondition(checkAll, document.body, timeoutMs);
  const elapsedMs = Date.now() - t0;
  if (ready) {
    dfLog('waitForDiagramBlocksReady abgeschlossen:', { count: initialBlocks.length, elapsedMs }); } 
    else {
    dfWarn('waitForDiagramBlocksReady Timeout erreicht.', { count: initialBlocks.length, elapsedMs }); }
  return ready; }
async function prepareDiagramCodeBlocks() {
  const blocks = getDiagramBlocks();
  dfLog('prepareDiagramCodeBlocks Start:', { diagramBlocks: blocks.length });
  if (blocks.length === 0) return;
  await Promise.all(
    blocks.map(async (block, index) => {
      const tabs = Array.from(block.querySelectorAll('[role="tab"]'));
      const selectedTab = tabs.find(isTabSelected) || null;
      const chartTab = tabs.find((t) => /diagram/i.test((t.textContent || '').trim()));
      const codeTab = tabs.find((t) => /code/i.test((t.textContent || '').trim()));
      const chartWasSelected = /diagram/i.test((selectedTab?.textContent || '').trim());
      const getPre = () => (block.querySelector('pre')?.textContent || '').trim();
      let preText = getPre();
      dfLog(`Diagramm-Block #${index + 1}:`, {
        hasInitialPre: Boolean(preText),
        hasCodeTab: Boolean(codeTab),
        hasChartTab: Boolean(chartTab),
        chartWasSelected });
      if (!preText && codeTab) {
        if (!isTabSelected(codeTab)) triggerTab(codeTab);
        const loaded = await waitForCondition(() => Boolean(getPre()), block, 2500);
        preText = getPre();
        dfLog(`Diagramm-Block #${index + 1} Code-Tab Ergebnis:`, { loaded, codeLength: preText.length }); }
      if (preText) {
        block.setAttribute('data-export-code', preText);
        const langText = (block.querySelector(DF_SELECTORS.codeLang)?.textContent || '').trim();
        if (langText) block.setAttribute('data-export-lang', langText);
        dfLog(`Diagramm-Block #${index + 1} gecacht:`, { lang: langText || 'auto', codeLength: preText.length }); } 
        else {
        dfWarn(`Diagramm-Block #${index + 1}: Kein Quellcode im DOM gefunden.`); }
      if (chartTab && chartWasSelected) {
        triggerTab(chartTab);
        const svgRestored = await waitForCondition(() => Boolean(block.querySelector('svg.mermaid-svg, .mermaid-svg')), block, 2500);
        dfLog(`Diagramm-Block #${index + 1} Diagramm-Ansicht wiederhergestellt:`, { svgRestored }); } 
        else if (selectedTab && !isTabSelected(selectedTab)) {
        triggerTab(selectedTab);
        dfLog(`Diagramm-Block #${index + 1} ursprünglicher Tab wiederhergestellt.`); } }) );
  dfLog('prepareDiagramCodeBlocks abgeschlossen.'); }
// ============================================================================
// 5. DOM-PARSING (KATEX, CODE, TABELLEN, MARKDOWN, QUELLEN)
// ============================================================================
const DF_INLINE_MATH_TAGS = new Set(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'strong', 'b', 'em', 'i', 'code']);
function texToMarkdown(domElements, katexElement) {
  let content = '';
  if (!domElements || domElements.length === 0) {
    dfLog('texToMarkdown: Keine TeX-Annotation-Elemente vorhanden.');
    return ''; }
  domElements.forEach((node) => {
    const tex = (node?.textContent || '').trim();
    if (tex && (node.closest?.('span.katex') || node.parentElement)) content += tex; });
  if (!content) {
    dfLog('texToMarkdown: Leerer TeX-Inhalt nach Trimmen.');
    return ''; }
  let isBlock = false;
  if (katexElement) {
    try {
      let isInlineContext = false;
      let current = katexElement.parentElement;
      while (current) {
        if (DF_INLINE_MATH_TAGS.has(current.tagName.toLowerCase())) {
          isInlineContext = true;
          break; }
        current = current.parentElement; }
      if (!isInlineContext) {
        const display = window.getComputedStyle(katexElement).display;
        if (katexElement.tagName.toLowerCase() !== 'span' || display === 'block') {
          isBlock = true; } 
        else {
          const parent = katexElement.parentElement;
          if (parent && parent.tagName.toLowerCase() !== 'p') {
            const hasOtherText = Array.from(parent.childNodes).some(
              (n) => n !== katexElement && n.nodeType === Node.TEXT_NODE && n.textContent.trim() );
            if (!hasOtherText) isBlock = true; } } } } 
    catch (e) {
      dfLog('Math display type Fallback:', e); } }
  return isBlock ? `$$${content}$$\n\n` : `$${content}$`; }
function extractMarkdownCodeInfo(domElement) {
  try {
    const cachedCode = (domElement.getAttribute('data-export-code') || '').trim();
    const cachedLang = (domElement.getAttribute('data-export-lang') || '').trim();
    if (cachedCode) {
      const language = cachedLang || (MERMAID_KEYWORD_RE.test(cachedCode) ? 'mermaid' : '');
      dfLog('extractMarkdownCodeInfo: Nutze gecachten Code-Block.', { language: language || 'none', length: cachedCode.length });
      return { language, content: cachedCode }; }
    const infoEl =
      domElement.querySelector(DF_SELECTORS.codeLang) ||
      domElement.querySelector('[data-language]') ||
      domElement.querySelector('.md-code-block-banner-wrap [class*="language"]');
    let language = infoEl ? (infoEl.getAttribute('data-language') || infoEl.textContent || '').trim() : '';
    if (!language) {
      const bannerText = (domElement.querySelector('.md-code-block-banner-wrap')?.textContent || '').trim();
      if (bannerText && !/^(code|diagram)$/i.test(bannerText)) {
        language = bannerText.split(/\s+/)[0]; } }
    const preText = (domElement.querySelector('pre')?.textContent || '').replace(/\u00A0/g, ' ').trim();
    if (preText) {
      if (!language && MERMAID_KEYWORD_RE.test(preText)) language = 'mermaid';
      dfLog('extractMarkdownCodeInfo: Code aus <pre> extrahiert.', { language: language || 'none', length: preText.length });
      return { language, content: preText }; }
    const hasMermaidSvg = Boolean(domElement.querySelector('svg.mermaid-svg, .mermaid-svg'));
    const tabText = (domElement.querySelector('[role="tablist"]')?.textContent || '').trim();
    const preferMermaid = hasMermaidSvg || /diagram|mermaid/i.test(tabText);
    const svgTexts = Array.from(
      domElement.querySelectorAll('svg text, svg foreignObject, svg .nodeLabel, svg .edgeLabel') )
      .map((node) => (node.textContent || '').replace(/\s+/g, ' ').trim())
      .filter(Boolean);
    const uniqueSvgTexts = Array.from(new Set(svgTexts)).slice(0, 80);
    dfWarn('extractMarkdownCodeInfo: Kein <pre>-Quelltext gefunden, nutze Diagramm-Fallback.', {
      preferMermaid,
      hasMermaidSvg,
      svgLabelCount: uniqueSvgTexts.length });
    if (uniqueSvgTexts.length > 0) {
      return preferMermaid
        ? { language: language || 'mermaid', content: `%% Mermaid source unavailable in DOM\n%% Diagram labels: ${uniqueSvgTexts.join(' | ')}` }
        : { language: language || 'diagram', content: `[diagram]\n${uniqueSvgTexts.join(' ')}` }; }
    return {
      language: language || (preferMermaid ? 'mermaid' : 'diagram'),
      content: preferMermaid ? '%% Mermaid source unavailable in DOM' : '[diagram content unavailable]' }; } 
  catch (error) {
    dfError('Code-Block-Fehler.', error);
    return null; } }
function convertTableToMarkdown(tableElement) {
  if (!tableElement || tableElement.nodeName.toLowerCase() !== 'table') {
    dfLog('convertTableToMarkdown: Ungültiges oder fehlendes <table>-Element.');
    return ''; }
  const extractCellText = (cell) => {
    let content = '';
    for (const child of cell.childNodes) {
      if (child.nodeType === Node.ELEMENT_NODE) content += domToMarkdown(child);
      else if (child.nodeType === Node.TEXT_NODE) content += child.textContent; }
    return content.trim().replace(/\|/g, '\\|').replace(/\n/g, ' '); };
  let headers = [];
  let skipFirstRow = false;
  const thead = tableElement.querySelector('thead');
  if (thead) {
    const headerRow = thead.querySelector('tr');
    if (headerRow) headers = Array.from(headerRow.querySelectorAll('th, td')).map(extractCellText); } 
  else {
    const firstRow = (tableElement.querySelector('tbody') || tableElement).querySelector('tr');
    if (firstRow) {
      skipFirstRow = true;
      const ths = firstRow.querySelectorAll('th');
      headers = Array.from(ths.length > 0 ? ths : firstRow.querySelectorAll('td')).map(extractCellText); } }
  if (headers.length === 0) {
    dfWarn('convertTableToMarkdown: Tabelle ohne verwertbare Spaltenüberschriften übersprungen.');
    return ''; }
  const rows = [];
  const rowElements = (tableElement.querySelector('tbody') || tableElement).querySelectorAll('tr');
  Array.from(rowElements).forEach((row, index) => {
    if (skipFirstRow && index === 0) return;
    const rowData = Array.from(row.querySelectorAll('td, th')).map(extractCellText);
    while (rowData.length < headers.length) rowData.push('');
    rows.push(rowData.slice(0, headers.length)); });
  dfLog('convertTableToMarkdown: Tabelle konvertiert.', { columns: headers.length, rows: rows.length });
  let markdown = `| ${headers.join(' | ')} |\n`;
  markdown += `| ${headers.map(() => '---').join(' | ')} |\n`;
  rows.forEach((row) => {
    markdown += `| ${row.join(' | ')} |\n`; });
  return `${markdown}\n`; }
function domToMarkdown(domElement) {
  if (!(domElement instanceof HTMLElement)) return domElement;
  if (domElement.classList.contains(DF_SELECTORS.codeBlock.slice(1))) {
    const codeInfo = extractMarkdownCodeInfo(domElement);
    return codeInfo ? `\`\`\`${codeInfo.language}\n${codeInfo.content}\n\`\`\`\n\n` : ''; }
  if (domElement.classList.contains('katex')) {
    const annotations = domElement.querySelectorAll('annotation[encoding="application/x-tex"]');
    return texToMarkdown(annotations, domElement); }
  const isWordLikeChar = (ch) =>
    /[0-9A-Za-z\u00C0-\u024F\u0370-\u03FF\u0400-\u04FF\u3040-\u30FF\u3400-\u4DBF\u4E00-\u9FFF\uAC00-\uD7AF]/.test(ch);
  const getNeighborInfo = (element, direction) => {
    let sibling = direction === 'left' ? element.previousSibling : element.nextSibling;
    while (sibling) {
      if (sibling.nodeType === Node.TEXT_NODE) {
        const normalized = String(sibling.textContent || '').replace(/\u00A0/g, ' ');
        const trimmed = normalized.trim();
        if (trimmed) {
          return {
            char: direction === 'left' ? trimmed.slice(-1) : trimmed.charAt(0),
            hasBoundarySpace: direction === 'left' ? /\s$/.test(normalized) : /^\s/.test(normalized),
            nodeType: Node.TEXT_NODE,
            tagName: '' }; } } 
        else if (sibling.nodeType === Node.ELEMENT_NODE) {
        const text = String(sibling.textContent || '').replace(/\u00A0/g, ' ').trim();
        if (text) {
          return {
            char: direction === 'left' ? text.slice(-1) : text.charAt(0),
            hasBoundarySpace: false,
            nodeType: Node.ELEMENT_NODE,
            tagName: sibling.nodeName.toLowerCase() }; } }
      sibling = direction === 'left' ? sibling.previousSibling : sibling.nextSibling; }
    return { char: '', hasBoundarySpace: false, nodeType: null, tagName: '' }; };
  const wrapInline = (element, marker, rawText) => {
    const text = String(rawText || '').trim();
    if (!text) return '';
    const left = getNeighborInfo(element, 'left');
    const right = getNeighborInfo(element, 'right');
    const leftBoundaryLike = isWordLikeChar(text.charAt(0)) || /^[([{<（【《「『“‘]/.test(text.charAt(0));
    const rightBoundaryLike = isWordLikeChar(text.slice(-1)) || /[)\]}>）】》」』”’'"`]/.test(text.slice(-1));
    const rightWillHandle = right.nodeType === Node.ELEMENT_NODE && /^(strong|b|em|i)$/.test(right.tagName);
    const needsRightSpace = !rightWillHandle && !right.hasBoundarySpace && right.char && rightBoundaryLike && isWordLikeChar(right.char);
    const needsLeftSpace = !left.hasBoundarySpace && left.char && isWordLikeChar(left.char) && leftBoundaryLike;
    return `${needsLeftSpace ? ' ' : ''}${marker}${text}${marker}${needsRightSpace ? ' ' : ''}`; };
  const childrenToMarkdown = (element) => {
    let content = '';
    for (const child of element.childNodes) {
      if (child.nodeType === Node.ELEMENT_NODE) content += domToMarkdown(child);
      else if (child.nodeType === Node.TEXT_NODE) content += child.textContent; }
    return content; };
  const tag = domElement.nodeName.toLowerCase();
  switch (tag) {
    case 'h1': case 'h2': case 'h3': case 'h4': case 'h5': case 'h6':
      return `${'#'.repeat(Number(tag.charAt(1)))} ${childrenToMarkdown(domElement).trim()}\n\n`;
    case 'p':
      return `${childrenToMarkdown(domElement).trim()}\n\n`;
    case 'ul':
      return (
        Array.from(domElement.children)
          .filter((li) => li.nodeName.toLowerCase() === 'li')
          .map((li) => `- ${childrenToMarkdown(li).trim()}\n`)
          .join('') + '\n' );
    case 'ol': {
      let index = domElement.hasAttribute('start') ? parseInt(domElement.getAttribute('start'), 10) || 1 : 1;
      return (
        Array.from(domElement.children)
          .filter((li) => li.nodeName.toLowerCase() === 'li')
          .map((li) => `${index++}. ${childrenToMarkdown(li).trim()}\n`)
          .join('') + '\n' ); }
    case 'blockquote': {
      const normalized = childrenToMarkdown(domElement).replace(/\r\n?/g, '\n').trim();
      return normalized ? `${normalized.split('\n').map((l) => `> ${l}`).join('\n')}\n\n` : '> \n\n'; }
    case 'a': {
      const href = (domElement.getAttribute('href') || '').trim();
      return `[${childrenToMarkdown(domElement).trim()}](${href})`; }
    case 'strong': case 'b':
      return wrapInline(domElement, '**', childrenToMarkdown(domElement));
    case 'em': case 'i':
      return wrapInline(domElement, '*', childrenToMarkdown(domElement));
    case 'code':
      return domElement.closest(DF_SELECTORS.codeBlock) ? domElement.textContent.trim() : `\`${domElement.textContent.trim()}\``;
    case 'img':
      return `![${domElement.getAttribute('alt') || ''}](${domElement.getAttribute('src') || ''})`;
    case 'hr':
      return '---\n\n';
    case 'br':
      return ' \n';
    case 'table':
      return convertTableToMarkdown(domElement);
    default:
      return childrenToMarkdown(domElement); } }
function normalizeAssistantContent(domElement) {
  if (!(domElement instanceof HTMLElement)) {
    dfLog('normalizeAssistantContent: Kein HTMLElement übergeben.', typeof domElement);
    return { element: domElement, references: [] }; }
  const cloned = domElement.cloneNode(true);
  const references = [];
  const referenceMap = new Map();
  const getDomain = (href) => {
    try {
      return new URL(href, window.location.href).hostname.replace(/^www\./, ''); } 
      catch (err) {
      dfLog('normalizeAssistantContent: Ungültige Quellen-URL.', { href, err });
      return ''; } };
  let removedSourceBlocks = 0;
  cloned.querySelectorAll('a').forEach((link) => {
    const href = (link.getAttribute('href') || '').trim();
    if (!link.querySelector('.ds-markdown-cite') || !href) return;
    const label = getDomain(href);
    const key = href || label;
    let index = referenceMap.get(key);
    if (!index) {
      references.push({ href, label });
      index = references.length;
      referenceMap.set(key, index); }
    link.replaceWith(cloned.ownerDocument.createTextNode(`[^${index}]`)); });
  cloned.querySelectorAll(DF_SELECTORS.sourceBlock).forEach((source) => {
    source.remove();
    removedSourceBlocks += 1; });
  if (references.length > 0 || removedSourceBlocks > 0) {
    dfLog('normalizeAssistantContent: Quellen normalisiert.', { uniqueReferences: references.length, removedSourceBlocks }); }
  return { element: cloned, references }; }
function assistantElementToMarkdown(domElement) {
  const normalized = normalizeAssistantContent(domElement);
  const content = domToMarkdown(normalized.element).trim();
  dfLog('assistantElementToMarkdown:', { contentLength: content.length, referenceCount: normalized.references.length });
  return {
    content,
    references: normalized.references }; }
function removeReferenceMarkers(text) {
  return String(text ?? '').replace(/\[\^\d+\]/g, ''); }
function referencesToMarkdown(items, ids) {
  if (!Array.isArray(items) || items.length === 0) return '';
  return items
    .map((item, i) => {
      const refId = Array.isArray(ids) && ids[i] ? String(ids[i]).trim() : String(i + 1);
      const href = (item?.href || '').trim();
      const label = (item?.label || '').trim();
      return label && href ? `[^${refId}]: [${label}](${href})` : `[^${refId}]: ${href || label}`; })
    .join('\n'); }
function referencesToPlainText(items) {
  if (!Array.isArray(items) || items.length === 0) return '';
  return items
    .map((item, i) => {
      const href = (item?.href || '').trim();
      const label = (item?.label || '').trim();
      return (label && href ? `${i + 1}. ${label} - ${href}` : `${i + 1}. ${href || label}`).trim(); })
    .join('\n'); }
function extractParagraphs(element) {
  if (!element) return '';
  const paragraphs = Array.from(element.querySelectorAll('p')).map((p) => p.textContent.trim());
  return paragraphs.length > 0 ? paragraphs.join('\n') : element.textContent.trim(); }
// ============================================================================
// 6. CHAT-EXTRAKTION (TITEL, USER-ANHÄNGE, NACHRICHTEN)
// ============================================================================
function getDefaultConversationTitle() {
  const now = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `DeepSeek-Chat-${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}-${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`; }
function getConversationTitle() {
  for (const sel of DF_SELECTORS.chatTitle.split(',').map((s) => s.trim())) {
    const text = (document.querySelector(sel)?.textContent || '').trim();
    if (text) {
      dfLog('getConversationTitle aus Selektor:', { selector: sel, title: text });
      return text; } }
  const docTitle = (document.title || '').trim();
  if (docTitle) {
    dfLog('getConversationTitle aus document.title:', docTitle);
    return docTitle; }
  const fallbackTitle = getDefaultConversationTitle();
  dfLog('getConversationTitle Fallback generiert:', fallbackTitle);
  return fallbackTitle; }
function extractUserAttachments(messageElement) {
  if (!(messageElement instanceof Element)) {
    dfLog('extractUserAttachments: Ungültiges messageElement.');
    return []; }
  const container = messageElement.closest(DF_SELECTORS.message) || messageElement.closest('._9663006');
  if (!container) {
    dfLog('extractUserAttachments: Kein Nachrichten-Container gefunden.');
    return []; }
  const nameNodes = Array.from(container.querySelectorAll(DF_SELECTORS.attachmentName));
  const sizeNodes = Array.from(container.querySelectorAll(DF_SELECTORS.attachmentSize));
  const attachments = [];
  const seen = new Set();
  nameNodes.forEach((nameNode, index) => {
    const name = (nameNode.textContent || '').trim();
    const size = (sizeNodes[index]?.textContent || '').trim();
    if (!name) return;
    const key = `${name}__${size}`;
    if (seen.has(key)) return;
    seen.add(key);
    attachments.push({ name, size, type: size ? size.split(/\s+/)[0] : '' }); });
  if (attachments.length > 0) {
    dfLog('extractUserAttachments gefunden:', { count: attachments.length, files: attachments.map((a) => a.name) }); }
  return attachments; }
function formatUserContent(text, attachments) {
  const normalizedText = (text || '').trim();
  if (!Array.isArray(attachments) || attachments.length === 0) return normalizedText;
  const lines = attachments.map((item, i) => `${i + 1}. ${item.name}${item.size ? ` (${item.size})` : ''}`).join('\n');
  return normalizedText ? `${normalizedText}\n\nAttachments:\n${lines}` : `Attachments:\n${lines}`; }
function getLongestRun(text, targetChar) {
  let max = 0;
  let current = 0;
  for (let i = 0; i < text.length; i++) {
    if (text[i] === targetChar) {
      current += 1;
      if (current > max) max = current; } 
      else {
      current = 0; } }
  return max; }
function formatUserMarkdownContent(content) {
  const text = String(content ?? '');
  const maxBackticks = getLongestRun(text, '`');
  const maxTildes = getLongestRun(text, '~');
  const useBackticks = maxBackticks <= maxTildes;
  const fence = (useBackticks ? '`' : '~').repeat(Math.max(3, (useBackticks ? maxBackticks : maxTildes) + 1));
  return `${fence}text\n${text}\n${fence}`; }
function extractAllMessagesFromPage(root = document, { cloneDomNodes = false } = {}) {
  try {
    const queryRoot = root && typeof root.querySelectorAll === 'function' ? root : document;
    const userQuestions = queryRoot.querySelectorAll(DF_SELECTORS.userQuestion);
    const aiResponses = queryRoot.querySelectorAll(DF_SELECTORS.aiMarkdown);
    const cotContainers = queryRoot.querySelectorAll(DF_SELECTORS.cotContainer);
    dfLog('extractAllMessagesFromPage DOM-Treffer:', {
      userCount: userQuestions.length,
      aiCount: aiResponses.length,
      cotCount: cotContainers.length,
      cloneDomNodes });
    if (userQuestions.length === 0 && aiResponses.length === 0 && cotContainers.length === 0) {
      dfWarn('extractAllMessagesFromPage: Keine Chat-Elemente im DOM gefunden.');
      return {}; }
    const allElements = [
      ...Array.from(userQuestions).map((element) => ({ element, type: 'user' })),
      ...Array.from(aiResponses).map((element) => ({ element, type: 'ai' })),
      ...Array.from(cotContainers).map((element) => ({ element, type: 'cot' })) ];
    allElements.sort((a, b) => {
      if (a.element === b.element) return 0;
      const pos = a.element.compareDocumentPosition(b.element);
      if (pos & Node.DOCUMENT_POSITION_FOLLOWING) return -1;
      if (pos & Node.DOCUMENT_POSITION_PRECEDING) return 1;
      return 0; });
    const messages = [];
    let cot = null;
    allElements.forEach(({ element, type }, index) => {
      if (type === 'user') {
        const attachments = extractUserAttachments(element);
        const message = {
          role: 'user',
          content: formatUserContent((element.textContent || '').trim(), attachments),
          element_id: element.id || `user-${index}-${Date.now()}` };
        if (attachments.length > 0) message.attachments = attachments;
        messages.push(message); } 
        else if (type === 'ai') {
        const message = {
          role: 'assistant',
          content: cloneDomNodes ? element.cloneNode(true) : element,
          element_id: element.id || `ai-${index}-${Date.now()}` };
        if (cot !== null) {
          message.chain_of_thought = cot;
          cot = null; }
        messages.push(message); } 
        else if (type === 'cot') {
        cot = cloneDomNodes ? element.cloneNode(true) : element; } });
    const title = getConversationTitle();
    dfLog('extractAllMessagesFromPage fertig:', { title, totalMessages: messages.length, pendingCot: Boolean(cot) });
    return { title, messages }; } 
    catch (error) {
    dfError('Nachrichten konnten nicht gelesen werden.', error);
    return {}; } }
// ============================================================================
// 7. FORMAT-KONVERTER (MARKDOWN, PLAIN TEXT, JSON)
// ============================================================================
function formatExportDate(rawDate) {
  const parsed = rawDate ? new Date(rawDate) : new Date();
  if (Number.isNaN(parsed.getTime())) {
    dfLog('formatExportDate: Ungültiges Datum, nutze aktuelle Zeit.', rawDate);
    return new Date().toLocaleString('de-DE'); }
  return parsed.toLocaleString('de-DE'); }
function formatAssistantExportText(assistantData, includeReferences) {
  const rawContent = assistantData?.content || '';
  const refs = Array.isArray(assistantData?.references) ? assistantData.references : [];
  if (includeReferences) {
    return { text: rawContent, references: refs }; }
  return { text: removeReferenceMarkers(rawContent), references: [] }; }
function convertToMarkdown(data, settings) {
  const includeReferences = Boolean(settings?.exportWebReferences);
  const messages = Array.isArray(data?.messages) ? data.messages : [];
  const title = data?.title || 'DeepSeek Chat';
  const url = data?.url || '';
  const formattedDate = formatExportDate(data?.date);
  dfLog('convertToMarkdown Start:', { title, messageCount: messages.length, includeReferences });
  let markdown = `# ${title}\n\n- **URL**: ${url}\n- **Date**: ${formattedDate}\n\n---\n\n`;
  let globalReferenceCounter = 0;
  messages.forEach((msg, index) => {
    const roleHeader = msg.role === 'user' ? '## 🧑 User' : '## 🤖 DeepSeek AI';
    markdown += `${roleHeader}\n\n`;
    if (msg.role === 'assistant' && msg.chain_of_thought) {
      markdown += `### Chain of Thought\n\n${extractParagraphs(msg.chain_of_thought)}\n\n`; }
    if (msg.role === 'assistant') {
      const assistantData = assistantElementToMarkdown(msg.content);
      let assistantContent = assistantData.content;
      if (assistantData.references.length > 0 && includeReferences) {
        const referenceIds = assistantData.references.map(() => ++globalReferenceCounter);
        assistantContent = assistantContent
          .replace(/\[\^(\d+)\]/g, (match, localIdx) => {
            const idx = Number(localIdx) - 1;
            const mapped = idx >= 0 && idx < referenceIds.length ? referenceIds[idx] : undefined;
            return mapped ? `[^${mapped}]` : match; })
          .replace(/(\[\^\d+\])(?=\[\^\d+\])/g, '$1 ');
        markdown += `${assistantContent}\n\n### References\n\n${referencesToMarkdown(assistantData.references, referenceIds)}\n\n`; } 
        else {
        markdown += `${removeReferenceMarkers(assistantContent)}\n\n`; } } 
      else {
      markdown += `${formatUserMarkdownContent(msg.content)}\n\n`; }
    if (index < messages.length - 1) markdown += '---\n\n'; });
  dfLog('convertToMarkdown fertig:', { length: markdown.length, totalReferences: globalReferenceCounter });
  return markdown; }
function convertToPlainText(data, settings) {
  const includeReferences = Boolean(settings?.exportWebReferences);
  const messages = Array.isArray(data?.messages) ? data.messages : [];
  const title = data?.title || 'DeepSeek Chat';
  const url = data?.url || '';
  const formattedDate = formatExportDate(data?.date);
  dfLog('convertToPlainText Start:', { title, messageCount: messages.length, includeReferences });
  let text = `${title}\n\nURL: ${url}\nDate: ${formattedDate}\n\n----------------------------------------\n\n`;
  messages.forEach((msg, index) => {
    text += `${msg.role === 'user' ? 'User' : 'DeepSeek AI'}:\n\n`;
    if (msg.role === 'assistant' && msg.chain_of_thought) {
      text += `Thinking process:\n\n${extractParagraphs(msg.chain_of_thought)}\n\n`; }
    if (msg.role === 'user') {
      text += `${msg.content}\n\n`; } 
      else {
      const assistantData = formatAssistantExportText(assistantElementToMarkdown(msg.content), includeReferences);
      text += `${assistantData.text}\n\n`;
      if (includeReferences && assistantData.references.length > 0) {
        text += `References:\n${referencesToPlainText(assistantData.references)}\n\n`; } }
    if (index < messages.length - 1) text += '----------------------------------------\n\n'; });
  dfLog('convertToPlainText fertig:', { length: text.length });
  return text; }
function convertToJSON(formattedData, settings) {
  const includeReferences = Boolean(settings?.exportWebReferences);
  const sourceMessages = Array.isArray(formattedData?.messages) ? formattedData.messages : [];
  dfLog('convertToJSON Start:', { title: formattedData?.title || '', messageCount: sourceMessages.length, includeReferences });
  const messages = sourceMessages.map((msg) => {
    if (msg.role === 'assistant') {
      const assistantData = formatAssistantExportText(assistantElementToMarkdown(msg.content), includeReferences);
      return {
        role: msg.role,
        content: assistantData.text,
        references: assistantData.references,
        chain_of_thought: extractParagraphs(msg.chain_of_thought) }; }
    const userMessage = { role: msg.role, content: String(msg.content ?? '') };
    if (Array.isArray(msg.attachments) && msg.attachments.length > 0) userMessage.attachments = msg.attachments;
    return userMessage; });
  const result = {
    title: formattedData?.title || '',
    url: formattedData?.url || '',
    date: formattedData?.date || new Date().toISOString(),
    messages };
  dfLog('convertToJSON fertig:', { messageCount: messages.length });
  return result; }
// ============================================================================
// 8. DATEI-ANHÄNGE & PDF-CAPTURE (FÜR HTML-EXPORT)
// ============================================================================
function isCapturableFile(name) {
  const ext = (String(name).split('.').pop() || '').toLowerCase();
  return !NON_CAPTURABLE_EXTENSIONS.has(ext); }
function findAttachmentCards() {
  const cards = [];
  const seen = new Set();
  document.querySelectorAll('.e70accd6').forEach((nameEl, index) => {
    if (!nameEl.closest('.ds-message')) return;
    const name = (nameEl.textContent || '').trim();
    const card = nameEl.closest('._25c7358.dafb6286') || nameEl.closest('._25c7358') || nameEl.closest('.dafb6286');
    if (!name || !card) return;
    const uniqueKey = `${index}::${name}`;
    if (seen.has(uniqueKey)) return;
    seen.add(uniqueKey);
    cards.push({ element: card, name }); });
  dfLog('(Attachments) Karten gefunden:', cards.length, cards.map((c) => c.name));
  return cards; }
function findOpenFileModal() {
  for (const el of document.querySelectorAll('[aria-hidden="false"]')) {
    const heading = el.querySelector('[role="heading"]');
    if (!heading) continue;
    const contentEl = el.querySelector('.abbe3c45') || el.querySelector('[class*="scroll"] pre') || el.querySelector('pre');
    if (contentEl) {
      return { modal: el, name: (heading.textContent || '').trim(), content: contentEl.textContent || '' }; } }
  return null; }
function isPdfViewerOpen() {
  return document.querySelectorAll('.react-pdf__Page').length > 0; }
async function waitForPdfViewerClosed(timeoutMs = 3000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    if (!isExtensionContextValid()) return false;
    if (!isPdfViewerOpen() && !findOpenFileModal()) return true;
    await delay(150); }
  return !isPdfViewerOpen(); }
async function closeAnyOverlayModal() {
  const selectors = ['[role="dialog"]', '[class*="viewer" i]', '[class*="preview" i]', '[aria-hidden="false"]'];
  let clicked = false;
  for (const sel of selectors) {
    for (const overlay of document.querySelectorAll(sel)) {
      if (!overlay.offsetParent && overlay.tagName !== 'BODY') continue;
      for (const btn of overlay.querySelectorAll('button, [role="button"]')) {
        const svg = btn.querySelector('svg');
        const label = `${btn.getAttribute('aria-label') || ''} ${btn.getAttribute('title') || ''}`.toLowerCase();
        if ((svg && svg.querySelectorAll('path').length === 2) || /close|schließ|zurück/.test(label)) {
          btn.click();
          clicked = true;
          dfLog('(Modal) Schließen-Button geklickt:', label || sel);
          break; } }
      if (clicked) break; }
    if (clicked) break; }
  if (!clicked) {
    const esc = new KeyboardEvent('keydown', { key: 'Escape', code: 'Escape', keyCode: 27, bubbles: true });
    document.dispatchEvent(esc);
    document.body.dispatchEvent(esc);
    document.activeElement?.dispatchEvent(esc);
    dfLog('(Modal) Escape gesendet'); }
  await waitForPdfViewerClosed(2500);
  await delay(350); }
async function waitForFileModalContent(expectedName, timeoutMs = 3000) {
  const target = expectedName.toLowerCase();
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    if (!isExtensionContextValid()) return null;
    const modal = findOpenFileModal();
    if (modal) {
      const modalName = modal.name.toLowerCase();
      if (modalName === target || modalName.includes(target) || target.includes(modalName)) {
        return modal.content; } }
    await delay(120); }
  return null; }
async function capturePdfAsImages(card, name) {
  if (!isExtensionContextValid()) {
    dfLog('(PDF) Abbruch: Extension-Kontext ungültig vor Start:', name);
    return null; }
  await closeAnyOverlayModal();
  await delay(400);
  try {
    card.scrollIntoView({ block: 'center', behavior: 'instant' });
    await delay(250);
    card.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
    dfLog('(PDF) Attachment geklickt:', name); } 
    catch (err) {
    dfLog('(PDF) Klick fehlgeschlagen:', name, err);
    return null; }
  const pageWaitStart = Date.now();
  while (Date.now() - pageWaitStart < 25000) {
    if (!isExtensionContextValid()) return null;
    if (document.querySelectorAll('.react-pdf__Page').length > 0) break;
    await delay(250); }
  let lastCount = 0;
  let stableTime = 0;
  const discoverStart = Date.now();
  while (Date.now() - discoverStart < PDF_DISCOVERY_MAX_MS) {
    if (!isExtensionContextValid()) return null;
    const pageEls = document.querySelectorAll('.react-pdf__Page');
    const count = pageEls.length;
    updateExportingOverlay(`Read: ${count}\n${name}`);
    if (count > 0 && count === lastCount) {
      stableTime += 750;
      if (stableTime >= PDF_DISCOVERY_STABLE_MS) break; } 
      else if (count > 0) {
      dfLog('(PDF) Seitenzahl aktualisiert:', name, count);
      lastCount = count;
      stableTime = 0; }
    if (count > 0) {
      try {
        pageEls[count - 1].scrollIntoView({ block: 'end', behavior: 'smooth' }); } 
        catch {} }
    await delay(750); }
  const totalPages = document.querySelectorAll('.react-pdf__Page').length;
  dfLog('(PDF) Discovery abgeschlossen:', name, 'totalPages =', totalPages);
  if (totalPages === 0) {
    await closeAnyOverlayModal();
    return null; }
  const readCanvas = async (pageWrapper, pageNum, timeoutMs = PDF_PAGE_TIMEOUT_MS) => {
    const start = Date.now();
    let lastUrl = '';
    let stableReads = 0;
    let nudgeSent = false;
    while (Date.now() - start < timeoutMs) {
      if (!isExtensionContextValid()) return '';
      const canvas = pageWrapper.querySelector('.react-pdf__Page__canvas');
      if (canvas && canvas.width > 0 && canvas.height > 0) {
        try {
          const url = canvas.toDataURL('image/png');
          if (url && url.startsWith('data:image/png;base64,')) {
            if (url === lastUrl) {
              stableReads += 1;
              if (stableReads >= 2) {
                return url; } } 
              else {
              lastUrl = url;
              stableReads = 1; } } } 
          catch (err) {
          dfLog('(PDF) toDataURL Fehler auf Seite', pageNum, ':', err); } }
      if (!nudgeSent && Date.now() - start > timeoutMs * 0.5) {
        nudgeSent = true;
        dfLog('(PDF) Sanfter Scroll-Anstoß auf Seite:', name, pageNum);
        try {
          pageWrapper.scrollIntoView({ block: 'center', behavior: 'instant' }); } 
          catch {} }
      await delay(PDF_PAGE_SETTLE_MS); }
    if (lastUrl && lastUrl.startsWith('data:image/png;base64,')) {
      dfLog('(PDF) Nutze letzten Canvas-Stand nach Wartezeit auf Seite:', name, pageNum);
      return lastUrl; }
    return ''; };
  const pages = [];
  for (let i = 0; i < totalPages; i++) {
    if (!isExtensionContextValid()) return null;
    const pageNum = i + 1;
    updateExportingOverlay(`Capture: ${pageNum}/${totalPages}\n${name}`);
    const allPages = document.querySelectorAll('.react-pdf__Page');
    const pageWrapper = allPages[i];
    if (!pageWrapper) {
      dfLog('(PDF) Kein Page-Wrapper gefunden für Seite:', name, pageNum);
      continue; }
    try {
      pageWrapper.scrollIntoView({ block: 'center', behavior: 'instant' }); } 
      catch {}
    await delay(PDF_PAGE_SETTLE_MS);
    const t0 = Date.now();
    const dataUrl = await readCanvas(pageWrapper, pageNum, PDF_PAGE_TIMEOUT_MS);
    const elapsedMs = Date.now() - t0;
    if (dataUrl) {
      pages.push({ index: pageNum, src: dataUrl });
      dfLog('(PDF) Seite erfasst:', name, `${pageNum}/${totalPages}`, `(${elapsedMs}ms, len=${dataUrl.length})`); } 
      else {
      dfLog('(PDF) Seite lieferte kein Canvas-Bild:', name, `${pageNum}/${totalPages}`, `(${elapsedMs}ms)`); } }
  await closeAnyOverlayModal();
  dfLog('(PDF) Fertig:', name, `gespeichert=${pages.length}/${totalPages}`);
  return pages.length > 0 ? { type: 'pdf', pages, total: totalPages } : null; }
async function captureAttachmentContents() {
  const result = {};
  if (!isExtensionContextValid()) {
    dfLog('(Attachments) Abbruch: Extension-Kontext ungültig.');
    return result; }
  const cards = findAttachmentCards();
  if (cards.length === 0) return result;
  if (findOpenFileModal() || isPdfViewerOpen()) await closeAnyOverlayModal();
  for (let i = 0; i < cards.length; i++) {
    if (!isExtensionContextValid()) break;
    const { element, name } = cards[i];
    if (result[name] || !isCapturableFile(name)) continue;
    const ext = (name.split('.').pop() || '').toLowerCase();
    updateExportingOverlay(`${i + 1}/${cards.length}\n${name}`);
    dfLog('(Attachments) Verarbeite:', `${i + 1}/${cards.length}`, name);
    if (ext === 'pdf') {
      try {
        const pdfData = await capturePdfAsImages(element, name);
        if (pdfData) {
          result[name] = pdfData; } 
          else {
          dfWarn(`(PDF) konnte nicht geladen werden: ${name}`); } } 
        catch (err) {
        dfLog('(PDF) Ausnahmefehler:', name, err);
        dfWarn(`(PDF) Fehler beim Capture: ${name}`);
        await closeAnyOverlayModal(); }
      await delay(350);
      continue; }
    try {
      element.scrollIntoView({ block: 'center', behavior: 'instant' });
      await delay(200);
      element.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
      let content = await waitForFileModalContent(name, 1200);
      if (content === null) {
        await closeAnyOverlayModal();
        await delay(400);
        element.click();
        content = await waitForFileModalContent(name, 2500); }
      if (content !== null) {
        result[name] = content;
        dfLog('(Attachments) Datei erfasst:', name, 'Länge:', content.length); } 
        else {
        dfWarn(`Konnte nicht laden: ${name}`); }
      await closeAnyOverlayModal();
      await delay(350); } 
      catch (err) {
      dfLog('(Attachments) Fehler bei Datei:', name, err);
      dfWarn(`Fehler bei ${name}`);
      await closeAnyOverlayModal();
      await delay(250); } }
  return result; }
// ============================================================================
// 9. STANDALONE HTML-EXPORT (STYLES, FONTS, TOC, FILE-DRAWER)
// ============================================================================
function sendBgMessage(payload) {
  if (!isExtensionContextValid()) {
    dfWarn('sendBgMessage abgebrochen: Extension-Kontext ungültig.', payload?.action);
    return Promise.resolve(null); }
  return new Promise((resolve) => {
    try {
      chrome.runtime.sendMessage(payload, (response) => {
        const lastError = chrome.runtime?.lastError;
        if (lastError) {
          dfLog('sendBgMessage runtime.lastError:', { action: payload?.action, message: lastError.message });
          resolve(null);
          return; }
        if (!response?.ok) {
          dfLog('sendBgMessage ohne ok-Antwort:', { action: payload?.action, url: payload?.url });
          resolve(null);
          return; }
        resolve(response); }); } 
      catch (err) {
      dfLog('sendBgMessage Exception:', { action: payload?.action, err });
      resolve(null); } }); }
function snapshotCssVariables() {
  const root = getComputedStyle(document.documentElement);
  const vars = [];
  for (const name of root) {
    if (name.startsWith('--')) {
      const value = root.getPropertyValue(name).trim();
      if (value) vars.push(`  ${name}: ${value};`); } }
  dfLog('snapshotCssVariables:', { count: vars.length });
  return `:root {\n${vars.join('\n')}\n}`; }
function resolveCssUrls(cssText) {
  return cssText.replace(/url\((['"]?)([^'")]+)\1\)/g, (match, _q, url) => {
    if (!url || /^(data:|https?:|#)/i.test(url)) return match;
    try {
      return `url("${new URL(url, window.location.href).href}")`; } 
      catch {
      return match; } }); }
async function inlineFontFaceUrls(cssText) {
  const fontUrls = new Set();
  const re = /@font-face\s*{[^}]*?url\((['"]?)([^'")]+)\1\)/g;
  let m;
  while ((m = re.exec(cssText)) !== null) {
    if (m[2] && /^https?:/i.test(m[2])) fontUrls.add(m[2]); }
  dfLog('inlineFontFaceUrls gefunden:', { uniqueFonts: fontUrls.size });
  if (fontUrls.size === 0) return cssText;
  const fetched = await Promise.all(
    Array.from(fontUrls).map(async (url) => {
      const res = await sendBgMessage({ action: 'fetchDataUrl', url });
      return { url, dataUrl: res?.dataUrl || '' }; }) );
  let result = cssText;
  let inlinedCount = 0;
  fetched.forEach(({ url, dataUrl }) => {
    if (dataUrl) {
      result = result.split(url).join(dataUrl);
      inlinedCount += 1; } });
  dfLog('inlineFontFaceUrls abgeschlossen:', { inlined: inlinedCount, total: fontUrls.size });
  return result; }
async function collectOriginalStyles() {
  const chunks = [];
  const seenHrefs = new Set();
  const externalHrefs = [];
  let inlineStyleCount = 0;
  let accessibleSheetCount = 0;
  document.querySelectorAll('style').forEach((style) => {
    if (style.textContent) {
      chunks.push(style.textContent);
      inlineStyleCount += 1; } });
  for (const sheet of Array.from(document.styleSheets)) {
    const href = sheet.href || '';
    if (href && seenHrefs.has(href)) continue;
    if (href) seenHrefs.add(href);
    try {
      const rules = Array.from(sheet.cssRules || []);
      chunks.push(rules.map((r) => r.cssText).join('\n'));
      accessibleSheetCount += 1; } 
      catch {
      if (href) externalHrefs.push(href); } }
  if (externalHrefs.length > 0) {
    dfLog('collectOriginalStyles lade externe Stylesheets:', { count: externalHrefs.length });
    const fetchedSheets = await Promise.all(
      externalHrefs.map(async (href) => {
        const res = await sendBgMessage({ action: 'fetchText', url: href });
        return res?.text || ''; }) );
    fetchedSheets.forEach((text) => {
      if (text) chunks.push(text); }); }
  chunks.push(snapshotCssVariables());
  const rawCss = resolveCssUrls(chunks.join('\n\n'));
  dfLog('collectOriginalStyles Basis gesammelt:', {
    inlineStyleCount,
    accessibleSheetCount,
    externalFetched: externalHrefs.length,
    rawCssLength: rawCss.length });
  return inlineFontFaceUrls(rawCss); }
async function getBlackChanceryDataUrl() {
  if (!isExtensionContextValid()) {
    dfWarn('getBlackChanceryDataUrl abgebrochen: Extension-Kontext ungültig.');
    return ''; }
  try {
    const fontUrl = chrome.runtime.getURL('fonts/BlackChancery.ttf');
    const response = await fetch(fontUrl);
    if (!response.ok) {
      dfWarn('getBlackChanceryDataUrl HTTP-Fehler:', { status: response.status, fontUrl });
      return ''; }
    const blob = await response.blob();
    return await new Promise((resolve) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        const result = typeof reader.result === 'string' ? reader.result : '';
        dfLog('getBlackChanceryDataUrl geladen:', { length: result.length });
        resolve(result); };
      reader.onerror = () => {
        dfWarn('getBlackChanceryDataUrl FileReader-Fehler.');
        resolve(''); };
      reader.readAsDataURL(blob); }); } 
    catch (err) {
    dfWarn('getBlackChanceryDataUrl Exception:', err);
    return ''; } }
async function buildOriginalHtml(attachmentsData = {}) {
  clearToasts();
  const root = document.querySelector('main') || document.body;
  if (!root) {
    dfError('buildOriginalHtml: Kein DOM-Root (main/body) gefunden.');
    return ''; }
  dfLog('buildOriginalHtml Start:', { attachmentKeys: Object.keys(attachmentsData || {}) });
  const cloned = root.cloneNode(true);
  const markClickable = (el, attrName, attrValue) => {
    el.setAttribute(attrName, attrValue);
    el.style.setProperty('cursor', 'pointer', 'important');
    el.style.setProperty('pointer-events', 'auto', 'important'); };
  const removedUi = cloned.querySelectorAll(
    '#df-toast-container, [id^="df-toast"], [class*="df-toast"], #deepseek-export-container, #deepseek-export-loading, #deepforge-electric-filters, [class*="notification"], script' );
  removedUi.forEach((el) => el.remove());
  cloned.querySelectorAll('div').forEach((el) => {
    if ((el.textContent || '').trim() === 'One more step before you proceed...' && el.children.length <= 3) {
      el.remove(); } });
  cloned.querySelectorAll('[aria-hidden="false"]').forEach((el) => {
    if (!el.querySelector('.ds-message') && el.querySelector('[role="heading"]')) el.remove(); });
  let markedFileCards = 0;
  cloned.querySelectorAll('.e70accd6').forEach((nameEl) => {
    if (!nameEl.closest('.ds-message')) return;
    const name = (nameEl.textContent || '').trim();
    const card = nameEl.closest('._25c7358.dafb6286') || nameEl.closest('._25c7358') || nameEl.closest('.dafb6286');
    if (!name || !card) return;
    markClickable(card, 'data-df-file-name', name);
    markedFileCards += 1; });
  const globalRefs = [];
  const seenRefs = new Set();
  cloned.querySelectorAll('a[aria-label][href]').forEach((a) => {
    const label = (a.getAttribute('aria-label') || '').trim();
    const href = (a.getAttribute('href') || '').trim();
    if (!/^\d+$/.test(label) || !href || !a.querySelector('.ds-markdown-cite') || seenRefs.has(href)) return;
    seenRefs.add(href);
    globalRefs.push({ label, href }); });
  globalRefs.sort((a, b) => parseInt(a.label, 10) - parseInt(b.label, 10));
  let markedRefBlocks = 0;
  if (globalRefs.length > 0) {
    const refsJson = JSON.stringify(globalRefs);
    cloned.querySelectorAll('.f93f59e4').forEach((refBlock) => {
      markClickable(refBlock, 'data-df-references', refsJson);
      markedRefBlocks += 1; }); }
  cloned.querySelectorAll('._871cbca').forEach((el) => el.remove());
  cloned.querySelectorAll('textarea, [contenteditable="true"]').forEach((el) => {
    const parent = el.closest('[class*="input"], [class*="editor"], [class*="composer"]') || el.parentElement;
    if (parent && !parent.querySelector('.ds-message')) parent.remove();
    else el.remove(); });
  const sidebarCandidates = [];
  cloned.querySelectorAll('*').forEach((el) => {
    if (el.querySelector('.ds-message')) return;
    const allChatLinks = el.querySelectorAll('a[href*="/chat/s/"]').length;
    const anchorChatLinks = el.querySelectorAll('a[href*="/chat/s/"][href*="#"]').length;
    const score = allChatLinks - anchorChatLinks;
    if (score >= 3) sidebarCandidates.push({ el, score }); });
  sidebarCandidates.sort((a, b) => b.score - a.score);
  if (sidebarCandidates[0]) {
    sidebarCandidates[0].el.remove();
    dfLog('buildOriginalHtml Sidebar entfernt:', { score: sidebarCandidates[0].score }); }
  let removedEmptyDivs = 0;
  cloned.querySelectorAll('div').forEach((el) => {
    if (!el.parentElement) return;
    if (
      !(el.textContent || '').trim() &&
      !el.querySelector('.ds-message, a, img, svg, button') ) {
      el.remove();
      removedEmptyDivs += 1; } });
  const tocEntries = Array.from(cloned.querySelectorAll(DF_SELECTORS.userQuestion)).map((u, i) => {
    const id = `df-user-${i + 1}`;
    u.id = id;
    let text = (u.textContent || '').replace(/\s+/g, ' ').trim();
    if (text.length > TOC_MAX_LABEL_LENGTH) text = `${text.slice(0, TOC_MAX_LABEL_LENGTH - 3)}…`;
    return { id, label: text || `Nachricht ${i + 1}`, index: i + 1 }; });
  const tocHtml =
    tocEntries.length > 0
      ? `<nav class="df-toc collapsed" id="df-toc">
          <div class="df-toc-header" id="df-toc-header">
            <span class="df-toc-toggle-icon"></span>
            <span class="df-toc-title"> Content  (${tocEntries.length})</span>
            <span class="df-toc-toggle-icon"></span>
          </div>
          <div class="df-toc-list-box">
            <ol class="df-toc-list">
              ${tocEntries.map((e) => `<li><a href="#${e.id}">${e.index}. ${escapeHtml(e.label)}</a></li>`).join('')}
            </ol>
          </div>
        </nav>`
      : '';
  cloned.querySelectorAll('details').forEach((d) => { d.open = true; });
  dfLog('buildOriginalHtml DOM aufbereitet:', {
    removedUiNodes: removedUi.length,
    markedFileCards,
    globalRefs: globalRefs.length,
    markedRefBlocks,
    removedEmptyDivs,
    tocEntries: tocEntries.length });
  const [styles, fontDataUrl] = await Promise.all([collectOriginalStyles(), getBlackChanceryDataUrl()]);
  const fontFace = fontDataUrl
    ? `@font-face { font-family: 'BlackChancery'; src: url('${fontDataUrl}') format('truetype'); font-display: swap; }`
    : '';
const overrideStyles = `
    /* ======== FONTS & ANIMATIONS ======== */
    ${fontFace}
    @property --df-angle { syntax: '<angle>'; initial-value: 0deg; inherits: false; }
    @keyframes df-rainbow-rotate { to { --df-angle: 360deg; } }
    @keyframes df-text-rainbow { from { background-position: 0% 0; } to { background-position: -200% 0; } }
    @keyframes df-scroll-flow { to { background-position: 0 -300%; } }
    @keyframes df-active-seamless { 0%   { transform: translate3d(0%, 0, 0); } 100% { transform: translate3d(-50%, 0, 0); } }
    /* ======== EXPAND / COLLAPSE & FILE HOVER ======== */
    details > *:not(summary) { display: block !important; }
    .ds-collapsible-text, [class*="collapsible" i], [class*="collapsed" i],
    [class*="clamped" i], [class*="truncated" i], [class*="fold" i] {
      max-height: none !important; overflow: visible !important; height: auto !important; }
    [class*="expand-more" i], [class*="show-more" i], [class*="read-more" i],
    [class*="expand-btn" i], [class*="collapse-btn" i] { display: none !important; }
    [data-df-file-name]:hover { outline: 1px solid #ffffff; outline-offset: 1px; }
    /* ======== SCROLLBARS & PROGRESS ======== */
    .df-toc-list::-webkit-scrollbar, .df-file-drawer-scroll::-webkit-scrollbar,
    .df-ref-list::-webkit-scrollbar { width: 0 !important; height: 0 !important; }
    .df-toc-list, .df-file-drawer-scroll, .df-ref-list {
      scrollbar-width: none !important; -ms-overflow-style: none !important; }
    .df-scroll-progress { position: absolute; right: 0; width: 8px; z-index: 10;
      background: rgba(0, 0, 0, 0); border-radius: 4px; pointer-events: none; }
    .df-scroll-thumb { width: 100%; height: 0%; background: linear-gradient( 180deg,
        #ff0055, #ff8800, #ffdd00, #00ff88, #00ddff, #8800ff, #ff00cc,
        #ff0055, #ff8800, #ffdd00, #00ff88, #00ddff, #8800ff, #ff00cc, #ff0055 );
      background-size: 100% 300%; border-radius: 4px; animation: df-scroll-flow 4s linear infinite;
      box-shadow: 0 0 8px rgba(255, 100, 200, 0.8), 0 0 16px rgba(100, 200, 255, 0.5),
        0 0 24px rgba(255, 220, 100, 0.3); transition: height 0.08s linear; }
    /* ======== TABLE OF CONTENT (TOC) ======== */
    .df-toc {
      position: fixed; top: 21px; right: 21px; width: max-content; min-width: 200px;
      max-width: min(420px, 92vw); max-height: calc(92vh - 42px);
      z-index: 999999; display: flex; flex-direction: column;
      border-radius: 14px; isolation: isolate; overflow: visible; }
    .df-toc::before {
      content: ''; position: absolute; inset: -11px; border-radius: 25px;
      background: conic-gradient(from var(--df-angle), #ff0055, #ff8800, #ffdd00, #00ff88, #00ddff, #8800ff, #ff00cc, #ff0055);
      animation: df-rainbow-rotate 4s linear infinite; filter: url(#df-electric); z-index: -1; pointer-events: none; }
    .df-toc::after {
      content: ''; position: absolute; inset: 0; border-radius: 14px; background: #000000; z-index: -1; pointer-events: none; }
    .df-toc.collapsed .df-toc-list-box { display: none; }
    .df-toc.collapsed .df-toc-header { border-bottom: none; }
    .df-toc-header {
      position: relative; display: flex; align-items: center; justify-content: center; gap: 12px;
      padding: 12px 24px; border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      cursor: pointer; user-select: none; }
    .df-toc-toggle-icon, .df-toc-title, .df-file-drawer-title, .df-file-drawer-close, .df-ref-title, .df-ref-close, .df-ref-domain {
      background: linear-gradient(90deg, #ff0055, #ff8800, #ffdd00, #00ff88, #00ddff, #8800ff, #ff00cc, #ff0055);
      background-size: 200% 100%; -webkit-background-clip: text; background-clip: text;
      -webkit-text-fill-color: transparent; color: transparent;
      animation: df-text-rainbow 4s linear infinite; }
    .df-toc-title { font-family: 'BlackChancery', sans-serif; font-size: 22px; font-weight: 700; white-space: nowrap; }
    .df-toc-toggle-icon { font-family: 'BlackChancery', sans-serif; font-size: 28px; font-weight: 700; line-height: 1; min-width: 20px; text-align: center; }
    .df-toc-toggle-icon::before { content: '+'; }
    .df-toc:not(.collapsed) .df-toc-toggle-icon::before { content: '−'; }
    .df-toc-list-box { font-family: 'BlackChancery', sans-serif; font-size: 33px; position: relative; flex: 1; min-height: 0; display: flex; flex-direction: column; overflow: hidden; border-radius: 0 0 14px 14px; }
    .df-toc-list { list-style: none; margin: 0; padding: 8px 0; overflow-y: auto; overflow-x: hidden; max-height: calc(92vh - 150px); }
    .df-toc-header:hover .df-toc-title, .df-toc-header:hover .df-toc-toggle-icon {
      filter: drop-shadow(1px 2px 3px rgba(0, 0, 0, 0.8));
      transform: scale(1.25);
      transition: transform 0.2s ease, filter 0.2s ease; }
    .df-toc-header:active { transform: translateY(0) scale(1); }
    .df-toc-list a {
      display: block; padding: 8px 16px; text-decoration: none; overflow: hidden;
      text-overflow: ellipsis; white-space: nowrap; border-left: 2px solid transparent; font-size: 13px; color: #ffffff; }
    .df-toc-list a:hover { background-color: rgba(100, 150, 255, 0.15); border-left-color: #4facfe; }
    .df-toc-list a.df-toc-active,
    .df-toc-list a.df-toc-active, .df-toc-list a.df-toc-active:hover {
      position: relative; overflow: hidden; isolation: isolate; color: #000000 !important; -webkit-text-fill-color: #000000 !important; font-weight: 600 !important;
      text-shadow: 0 0 6px rgba(255, 255, 255, 0.45) !important; border-left: 1px solid rgba(255, 255, 255, 0.45) !important; border-right: 1px solid rgba(255, 255, 255, 0.45) !important; 
      border-radius: 11px !important; background: transparent !important;
      box-shadow: 0 0 10px rgba(255, 0, 128, 0.45), 0 0 22px rgba(0, 230, 255, 0.35), inset 0 0 10px rgba(255, 255, 255, 0.18) !important; }
    .df-toc-list a.df-toc-active::before, .df-toc-list a.df-toc-active:hover::before {
      content: ''; position: absolute; top: 0; left: 0; width: 200%; height: 100%;
      background: linear-gradient( 90deg,
        #ff0066 0%, #ff7b00 7.14%, #fff200 14.28%, #00ff88 21.42%, #00e5ff 28.57%,
        #9d00ff 35.71%, #ff00cc 42.85%, #ff0066 50%, #ff7b00 57.14%, #fff200 64.28%,
        #00ff88 71.42%, #00e5ff 78.57%, #9d00ff 85.71%, #ff00cc 92.85%, #ff0066 100% );
      filter: saturate(1.45) brightness(1.12); animation: df-active-seamless 4.5s linear infinite;
      z-index: -1; pointer-events: none; }
    /* ======== DRAWER & REFERENCES OVERLAY ======== */
    .df-file-drawer, .df-ref-overlay {
      position: relative; background: #000000; border-radius: 14px; isolation: isolate; }
    .df-file-drawer::before, .df-ref-overlay::before {
      content: ''; position: absolute; inset: -11px; border-radius: 25px;
      background: conic-gradient(from var(--df-angle), #ff0055, #ff8800, #ffdd00, #00ff88, #00ddff, #8800ff, #ff00cc, #ff0055);
      animation: df-rainbow-rotate 4s linear infinite; filter: url(#df-electric); z-index: -1; pointer-events: none; }
    .df-file-drawer::after, .df-ref-overlay::after {
      content: ''; position: absolute; inset: 0; border-radius: 14px; background: #000000; z-index: -1; pointer-events: none; }
    .df-file-drawer-backdrop, .df-ref-overlay-backdrop {
      position: fixed; inset: 0; background: rgba(0, 0, 0, 0.5); z-index: 99999998; opacity: 0; transition: opacity 0.28s ease; }
    .df-file-drawer-backdrop.open, .df-ref-overlay-backdrop.open { opacity: 1; }
    .df-file-drawer {
      position: fixed !important; top: 21px !important; bottom: 21px !important; left: 21px !important;
      width: clamp(450px, 33vw, 650px) !important; max-width: 90vw !important; border-radius: 14px;
      z-index: 99999999 !important; display: flex !important; flex-direction: column !important;
      transform: translateX(-110%) !important; transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important; }
    .df-file-drawer.open { transform: translateX(0) !important; }
    .df-file-drawer-header, .df-ref-header {
      position: relative; display: flex; align-items: center; justify-content: center; border-radius: 14px;
      padding: 14px 56px; min-height: 56px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); flex-shrink: 0; }
    .df-file-drawer-title, .df-ref-title {
      font-family: 'BlackChancery', sans-serif; font-size: 24px; font-weight: 700;
      overflow: hidden; text-overflow: ellipsis; white-space: nowrap; text-align: center; }
    .df-file-drawer-close, .df-ref-close {
      position: absolute; right: 14px; top: 50%; transform: translateY(-50%);
      border: none; cursor: pointer; width: 36px; height: 36px; font-family: 'BlackChancery', sans-serif; font-size: 30px; }
    .df-file-drawer-content { position: relative; flex: 1; min-height: 0; display: flex; flex-direction: column; overflow: hidden; }
    .df-file-drawer-scroll { position: absolute; inset: 0; overflow-y: auto; overflow-x: hidden; padding: 18px 22px; }
    .df-file-drawer-pre {
      margin: 0; font-family: 'SFMono-Regular', Consolas, monospace; font-size: 13px;
      line-height: 1.55; white-space: pre-wrap; word-break: break-word; color: #ffffff !important; }
    /* ======== DRAWER PDF ======== */
    .df-pdf-warning { padding: 12px 22px; color: #f9e2af; font-size: 13px; background: rgba(249,226,175,0.1); text-align: center; }
    .df-pdf-pages { display: flex; flex-direction: column; gap: 24px; padding: 10px 0; align-items: center; }
    .df-pdf-page-wrap { position: relative; width: 100%; display: flex; justify-content: center; }
    .df-pdf-page-label {
      position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%);
      background: rgba(0,0,0,1); color: #ffffff; padding: 4px 14px; border-radius: 6px; font-size: 11px; }
    .df-pdf-page-img { display: block !important; width: 100% !important; height: auto !important; background: #ffffff !important; border-radius: 8px; }
    /* ======== REFERENCES OVERLAY ======== */
    .df-ref-overlay {
      position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0.9);
      width: min(600px, 90vw); max-height: 80vh; color: #fff; z-index: 99999999;
      display: flex; flex-direction: column; opacity: 0; transition: opacity 0.28s ease, transform 0.3s ease; }
    .df-ref-overlay.open { opacity: 1; transform: translate(-50%, -50%) scale(1); }
    .df-ref-overlay .df-ref-domain,
    .df-ref-list a {
      font-family: 'BlackChancery', sans-serif; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important;
      background: none !important; -webkit-background-clip: border-box !important; background-clip: border-box !important;
      animation: none !important; }
    .df-ref-list { list-style: none; margin: 0; padding: 8px 0; overflow-y: auto; flex: 1; }
    .df-ref-list a {
      display: flex; align-items: center; gap: 12px; padding: 10px 22px; text-decoration: none;
      font-size: 13px; border-left: 2px solid transparent; }
    .df-ref-list a:hover {
      background-color: rgba(100, 150, 255, 0.15) !important; border-left-color: #4facfe !important; }
    .df-ref-label { font-family: monospace; background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 6px; font-size: 12px; }
  `;
  const attachmentsJson = JSON.stringify(attachmentsData).replace(/<\/script/gi, '<\\/script');
  dfLog('buildOriginalHtml Assets bereit:', {
    stylesLength: styles.length,
    hasBlackChancery: Boolean(fontDataUrl),
    attachmentsJsonLength: attachmentsJson.length });
  const interactiveScript = `
  <script>
    window.__DF_FILES__ = ${attachmentsJson};
    (function () {
      const escHtml = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
      // ============ Expand & Fold Overrides ============
      document.querySelectorAll('details').forEach((d) => { d.open = true; });
      document.querySelectorAll('.ds-collapsible-text,[class*="collapsible" i],[class*="collapsed" i],[class*="clamped" i],[class*="truncated" i],[class*="fold" i]').forEach((el) => {
        el.style.setProperty('max-height', 'none', 'important');
        el.style.setProperty('overflow', 'visible', 'important');
        el.style.setProperty('height', 'auto', 'important'); });
      document.querySelectorAll('[class*="expand" i],[class*="more" i]').forEach((btn) => {
        if (/mehr|more|weniger|less|anzeigen|show/i.test(btn.textContent || '')) {
          btn.style.setProperty('display', 'none', 'important'); } });
      // ============ Code Copy & Download ============
      document.addEventListener('click', (e) => {
        const btn = e.target.closest('button');
        if (!btn) return;
        const label = ((btn.getAttribute('aria-label') || '') + ' ' + (btn.getAttribute('title') || '') + ' ' + (btn.textContent || '')).toLowerCase();
        const isCopy = /copy|kopier|clipboard/.test(label);
        const isDownload = /download|herunterladen/.test(label);
        if (!isCopy && !isDownload) return;
        let pre = btn.closest('pre') || btn.closest('[class*="code" i]')?.querySelector('pre');
        for (let p = btn.parentElement, i = 0; i < 5 && p && !pre; i++, p = p.parentElement) pre = p.querySelector('pre');
        if (!pre) return;
        e.preventDefault();
        e.stopPropagation();
        const text = pre.textContent || '';
        if (isDownload) {
          const url = URL.createObjectURL(new Blob([text], { type: 'text/plain' }));
          const a = Object.assign(document.createElement('a'), { href: url, download: 'code-' + Date.now() + '.txt' });
          a.click();
          setTimeout(() => URL.revokeObjectURL(url), 1000);
          return; }
        navigator.clipboard?.writeText(text).then(() => {
          const old = btn.innerHTML;
          btn.textContent = 'Kopiert!';
          setTimeout(() => { btn.innerHTML = old; }, 1500); }); });
      // ============ TOC Toggle & Scrollspy ============
      const tocHeader = document.getElementById('df-toc-header');
      const tocNav = document.getElementById('df-toc');
      const tocList = tocNav?.querySelector('.df-toc-list');
      tocHeader?.addEventListener('click', () => tocNav?.classList.toggle('collapsed'));
      const tocLinks = Array.from(document.querySelectorAll('.df-toc a[href^="#"]'));
      const scrollTocLinkIntoView = (link) => {
        if (!link || !tocList || !tocNav || tocNav.classList.contains('collapsed')) return;
        const listRect = tocList.getBoundingClientRect();
        const linkRect = link.getBoundingClientRect();
        const pad = 16;
        if (linkRect.bottom > listRect.bottom - pad) {
          tocList.scrollTop += linkRect.bottom - (listRect.bottom - pad); } 
          else if (linkRect.top < listRect.top + pad) {
          tocList.scrollTop -= (listRect.top + pad) - linkRect.top; } };
      const setActiveToc = (id) => {
        let activeLink = null;
        tocLinks.forEach((l) => {
          const isMatch = l.getAttribute('href') === '#' + id;
          l.classList.toggle('df-toc-active', isMatch);
          if (isMatch) activeLink = l; });
        scrollTocLinkIntoView(activeLink); };
      tocLinks.forEach((a) => {
        a.addEventListener('click', (e) => {
          e.preventDefault();
          const href = a.getAttribute('href');
          const target = document.querySelector(href);
          if (!target) return;
          setActiveToc(href.slice(1));
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          const oldBg = target.style.backgroundColor;
          target.style.transition = 'background-color 0.3s';
          target.style.backgroundColor = 'rgba(79, 172, 254, 0.15)';
          setTimeout(() => { target.style.backgroundColor = oldBg; }, 1200); }); });
      const tocObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && entry.target.id) setActiveToc(entry.target.id); }); }, { rootMargin: '-20% 0px -70% 0px', threshold: 0 });
      tocLinks.forEach((a) => {
        const target = document.querySelector(a.getAttribute('href'));
        if (target) tocObserver.observe(target); });
      // ============ References & File Drawer Modals ============
      const mountModal = (backdropClass, boxClass, innerHtml, closeSelector) => {
        if (document.querySelector('.' + boxClass)) return;
        const backdrop = Object.assign(document.createElement('div'), { className: backdropClass });
        const box = Object.assign(document.createElement('div'), { className: boxClass, innerHTML: innerHtml });
        document.body.append(backdrop, box);
        void box.offsetWidth;
        backdrop.classList.add('open');
        box.classList.add('open');
        let closed = false;
        const close = () => {
          if (closed) return;
          closed = true;
          backdrop.classList.remove('open');
          box.classList.remove('open');
          document.removeEventListener('keydown', onEsc);
          setTimeout(() => { backdrop.remove(); box.remove(); }, 320); };
        const onEsc = (e) => { if (e.key === 'Escape') close(); };
        box.querySelector(closeSelector)?.addEventListener('click', close);
        backdrop.addEventListener('click', close);
        document.addEventListener('keydown', onEsc); };
      document.addEventListener('click', (e) => {
        const refBlock = e.target.closest('[data-df-references]');
        if (refBlock) {
          let refs = [];
          try { refs = JSON.parse(refBlock.getAttribute('data-df-references')); } catch {}
          if (!Array.isArray(refs) || refs.length === 0) return;
          e.preventDefault();
          const items = refs.map((r) => {
            let domain = '';
            try { domain = new URL(r.href).hostname.replace(/^www\\./, ''); } catch {}
            return '<li><a href="' + escHtml(r.href) + '" target="_blank" rel="noopener noreferrer">' +
              '<span class="df-ref-label">[' + escHtml(r.label) + ']</span>' +
              '<span class="df-ref-domain">' + escHtml(domain) + '</span></a></li>';
          }).join('');
          mountModal(
            'df-ref-overlay-backdrop',
            'df-ref-overlay',
            '<div class="df-ref-header"><span class="df-ref-title">Quellen (' + refs.length + ')</span><button class="df-ref-close" type="button">×</button></div><ol class="df-ref-list">' + items + '</ol>',
            '.df-ref-close' );
          return; }
        const card = e.target.closest('[data-df-file-name]');
        if (card) {
          const name = card.getAttribute('data-df-file-name');
          const files = window.__DF_FILES__ || {};
          if (!(name in files)) return;
          const content = files[name];
          let contentInner = '<pre class="df-file-drawer-pre">[Kein Inhalt verfügbar]</pre>';
          if (typeof content === 'string') {
            contentInner = '<div class="df-file-drawer-scroll"><pre class="df-file-drawer-pre">' + escHtml(content) + '</pre></div>'; } 
            else if (content?.type === 'pdf' && Array.isArray(content.pages)) {
            const total = content.total || content.pages.length;
            const warn = total > content.pages.length ? '<div class="df-pdf-warning">⚠️ ' + content.pages.length + ' von ' + total + ' Seiten gerendert</div>' : '';
            contentInner = warn + '<div class="df-file-drawer-scroll"><div class="df-pdf-pages">' +
              content.pages.map((p) => '<div class="df-pdf-page-wrap"><div class="df-pdf-page-label">Seite ' + p.index + '</div><img class="df-pdf-page-img" src="' + p.src + '" loading="lazy" /></div>').join('') +
              '</div></div>'; }
          mountModal(
            'df-file-drawer-backdrop',
            'df-file-drawer',
            '<div class="df-file-drawer-header"><div class="df-file-drawer-title">' + escHtml(name) + '</div><button class="df-file-drawer-close" type="button">×</button></div><div class="df-file-drawer-content">' + contentInner + '</div>',
            '.df-file-drawer-close' ); } });
      // ============ Scroll Progress Bars ============
      function attachScrollProgress(container) {
        if (!container || container.dataset.dfScrollAttached) return;
        container.dataset.dfScrollAttached = '1';
        const parent = container.parentNode;
        if (!parent) return;
        if (getComputedStyle(parent).position === 'static') {
          parent.style.position = 'relative'; }
        const progress = document.createElement('div');
        progress.className = 'df-scroll-progress';
        const thumb = document.createElement('div');
        thumb.className = 'df-scroll-thumb';
        progress.appendChild(thumb);
        parent.appendChild(progress);
        const update = () => {
          progress.style.top = container.offsetTop + 'px';
          progress.style.height = container.offsetHeight + 'px';
          const max = container.scrollHeight - container.clientHeight;
          const ratio = max > 0 ? (container.scrollTop / max) : 0;
          thumb.style.height = (ratio * 100) + '%'; };
        container.addEventListener('scroll', update, { passive: true });
        window.addEventListener('resize', update, { passive: true });
        if (typeof ResizeObserver !== 'undefined') {
          new ResizeObserver(update).observe(container); }
        update(); }
      function initScrollProgressBars() {
        const selectors = ['.df-toc-list', '.df-file-drawer-scroll', '.df-ref-list'];
        const seen = new WeakSet();
        let rafScheduled = false;
        const scan = () => {
          rafScheduled = false;
          selectors.forEach((sel) => {
            document.querySelectorAll(sel).forEach((el) => {
              if (!seen.has(el)) { seen.add(el); attachScrollProgress(el); } }); }); };
        const scheduleScan = () => {
          if (rafScheduled) return;
          rafScheduled = true;
          requestAnimationFrame(scan); };
        scan();
        if (typeof MutationObserver !== 'undefined' && document.body) {
          new MutationObserver(scheduleScan).observe(document.body, { childList: true, subtree: true }); } }
      initScrollProgressBars(); })();
  <\/script>`;
  const htmlOutput = `<!DOCTYPE html>
<html lang="de" class="${document.documentElement.className}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${escapeHtml(getConversationTitle())}</title>
  <style>${styles}\n${overrideStyles}</style>
</head>
<body class="${document.body.className}">
  ${ELECTRIC_FILTER_SVG}
  ${tocHtml}
  ${cloned.outerHTML}
  ${interactiveScript}
</body>
</html>`;
  dfLog('buildOriginalHtml fertig:', { totalHtmlLength: htmlOutput.length, tocCount: tocEntries.length });
  return htmlOutput; }
// ============================================================================
// 10. EXPORT-ORCHESTRIERUNG & BOOTSTRAP
// ============================================================================
function buildExportPayload(exportData) {
  const rawMessages = Array.isArray(exportData?.messages) ? exportData.messages : [];
  return {
    title: exportData?.title || getDefaultConversationTitle(),
    url: exportData?.url || window.location.href,
    date: exportData?.date || new Date().toISOString(),
    messages: rawMessages.map((msg) => {
      const formattedMsg = { role: msg.role, content: msg.content };
      if (msg.role === 'user' && msg.attachments?.length) formattedMsg.attachments = msg.attachments;
      if (msg.role === 'assistant' && msg.chain_of_thought) formattedMsg.chain_of_thought = msg.chain_of_thought;
      return formattedMsg; }) }; }
async function collectAllMessagesFromChat(options = {}) {
  let captured = null;
  let attachmentsData = {};
  const t0 = Date.now();
  dfLog('collectAllMessagesFromChat Start:', { captureAttachments: Boolean(options?.captureAttachments) });
  try {
    updateExportingOverlay('Activate print mode ');
    window.dispatchEvent(new Event('beforeprint'));
    dfLog('beforeprint Event ausgelöst, warte ' + BEFOREPRINT_DELAY_MS + 'ms.');
    await delay(BEFOREPRINT_DELAY_MS);
    if (!isExtensionContextValid()) {
      dfWarn('Extension-Kontext während beforeprint-Wartezeit ungültig geworden.');
      return { title: getConversationTitle(), messages: [], attachmentsData: {} }; }
    const expandedCount = document.querySelectorAll(DF_SELECTORS.message).length;
    dfLog('Gefundene .ds-message Elemente:', expandedCount);
    if (expandedCount === 0) {
      dfWarn('Keine Nachrichten im DOM gefunden.');
      return { title: getConversationTitle(), messages: [], attachmentsData: {} }; }
    updateExportingOverlay('Prepare diagrams ');
    await waitForDiagramBlocksReady(DIAGRAM_READY_TIMEOUT_MS);
    await prepareDiagramCodeBlocks();
    updateExportingOverlay(`Collect ${expandedCount} messages `);
    await delay(300);
    captured = extractAllMessagesFromPage(document, { cloneDomNodes: true });
    if (options.captureAttachments) {
      updateExportingOverlay('Collect file attachments ');
      attachmentsData = await captureAttachmentContents(); } } 
  finally {
    try { window.dispatchEvent(new Event('afterprint')); } 
    catch (afterErr) {
      dfLog('afterprint Event Fehler ignoriert:', afterErr); }
    clearToasts();
    await delay(AFTERPRINT_DELAY_MS);
    dfLog('collectAllMessagesFromChat beendet:', {
      elapsedMs: Date.now() - t0,
      extractedMessages: Array.isArray(captured?.messages) ? captured.messages.length : 0,
      attachmentKeys: Object.keys(attachmentsData || {}) }); }
  return {
    title: captured?.title || getConversationTitle(),
    messages: Array.isArray(captured?.messages) ? captured.messages : [],
    attachmentsData }; }
async function downloadChat(exportData, format, settings) {
  const formattedData = buildExportPayload(exportData);
  const safeTitle = sanitizeFilename((formattedData.title || '').trim() || getDefaultConversationTitle());
  const normalizedFormat = ['markdown', 'text', 'html', 'json'].includes(format) ? format : 'json';
  dfLog('downloadChat Start:', { format: normalizedFormat, safeTitle, messageCount: formattedData.messages.length });
  let blob;
  let filename;
  if (normalizedFormat === 'markdown') {
    blob = new Blob([convertToMarkdown(formattedData, settings)], { type: 'text/markdown;charset=utf-8' });
    filename = `${safeTitle}.md`; } 
    else if (normalizedFormat === 'text') {
    blob = new Blob([convertToPlainText(formattedData, settings)], { type: 'text/plain;charset=utf-8' });
    filename = `${safeTitle}.txt`; } 
    else if (normalizedFormat === 'html') {
    clearToasts();
    updateExportingOverlay('Collect original styles ');
    const html = await buildOriginalHtml(exportData.attachmentsData || {});
    blob = new Blob([html], { type: 'text/html;charset=utf-8' });
    filename = `${safeTitle}.html`; } 
    else {
    const json = JSON.stringify(convertToJSON(formattedData, settings), null, 2);
    blob = new Blob([json], { type: 'application/json;charset=utf-8' });
    filename = `${safeTitle}.json`; }
  const url = URL.createObjectURL(blob);
  const a = Object.assign(document.createElement('a'), { href: url, download: filename });
  a.style.display = 'none';
  (document.body || document.documentElement).appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  dfLog('downloadChat Download ausgelöst:', { filename, sizeBytes: blob.size });
  const exportButton = document.getElementById('deepseek-export-btn');
  if (exportButton) {
    exportButton.classList.add('pulse');
    setTimeout(() => exportButton.classList.remove('pulse'), 600); } }
let isExporting = false;
async function exportChat(format) {
  if (isExporting) {
    dfWarn('Export läuft bereits. Bitte warten.');
    return; }
  if (!isExtensionContextValid()) {
    hideExportingOverlay();
    dfWarn('Extension wurde neu geladen. Bitte die Seite neu laden (F5).');
    return; }
  isExporting = true;
  const t0 = Date.now();
  dfLog('exportChat gestartet:', { format, url: window.location.href });
  showExportingOverlay('Loading all messages');
  try {
    const settings = await getSettings();
    dfLog('exportChat Einstellungen geladen:', settings);
    const { title, messages, attachmentsData } = await collectAllMessagesFromChat({
      captureAttachments: format === 'html' });
    if (!isExtensionContextValid()) {
      hideExportingOverlay();
      dfWarn('Extension wurde während des Exports neu geladen. Bitte die Seite neu laden (F5).');
      return; }
    if (messages.length === 0) {
      hideExportingOverlay();
      dfWarn('Keine Nachrichten zum Exportieren gefunden.');
      return; }
    updateExportingOverlay('Create file ');
    await downloadChat(
      { title, url: window.location.href, date: new Date().toISOString(), messages, attachmentsData },
      format,
      settings );
    hideExportingOverlay();
    dfLog('exportChat erfolgreich abgeschlossen:', { format, title, elapsedMs: Date.now() - t0 }); } 
    catch (error) {
    hideExportingOverlay();
    dfError('Fehler beim Export.', error); } 
    finally {
    isExporting = false; } }
function init() {
  if (!isDeepSeekChatPage()) {
    dfLog('init übersprungen: Keine DeepSeek-Chat-Seite.', window.location.hostname);
    return; }
  if (document.documentElement?.dataset?.dfInitialized === '1') {
    dfLog('init übersprungen: Bereits initialisiert.');
    return; }
  try {
    dfLog('init startet DeepForge UI:', { readyState: document.readyState });
    injectElectricFilters();
    injectExportButton();
    if (document.documentElement) document.documentElement.dataset.dfInitialized = '1';
    dfLog('init abgeschlossen.'); } 
    catch (error) {
    dfError('Extension konnte nicht geladen werden.', error); } }
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init); } 
  else {
  init(); }