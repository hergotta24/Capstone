function downloadInvoice() {
  // Get HTML content
  var invoiceContent = document.getElementById('invoice').outerHTML;

  // Get CSS styles
  var styleSheets = document.styleSheets;
  var styles = '';
  for (var i = 0; i < styleSheets.length; i++) {
    var styleSheet = styleSheets[i];
    if (styleSheet.cssRules) {
      var rules = styleSheet.cssRules;
      for (var j = 0; j < rules.length; j++) {
        styles += rules[j].cssText + '\n';
      }
    }
  }

  // Merge HTML content and CSS styles
  var htmlWithStyles = '<style>' + styles + '</style>' + invoiceContent;

  // Create Blob
  var blob = new Blob([htmlWithStyles], { type: 'text/html' });

  // Create temporary anchor element
  var a = document.createElement('a');
  a.href = window.URL.createObjectURL(blob);
  a.download = 'invoice.html';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}


document.getElementById('downloadButton').addEventListener('click', downloadInvoice);