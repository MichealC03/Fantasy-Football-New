$(document).ready(function() {
    initializeDataTables();
});

function initializeDataTables() {
    if ($.fn.DataTable.isDataTable('table')) {
        $('table').DataTable().destroy();
    }

    let table = $('table').DataTable({
        paging: false,
        searching: true,
        ordering: true,
        lengthChange: false,
        scrollY: '400px',
        scrollCollapse: true,
        order: [[2, 'asc']]
    });

    highlightCells();
}

function highlightCells() {
    // Select all rows in the table
    $('table tbody tr').each(function() {
        let $row = $(this);
        // Get the value to compare from the third column
        let valueToCompare = parseFloat($row.find('td:eq(2)').text().trim());

        // Iterate through the target columns (startCol to endCol)
        $row.find('td').each(function(index) {
            if (index >= 3 && index <= 4) { // Adjust based on your startCol and endCol
                let cellValue = parseFloat($(this).text().trim());
                
                if (cellValue > valueToCompare) {
                    $(this).addClass('highlight-col');
                } else {
                    $(this).removeClass('highlight-col');
                }
            }
        });
    });
}

function updateTable(tableName) {
    $.ajax({
        url: `/update_table/${tableName}`,
        method: 'GET',
        success: function(response) {
            $('#table2-container').html(response.table_html);

            setTimeout(function() {
                let updatedTable = $('#table2-container table').DataTable({
                    paging: false,
                    searching: true,
                    ordering: true,
                    lengthChange: false,
                    scrollY: '400px',
                    scrollCollapse: true,
                    order: [[2, 'asc']]
                });

                highlightCells();
            }, 100);
        },
        error: function() {
            console.error('Failed to update the table.');
        }
    });
}