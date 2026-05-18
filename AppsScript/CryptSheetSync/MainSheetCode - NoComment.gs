// ===================================================================================================
//                                      CONFIGURATION 
// ===================================================================================================
const SOURCE_FILE_ID = "SHEET-ID";
const MASTER_SHEET_NAME = "Main";
const TEMP_SHEET_REGEX = /^\d+$/;
const CLEANUP_INTERVAL_MINUTES = 1;
const PREFIX_MAP = {
  "A2": ["ClassName - "],
  //"A2": ["ClassName - "],
};
// ===================================================================================================
//                                      CONFIGURATION 
// ===================================================================================================
// ===================================================================================================
//                                      ENCRYPTION
// ===================================================================================================
const ENCRYPTION_MAP = {
  'A': 'F', 'B': 'G', 'C': 'H', 'D': 'I', 'E': 'J',
  'F': 'K', 'G': 'L', 'H': 'M', 'I': 'N', 'J': 'O',
  'K': 'P', 'L': 'Q', 'M': 'R', 'N': 'S', 'O': 'T',
  'P': 'U', 'Q': 'V', 'R': 'W', 'S': 'X', 'T': 'Y',
  'U': 'Z', 'V': 'A', 'W': 'B', 'X': 'C', 'Y': 'D', 'Z': 'E',
  'a': 'f', 'b': 'g', 'c': 'h', 'd': 'i', 'e': 'j',
  'f': 'k', 'g': 'l', 'h': 'm', 'i': 'n', 'j': 'o',
  'k': 'p', 'l': 'q', 'm': 'r', 'n': 's', 'o': 't',
  'p': 'u', 'q': 'v', 'r': 'w', 's': 'x', 't': 'y',
  'u': 'z', 'v': 'a', 'w': 'b', 'x': 'c', 'y': 'd', 'z': 'e',
  '0': '9', '1': '8', '2': '7', '3': '6', '4': '5',
  '5': '4', '6': '3', '7': '2', '8': '1', '9': '0'};
const DECRYPTION_MAP = {};
for (const [key, value] of Object.entries(ENCRYPTION_MAP)) {
  DECRYPTION_MAP[value] = key;}
function encryptText(text) {
  let result = '';
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    result += ENCRYPTION_MAP[char] || char;  }
  return result;}
function decryptText(text) {
  let result = '';
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    result += DECRYPTION_MAP[char] || char;  }
  return result;}
function findSheetWithDecryption(sourceFile, selectedSheetName) {
  let sourceSheet = sourceFile.getSheetByName(selectedSheetName);
  if (sourceSheet) return { sheet: sourceSheet, wasEncrypted: false };
  const encryptedName = encryptText(selectedSheetName);
  sourceSheet = sourceFile.getSheetByName(encryptedName);
  if (sourceSheet) return { sheet: sourceSheet, wasEncrypted: true };
  return null;}
function decryptImportedData(sheet) {
  try {
    const cellA1 = sheet.getRange("A1");
    const value = cellA1.getValue();
    if (value !== null && value !== "" && value.toString().trim() !== "") {
      cellA1.setValue(decryptText(value.toString()));    }
  } catch (e) {}}
// ===================================================================================================
//                                      ENCRYPTION
// ===================================================================================================
// ===================================================================================================
//                                      IMPORT
// ===================================================================================================
function importiereSheetProUser(selectedSheetName) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sourceFile = SpreadsheetApp.openById(SOURCE_FILE_ID);
  const sheetResult = findSheetWithDecryption(sourceFile, selectedSheetName);
  if (!sheetResult) {
    console.error("Sheet nicht gefunden: " + selectedSheetName);
    SpreadsheetApp.getUi().alert("❌ Sheet nicht gefunden: " + selectedSheetName);
    return;  }
  const sourceSheet = sheetResult.sheet;
  const wasEncrypted = sheetResult.wasEncrypted;
  let lastRow = sourceSheet.getLastRow();
  let lastCol = sourceSheet.getLastColumn();
  if (lastRow < 1 || lastCol < 1) return;
  let nextIndex = 0;
  ss.getSheets().forEach(s => {
    const match = s.getName().match(TEMP_SHEET_REGEX);
    if (match) {
      const num = parseInt(match[0], 10);
      if (num >= nextIndex) nextIndex = num + 1;    }  });
  const newSheetName = `${nextIndex}`;
  const newSheet = sourceSheet.copyTo(ss);
  newSheet.setName(newSheetName);
  if (wasEncrypted) {
    decryptImportedData(newSheet);  }
  ss.setActiveSheet(newSheet);
  newSheet.showSheet();
  markSheetCreated();
  updateMasterSheetCounter();
  updateMasterSheetLastTime();
  return newSheet;}
