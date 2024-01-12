var currentMetric = "tracks";
var currentTimeFrame = "shortTerm";
var currentTableId = "";
var currentNumRows = 10;


document.addEventListener('DOMContentLoaded', function() {
    hideBorders('tracks-shortTerm');
    hideBorders('tracks-mediumTerm');
    hideBorders('tracks-longTerm');
    hideBorders('artists-shortTerm');
    hideBorders('artists-mediumTerm');
    hideBorders('artists-longTerm');
    hideBorders('genres-shortTerm');
    hideBorders('genres-mediumTerm');
    hideBorders('genres-longTerm');

    setMetric();
});


function setMetric() {
    var selection = document.getElementById('selectMetric');
    currentMetric = selection.value; 
    console.log('Selected value:', currentMetric);

    
    showTable(currentTimeFrame);
    removeLines();
    addHorizontalLines(currentTableId);
    changeDisplayType();
   
    
}

function showTable(timeFrame) {
    currentTimeFrame = timeFrame;
    currentTableId = currentMetric + "-" + currentTimeFrame;

    var allButtons = document.querySelectorAll('.set-term-button')

        allButtons.forEach(function(button) {
            if (button.classList.contains('pushed-button')) {
                button.classList.remove('pushed-button');
            }

            button.classList.add('released-button');
            
        });

    var currentButton = document.getElementById(currentTimeFrame);
    currentButton.classList.add('pushed-button');
    currentButton.classList.remove('released-button');

    var tables = document.getElementsByClassName('table');

    var anyTableVisible = false;

   removeLines();
    for (var i = 0; i < tables.length; i++) {
        if (tables[i].getAttribute('id') === currentTableId) {
            tables[i].style.display = 'block';
            showXRows(currentNumRows);
            changeDynamicText();
            changeDisplayType();
          
            anyTableVisible = true; // Set the flag if any table is displayed
        } else {
            tables[i].style.display = 'none';
        }
    }

    const page = document.getElementById('page');

    if (anyTableVisible) {
        page.style.display = 'block'; // Display the page if any table is visible
       
    } else {
        page.style.display = 'none'; // Hide the page if no table is visible
    }   
  
}

function showXRows(x) {
    removeLines();

    currentNumRows = x;
    if (currentTableId != "") {

        var allButtons = document.querySelectorAll('.set-rows-button')

        allButtons.forEach(function(button) {
            if (button.classList.contains('pushed-button')) {
                button.classList.remove('pushed-button');
            }

            button.classList.add('released-button');
            
        });

        var currentButton = document.getElementById(x + 'Rows');
        currentButton.classList.add('pushed-button');
        currentButton.classList.remove('released-button');

        var table = document.getElementById(currentTableId);
        var rows = table.getElementsByTagName("tr");

        for (var i = 0; i <= x && i < rows.length; i++) {
            rows[i].style.display = "table-row";
        }

        for (var i = x+1; i < rows.length; i++) {
            rows[i].style.display = "none";
        }

        changeDynamicText();
        
        
        addHorizontalLines(currentTableId);
        changeDisplayType();
        
    }   
    
}

function changeDynamicText() {
    var text = document.getElementById("book-header");

    var frame = "Long Term";

    if (currentTimeFrame === "shortTerm") {
        frame = "Short Term";
    } else if (currentTimeFrame === "mediumTerm") {
        frame = "Medium Term";
    }
    
    if (currentMetric != "") {
        text.textContent = "Top " + currentNumRows + " " + frame + " " + currentMetric.substring(0, 1).toUpperCase() + currentMetric.substring(1);
      
      text.style.color = '#191414';
      text.style.fontWeight = '500';
      text.style.fontSize = '130%';

        
    }
}


function addHorizontalLines(tableId) {
    var cols = 0;
    if (tableId === 'tracks-shortTerm' || tableId === 'tracks-mediumTerm' || tableId === 'tracks-longTerm') {
        cols = 6;
    }
    if (tableId === 'artists-shortTerm' || tableId === 'artists-mediumTerm' || tableId === 'artists-longTerm') {
        cols = 4;
    }
    if (tableId === 'genres-shortTerm' || tableId === 'genres-mediumTerm' || tableId === 'genres-longTerm') {
        cols = 3;
    }

    addLines(tableId, cols);
}


function addLines(tableId, cols) {
    const tableRows = document.querySelectorAll('#' + tableId + ' tbody tr');
    
    tableRows.forEach((row) => {

        if (row.style.display === 'none') {
            return;
        }

        const lineHTML = '<tr class="page-horizontal-lines"><td colspan="' + cols + '"><div></div></td></tr>';
        row.insertAdjacentHTML('beforebegin', lineHTML);
    });
    
}  

function removeLines() {
    const tables = document.querySelectorAll('table.table');

    // Iterate through each table
    tables.forEach(table => {
        // Get all rows (tr) in the table
        const rows = table.querySelectorAll('tr');

        // Iterate through each row
        rows.forEach(row => {
            // Check if the row has the class 'page-horizontal-lines'
            if (row.classList.contains('page-horizontal-lines')) {
                // Remove the row if it has the class 'page-horizontal-lines'
                row.parentNode.removeChild(row);
            }
        });
    });
}


function hideBorders(tableId) {
    const tableRows = document.querySelectorAll('#' + tableId + ' tbody tr');
  
    tableRows.forEach((row) => {
      row.classList.add('hide_all');
    });

    const topRow = document.querySelectorAll('#' + tableId + ' thead tr');
    topRow.forEach((row) => {
        row.classList.add('hide_all');
      });
} 


function changeDisplayType() {
    var page = document.getElementById('page');
    var table = document.getElementById(currentTableId);
    var header = document.getElementById('book-header');
    var headerEnd = document.getElementById('book-header-end');
   
     page.style.overflowX = 'visible';
   
    var pageWidth = window.getComputedStyle(page).width;
    var parsedPageWidth = parseInt(pageWidth);
    
     var tableWidth = window.getComputedStyle(table).width; 
    var parsedWidth = parseInt(tableWidth); 

  //  table.style.width = '100%'; // added this

    // Check if the value is numeric and then add 40 pixels
    if (!isNaN(parsedWidth) && parsedPageWidth != parsedWidth) {
    parsedWidth += 40; // Add 40 pixels
    var newWidth = parsedWidth + 'px'; // Convert the updated width back to a string with 'px'

    // Set the widths of other elements with the modified width
    
    
    page.style.width = newWidth;
    header.style.width = newWidth;
    headerEnd.style.width = newWidth;
    
    console.log("page width is " + page.style.width);
      
      
      
      console.log("new width is " + newWidth);
    }
    
    var rows = table.querySelectorAll("tbody tr");
    
    rows.forEach((row) => {
      var horizontalLinesDiv = row.querySelector('.page-horizontal-lines > td > div');
    if (horizontalLinesDiv) {
        horizontalLinesDiv.style.width = parsedWidth + 40 + 'px'; //added
      
       console.log(horizontalLinesDiv.style.width);
        
    }
    });
    
    
}


function downloadAsPNG() {
    var targetDiv = document.getElementById('toDownload'); // Replace 'yourDivId' with the actual ID of your target div

    html2canvas(targetDiv, {
        scale: 2, // Adjust the scale as needed for better resolution
    }).then(function (canvas) {
        var dataURL = canvas.toDataURL('image/png');
        
        // Create a link element and trigger a download
        var link = document.createElement('a');
        link.href = dataURL;
        link.download = 'downloaded_image.png'; // Set the desired file name
        link.click();
    });
}




