// Mücahid Emin Tomakin - https://mucahid-emin-tomakin.vercel.app/
// DeepForge - https://github.com/mucahid-emin-tomakin/AutoMate/tree/main/ChromeExtension/DeepForge/
// background.js

// ======== BACKGROUND FETCH PROXY ========
chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (!message?.action || !message?.url) return false;
  if (message.action === 'fetchText' || message.action === 'fetchDataUrl') {
    fetch(message.url, { credentials: 'omit' })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return message.action === 'fetchText' ? res.text() : res.blob(); })
      .then((payload) => {
        if (message.action === 'fetchText') {
          sendResponse({ ok: true, text: payload });
          return; }
        const reader = new FileReader();
        reader.onloadend = () => sendResponse({ ok: true, dataUrl: reader.result });
        reader.onerror = () => sendResponse({ ok: false, error: 'FileReader failed' });
        reader.readAsDataURL(payload); })
      .catch((err) => sendResponse({ ok: false, error: String(err) }));
    return true; }
  return false; });