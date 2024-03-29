function showView(show, view) {
  const display = show ? "flex" : "none";
  var viewElement = document.getElementById(view);
  viewElement.style.display = display;
}

function generateUsersTable(users) {
    const tbl = document.getElementById("usersTable")
    const tblBody = document.createElement("tbody");

    if (users.length == 0) {
      showView(true, "emptyUsersText");
      return;
    }

    users.forEach((user) => {
        const row = document.createElement("tr");

        addRow(tblBody, row, user["id"]);
        addRow(tblBody, row, user["email"]);
        addRow(tblBody, row, user["zip_code"]);
        addRow(tblBody, row, user["serial_number"]);
    });
  
    tbl.appendChild(tblBody);
  }

  function addRow(tblBody, row, value) {
    const cell = document.createElement("td");
    const cellText = document.createTextNode(value);
    cell.appendChild(cellText);
    row.appendChild(cell);

    // add the row to the end of the table body
    tblBody.appendChild(row);
  }
  

  jQuery(document).ready(function ($) {
    showView(true, "spinner");
    showView(false, "emptyUsersText");

    retrieveAudioMothUsers( function (response) {
        showView(false, "spinner");
    
        if (response == null) {
          alert("Failed to retrive AudioMoth users");
          return;
        }

        if (!response["success"]) {
            alert(response["error"]);
            return;
        }

        generateUsersTable(response["data"]);
      });
  });

  function filterUsers() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("filterInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("usersTable");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[1];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }       
    }
  }
