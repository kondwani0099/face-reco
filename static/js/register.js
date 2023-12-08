const recognizingMessage = document.getElementById('recognizingMessage');
const personName = document.getElementById('personName');

// Maintain a dictionary to store recognized persons and their names
const recognizedPersons = {};

// Function to show the recognizing message
function showRecognizingMessage() {
    recognizingMessage.style.display = 'block';
}

// Function to hide the recognizing message
function hideRecognizingMessage() {
    recognizingMessage.style.display = 'none';
}

// Function to update the displayed names
function updatePersonNames() {
    // Create a list of names from recognizedPersons
    const names = Object.values(recognizedPersons);

    // Display the names in the 'personName' element
    personName.innerText = `Persons: ${names.join(', ')}`;
}

// Function to fetch and update the person's name from SQL
function fetchPersonName(id) {
    if (recognizedPersons[id]) {
        // If the person's name is already recognized, no need to fetch it again
        return;
    }

    showRecognizingMessage();

    fetch(`/get_person_name?id=${id}`)
        .then(response => response.json())
        .then(data => {
            hideRecognizingMessage();
            if (data.success) {
                // Update the recognized persons dictionary
                recognizedPersons[id] = data.name;
                updatePersonNames();
            } else {
                recognizedPersons[id] = 'UNKNOWN';
                updatePersonNames();
            }
        })
        .catch(error => {
            hideRecognizingMessage();
            console.error('Error:', error);
        });
}
function addRecognitionToLog(id, name) {
    const logTable = document.getElementById('recognitionLog');
    const tableBody = logTable.getElementsByTagName('tbody')[0];
    const newRow = tableBody.insertRow();
    const cell1 = newRow.insertCell(0);
    const cell2 = newRow.insertCell(1);
    cell1.innerHTML = id;
    cell2.innerHTML = name;
}


// Replace personIds with the actual person IDs when you have detected persons
const personIds = [42, 55, 78]; // Replace with the actual person IDs
personIds.forEach(id => fetchPersonName(id));
