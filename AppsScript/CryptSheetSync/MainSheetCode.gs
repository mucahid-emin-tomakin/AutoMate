// ===================================================================================================
//                                      CONFIGURATION 
// ===================================================================================================
// CONFIGURATION
// All adjustable parameters for the import process
const SOURCE_FILE_ID = "SHEET-ID";                                  // ID of the source spreadsheet
const MASTER_SHEET_NAME = "Main";                                   // Sheet that contains the dropdowns
const TEMP_SHEET_REGEX = /^\d+$/;                                   // Pattern for temporary sheet names (numbers only)
const CLEANUP_INTERVAL_MINUTES = 1;                                 // Minutes of inactivity before cleanup
const PREFIX_MAP = {                                                // Prefixes per cell – each array item is tried in order
  "A2": ["ClassName - "],};
// ===================================================================================================
//                                      CONFIGURATION 
// ===================================================================================================
// ===================================================================================================
//                                      ENCRYPTION
// ===================================================================================================
// ENCRYPTION
// Simple substitution cipher for sheet names and cell A1
// Encryption map: each character is mapped to another
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
const DECRYPTION_MAP = {};                                          // Reverse map, built automatically
for (const [key, value] of Object.entries(ENCRYPTION_MAP)) {
  DECRYPTION_MAP[value] = key;}
// Encrypt a string using the substitution map
function encryptText(text) {
  let result = '';
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    result += ENCRYPTION_MAP[char] || char;  }
  return result;}
// Decrypt a string using the reverse map
function decryptText(text) {
  let result = '';
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    result += DECRYPTION_MAP[char] || char;  }
  return result;}
// Looks for a sheet by name; if not found, tries the encrypted name
// Returns an object { sheet, wasEncrypted } or null
function findSheetWithDecryption(sourceFile, selectedSheetName) {
  let sourceSheet = sourceFile.getSheetByName(selectedSheetName);
  if (sourceSheet) return { sheet: sourceSheet, wasEncrypted: false };
  const encryptedName = encryptText(selectedSheetName);
  sourceSheet = sourceFile.getSheetByName(encryptedName);
  if (sourceSheet) return { sheet: sourceSheet, wasEncrypted: true };
  return null;}
// Decrypt the content of cell A1 (if not empty)
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
// IMPORT – user‑visible import function (shows alert on failure)
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
// INTELLIGENT 🌙 FILTER
// Hides rows that neither contain a 🌙 nor a value from the header row (row 2)
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
// TIME TRACKING – logs when a sheet was created and updates master sheet
// Stores current timestamp as ISO string in script properties
function markSheetCreated() {
  const props = PropertiesService.getScriptProperties();
  props.setProperty("lastSheetCreated", new Date().toISOString());}
// Increments the import counter in cell A3 of the master sheet
function updateMasterSheetCounter() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const masterSheet = ss.getSheetByName(MASTER_SHEET_NAME);
  if (!masterSheet) return;
  const counterCell = masterSheet.getRange("A3");
  let count = counterCell.getValue();
  if (typeof count !== "number") count = 0;
  count += 1;
  counterCell.setValue(count);}
// Formats a date as DD.MM.YYYY_HH:MM:SS
function formatDateForMasterSheet(date) {
  const d = new Date(date);
  const day = String(d.getDate()).padStart(2, "0");
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const year = d.getFullYear();
  const hours = String(d.getHours()).padStart(2, "0");
  const minutes = String(d.getMinutes()).padStart(2, "0");
  const seconds = String(d.getSeconds()).padStart(2, "0");
  return `${day}.${month}.${year}_${hours}:${minutes}:${seconds}`;}
// Writes the last import time into cell B3 of the master sheet
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
// CLEANUP – deletes temporary sheets after a period of inactivity
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
// TRIGGERS – creates the necessary onEdit and time-based triggers
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
// onEdit WITH MUTEX – prevents concurrent execution, searches with all prefix/encryption combinations
function onEditHandler(e) {
  if (!e) return;
  const props = PropertiesService.getScriptProperties();
  if (props.getProperty("isProcessing") === "true") return;   // skip if already running
  props.setProperty("isProcessing", "true");
  try {
    const sheet = e.range.getSheet();
    if (sheet.getName() !== MASTER_SHEET_NAME) return;
    const cell = e.range.getA1Notation();
    let selectedSheet = e.range.getValue();
    if (!selectedSheet) return;
    let applyFilter = false;
    if (selectedSheet.endsWith("🌙")) {                        // moon filter requested
      applyFilter = true;
      selectedSheet = selectedSheet.replace("🌙", "").trim();    }
    let newSheet = null;
    let needsDecryption = false;
    const prefixes = PREFIX_MAP[cell];
    if (prefixes && prefixes.length > 0) {
      const decryptedSelected = decryptText(selectedSheet);   // also try with decrypted dropdown value
      for (const prefix of prefixes) {
        const encryptedPrefix = encryptText(prefix);
        // 1. Plain prefix + original dropdown
        let result = tryImportSheet(prefix + selectedSheet);
        if (result) {
          newSheet = result.sheet;
          needsDecryption = result.wasEncrypted;
          break;        }
        // 2. Encrypted prefix + original dropdown
        result = tryImportSheet(encryptedPrefix + selectedSheet);
        if (result) {
          newSheet = result.sheet;
          needsDecryption = true;
          break;        }
        // 3. Plain prefix + decrypted dropdown
        result = tryImportSheet(prefix + decryptedSelected);
        if (result) {
          newSheet = result.sheet;
          needsDecryption = result.wasEncrypted;
          break;        }
        // 4. Encrypted prefix + decrypted dropdown
        result = tryImportSheet(encryptedPrefix + decryptedSelected);
        if (result) {
          newSheet = result.sheet;
          needsDecryption = true;
          break;        }      }
    } else {
      // No prefixes (e.g. B2) – just try the dropdown value
      const result = tryImportSheet(selectedSheet);
      if (result) {
        newSheet = result.sheet;
        needsDecryption = result.wasEncrypted;      }    }
    // Show a single alert if nothing was found after all attempts
    if (!newSheet) {
      SpreadsheetApp.getUi().alert("❌ Sheet nicht gefunden: " + selectedSheet);
      return;    }
    // Decrypt A1 if the source was encrypted or the encrypted prefix was used
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
// SILENT IMPORT – same logic as importiereSheetProUser but without alert; returns { sheet, wasEncrypted } or null
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
  // Decryption is handled by the caller (onEditHandler) based on needsDecryption
  ss.setActiveSheet(newSheet);
  newSheet.showSheet();
  markSheetCreated();
  updateMasterSheetCounter();
  updateMasterSheetLastTime();
  return { sheet: newSheet, wasEncrypted: wasEncrypted };}
// ===================================================================================================
//                                      importSheetProUser
// ===================================================================================================
