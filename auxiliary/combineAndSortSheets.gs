function combineAndSortSheets() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var masterSheet = ss.getSheetByName("Master"); // Master sheet name
  var sheets = ss.getSheets();
  
  // Clear existing data in the master sheet, excluding the first row (headers)
  var masterDataRange = masterSheet.getDataRange();
  var masterHeaders = masterDataRange.offset(0, 0, 1).getValues();
  masterSheet.clearContents();
  masterDataRange.offset(0, 0, 1).setValues(masterHeaders);
  
  // Create a new array to hold all data
  var allData = [];
  
  // Loop through all sheets except the master sheet
  for (var i = 0; i < sheets.length; i++) {
    var sheet = sheets[i];
    if (sheet.getName() !== "Master") {
      var dataRange = sheet.getDataRange();
      var dataValues = dataRange.getValues();
      var foundEnd = false;
      
      // Skip headers and keep only data rows
      if (dataValues.length > 1) {
        dataValues.shift(); // Remove header row
      }

      for (var j = 0; j < dataValues.length; j++) {
        if (dataValues[j][0] === "---END---") {
          break;
        }
        allData.push(dataValues[j]);
      }
    }
  }
  
  // Sort the combined data by the timestamp column (column B)
  allData.sort(function(a, b) {
    var dateA = new Date(a[0] + ' ' + a[1]);
    var dateB = new Date(b[0] + ' ' + b[1]);
    return dateA - dateB;
  });
  
  // Write the sorted data to the master sheet, including the first row (headers)
  allData.unshift(masterHeaders[0]); // Add back the headers as the first row
  masterSheet.getRange(1, 1, allData.length, allData[0].length).setValues(allData);
}