// ===================================================================================================
//                                      IMPORT
// ===================================================================================================
// ===================================================================================================
//                                      SMART 🌙 FILTER
// ===================================================================================================
function applyMoonFilterFast(sheet) {
  const lastRow = sheet.getLastRow();
  const lastCol = sheet.getLastColumn();
  if (lastRow < 2) return;
  const data = sheet.getRange(2, 2, lastRow - 1, lastCol - 1).getValues();
  const headerRow = sheet.getRange(2, 1, 1, lastCol).getValues()[0];
  sheet.showRows(2, lastRow - 1);
  data.forEach((row, i) => {
    const hasMoon = row.some(cell => String(cell).includes("🌙") || String(cell).trim() !== "");
    const hasHeaderContent = headerRow.some(headerCell => {
      const headerValue = String(headerCell).trim();
      if (!headerValue) return false;
      return row.some(dataCell => String(dataCell) === headerValue);    });
    if (!hasMoon && !hasHeaderContent) {
      sheet.hideRows(i + 2);    }  });}
// ===================================================================================================
//                                      SMART 🌙 FILTER
// ===================================================================================================
// ===================================================================================================
//                                      TIME RECORDING
// ===================================================================================================
function markSheetCreated() {
  const props = PropertiesService.getScriptProperties();
  props.setProperty("lastSheetCreated", new Date().toISOString());}
function updateMasterSheetCounter() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const masterSheet = ss.getSheetByName(MASTER_SHEET_NAME);
  if (!masterSheet) return;
  const counterCell = masterSheet.getRange("A3");
  let count = counterCell.getValue();
  if (typeof count !== "number") count = 0;
  count += 1;
  counterCell.setValue(count);}
function formatDateForMasterSheet(date) {
  const d = new Date(date);
  const day = String(d.getDate()).padStart(2, "0");
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const year = d.getFullYear();
  const hours = String(d.getHours()).padStart(2, "0");
  const minutes = String(d.getMinutes()).padStart(2, "0");
  const seconds = String(d.getSeconds()).padStart(2, "0");
  return `${day}.${month}.${year}_${hours}:${minutes}:${seconds}`;}
function updateMasterSheetLastTime() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const masterSheet = ss.getSheetByName(MASTER_SHEET_NAME);
  if (!masterSheet) return;
  const lastCreatedISO = PropertiesService.getScriptProperties().getProperty("lastSheetCreated");
  if (!lastCreatedISO) return;
  const formattedDate = formatDateForMasterSheet(lastCreatedISO);
  masterSheet.getRange("B3").setValue(formattedDate);}
// ===================================================================================================
//                                      TIME RECORDING
// ===================================================================================================
// ===================================================================================================
//                                      CLEANUP
// ===================================================================================================
function deleteIfInactive() {
  const props = PropertiesService.getScriptProperties();
  const lastCreated = props.getProperty("lastSheetCreated");
  if (!lastCreated) return;
  const lastDate = new Date(lastCreated);
  const now = new Date();
  const diffMinutes = (now - lastDate) / 1000 / 60;
  if (diffMinutes >= CLEANUP_INTERVAL_MINUTES) {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    ss.getSheets().forEach(sheet => {
      if (sheet.getName() !== MASTER_SHEET_NAME && TEMP_SHEET_REGEX.test(sheet.getName())) {
        ss.deleteSheet(sheet);      }    });
    props.deleteProperty("lastSheetCreated");  }}
