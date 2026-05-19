// ===================================================================================================
//                                   SIMPLE ENCRYPTION 
// ===================================================================================================
const ENCRYPTION_MAP = {
  'A': 'F', 'B': 'G', 'C': 'H', 'D': 'I', 'E': 'J', 
  'F': 'K', 'G': 'L', 'H': 'M', 'I': 'N', 'J': 'O',
  'K': 'P', 'L': 'Q', 'M': 'R', 'N': 'S', 'O': 'T',
  'P': 'U', 'Q': 'V', 'R': 'W', 'S': 'X', 'T': 'Y',
  'U': 'Z', 'V': 'A', 'W': 'B', 'X': 'C', 'Y': 'D', 
  'Z': 'E',
  'a': 'f', 'b': 'g', 'c': 'h', 'd': 'i', 'e': 'j',
  'f': 'k', 'g': 'l', 'h': 'm', 'i': 'n', 'j': 'o',
  'k': 'p', 'l': 'q', 'm': 'r', 'n': 's', 'o': 't',
  'p': 'u', 'q': 'v', 'r': 'w', 's': 'x', 't': 'y',
  'u': 'z', 'v': 'a', 'w': 'b', 'x': 'c', 'y': 'd', 
  'z': 'e',
  '0': '9', '1': '8', '2': '7', '3': '6', '4': '5',
  '5': '4', '6': '3', '7': '2', '8': '1', '9': '0'};
const DECRYPTION_MAP = {};
for (const [key, value] of Object.entries(ENCRYPTION_MAP)) {
  DECRYPTION_MAP[value] = key;}
// ===================================================================================================
//                                   SIMPLE ENCRYPTION 
// ===================================================================================================
// ===================================================================================================
//                                   ENCRYPTION FUNCTIONS 
// ===================================================================================================
function encryptText(text) {
  let result = '';
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    result += ENCRYPTION_MAP[char] || char;}
  return result;}
function decryptText(text) {
  let result = '';
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    result += DECRYPTION_MAP[char] || char;}
  return result;}
// ===================================================================================================
//                                  ENCRYPTION FUNCTIONS 
// ===================================================================================================
// ===================================================================================================
//                                         MAINFUNCTION  
// ===================================================================================================
function encryptAllSheets() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheets = ss.getSheets();
  let encryptedCount = 0;
  sheets.forEach(sheet => {
    const originalName = sheet.getName();
    const encryptedName = encryptText(originalName);
    try {
      sheet.setName(encryptedName);
      console.log(`✅ Sheetname verschlüsselt: ${originalName} -> ${encryptedName}`);} 
      catch (e) {
      console.log(`❌ Sheetname konnte nicht geändert werden: ${originalName}`);}
    if (encryptCellA1(sheet)) {
      encryptedCount++;}});
  SpreadsheetApp.getUi().alert(`✅ Verschlüsselung abgeschlossen!\n\n• ${sheets.length} Sheetnamen verschlüsselt\n• ${encryptedCount} Zellen A1 verschlüsselt`);}
function decryptAllSheets() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheets = ss.getSheets();
  let decryptedCount = 0;
  sheets.forEach(sheet => {
    const currentName = sheet.getName();
    const decryptedName = decryptText(currentName);
    try {
      sheet.setName(decryptedName);
      console.log(`✅ Sheetname entschlüsselt: ${currentName} -> ${decryptedName}`);} 
      catch (e) {
      console.log(`❌ Sheetname konnte nicht entschlüsselt werden: ${currentName}`);}
    if (decryptCellA1(sheet)) {
      decryptedCount++;}});
  SpreadsheetApp.getUi().alert(`✅ Entschlüsselung abgeschlossen!\n\n• ${sheets.length} Sheetnamen entschlüsselt\n• ${decryptedCount} Zellen A1 entschlüsselt`);}
// ===================================================================================================
//                                         MAINFUNCTION  
// ===================================================================================================
// ===================================================================================================
//                                         CELL FUNCTIONS  
// ===================================================================================================
function encryptCellA1(sheet) {
  try {
    const cellA1 = sheet.getRange("A1");
    const value = cellA1.getValue();
    if (value !== null && value !== "" && value.toString().trim() !== "") {
      const displayValue = cellA1.getDisplayValue();
      cellA1.setValue(encryptText(displayValue));
      console.log(`✅ A1 verschlüsselt in Sheet: ${sheet.getName()}`);
      return true;}} 
    catch (e) {
    console.log(`❌ A1 konnte nicht verschlüsselt werden in Sheet: ${sheet.getName()}`);}
  return false;}
function decryptCellA1(sheet) {
  try {
    const cellA1 = sheet.getRange("A1");
    const value = cellA1.getValue();
    if (value !== null && value !== "" && value.toString().trim() !== "") {
      cellA1.setValue(decryptText(value.toString()));
      console.log(`✅ A1 entschlüsselt in Sheet: ${sheet.getName()}`);
      return true;}} 
    catch (e) {
    console.log(`❌ A1 konnte nicht entschlüsselt werden in Sheet: ${sheet.getName()}`);}
  return false;}
// ===================================================================================================
//                                         CELL FUNCTIONS  
// ===================================================================================================
// ===================================================================================================
//                                            CONFIGURATION  
// ===================================================================================================
function showEncryptionConfig() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheets = ss.getSheets();
  let sheetInfo = "";
  sheets.forEach(sheet => {
    const name = sheet.getName();
    const cellA1 = sheet.getRange("A1").getValue();
    const hasA1Content = cellA1 && cellA1.toString().trim() !== "";
    sheetInfo += `📊 ${name} 📊\n`;
    if (hasA1Content) {
      sheetInfo += `   A1: "${cellA1.toString().substring(0, 30)}${cellA1.toString().length > 30 ? '...' : ''}"\n`;} 
    else {
      sheetInfo += `   A1: "◻️ Leer"\n`;}
    sheetInfo;});
  const message = `🔐 VERSCHLÜSSELUNGSKONFIGURATION 🔐
⚙️ VERSCHLÜSSELUNG ⚙️
  • Alle Sheetnamen
  • Alle Zellen A1
📋 AKTUELLE SHEETS 📋
${sheetInfo}`;
  SpreadsheetApp.getUi().alert(message);}
// ===================================================================================================
//                                            CONFIGURATION  
// ===================================================================================================
// ===================================================================================================
//                                             MENU-FUNCTION  
// ===================================================================================================
function onOpen() {
  SpreadsheetApp.getUi().createMenu('🔐 Encrypt 🔐')
    .addItem('🔄 Alle verschlüsseln 🔄', 'encryptAllSheets')
    .addItem('🔓 Alle entschlüsseln 🔓', 'decryptAllSheets')
    .addSeparator()
    .addItem('📊 Konfiguration anzeigen 📊', 'showEncryptionConfig')
    .addToUi();}
// ===================================================================================================
//                                             MENU-FUNCTION  
// ===================================================================================================