// ===================================================================================================
//                                      CLEANUP
// ===================================================================================================
// ===================================================================================================
//                                      TRIGGER
// ===================================================================================================
function createTriggers() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  // Bestehende Trigger löschen, um Doppelungen zu vermeiden
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger("onEditHandler")
    .forSpreadsheet(ss)
    .onEdit()
    .create();
  ScriptApp.newTrigger("deleteIfInactive")
    .timeBased()
    .everyMinutes(CLEANUP_INTERVAL_MINUTES)
    .create();}
// ===================================================================================================
//                                      TRIGGER
// ===================================================================================================
// ===================================================================================================
//                                      onEdit WITH PROTECTION
// ===================================================================================================
function onEditHandler(e) {
  if (!e) return;
  const props = PropertiesService.getScriptProperties();
  if (props.getProperty("isProcessing") === "true") return;
  props.setProperty("isProcessing", "true");
  try {
    const sheet = e.range.getSheet();
    if (sheet.getName() !== MASTER_SHEET_NAME) return;
    const cell = e.range.getA1Notation();
    let selectedSheet = e.range.getValue();
    if (!selectedSheet) return;
    let applyFilter = false;
    if (selectedSheet.endsWith("🌙")) {
      applyFilter = true;
      selectedSheet = selectedSheet.replace("🌙", "").trim();    }
    let newSheet = null;
    let needsDecryption = false;
    const prefixes = PREFIX_MAP[cell];

    if (prefixes && prefixes.length > 0) {
      const decryptedSelected = decryptText(selectedSheet);

      for (const prefix of prefixes) {
        const encryptedPrefix = encryptText(prefix);

        // 1. Klartext-Präfix + Original-Dropdown
        let result = tryImportSheet(prefix + selectedSheet);
        if (result) {
          newSheet = result.sheet;
          needsDecryption = result.wasEncrypted;
          break;        }

        result = tryImportSheet(encryptedPrefix + selectedSheet);
        if (result) {
          newSheet = result.sheet;
          needsDecryption = true;
          break;        }
        result = tryImportSheet(prefix + decryptedSelected);
        if (result) {
          newSheet = result.sheet;
          needsDecryption = result.wasEncrypted;
          break;        }
        result = tryImportSheet(encryptedPrefix + decryptedSelected);
        if (result) {
          newSheet = result.sheet;
          needsDecryption = true;
          break;        }      }
    } else {
      const result = tryImportSheet(selectedSheet);
      if (result) {
        newSheet = result.sheet;
        needsDecryption = result.wasEncrypted;      }    }
    if (!newSheet) {
      SpreadsheetApp.getUi().alert("❌ Sheet nicht gefunden: " + selectedSheet);
      return;    }
    if (needsDecryption) {
      decryptImportedData(newSheet);    }
    if (applyFilter) {
      applyMoonFilterFast(newSheet);    }
  } finally {
    props.deleteProperty("isProcessing");  }}
// ===================================================================================================
//                                      onEdit WITH PROTECTION
// ===================================================================================================
// ===================================================================================================
//                                      importSheetProUser
// ===================================================================================================
function tryImportSheet(selectedSheetName) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sourceFile = SpreadsheetApp.openById(SOURCE_FILE_ID);
  const sheetResult = findSheetWithDecryption(sourceFile, selectedSheetName);
  if (!sheetResult) return null;
  const sourceSheet = sheetResult.sheet;
  const wasEncrypted = sheetResult.wasEncrypted;
  let lastRow = sourceSheet.getLastRow();
  let lastCol = sourceSheet.getLastColumn();
  if (lastRow < 1 || lastCol < 1) return null;
  let nextIndex = 0;
  ss.getSheets().forEach(s => {
    const match = s.getName().match(TEMP_SHEET_REGEX);
    if (match) {
      const num = parseInt(match[0], 10);
      if (num >= nextIndex) nextIndex = num + 1;    }  });
  const newSheetName = `${nextIndex}`;
  const newSheet = sourceSheet.copyTo(ss);
  newSheet.setName(newSheetName);
  ss.setActiveSheet(newSheet);
  newSheet.showSheet();
  markSheetCreated();
  updateMasterSheetCounter();
  updateMasterSheetLastTime();
  return { sheet: newSheet, wasEncrypted: wasEncrypted };}
// ===================================================================================================
//                                      importSheetProUser
// ===================================================================================================
