// Fetch and populate the dropdown with rule names when the page loads
window.onload = function() {
    fetchAndPopulateRules(); // Populate the initial rule dropdown
    addDefaultRuleSelectors(); // Add default rules and operator on page load
};

// Function to fetch rules and populate dropdowns
function fetchAndPopulateRules() {
    fetch("http://127.0.0.1:5000/get_rules")
        .then(response => response.json())
        .then(data => {
            if (!Array.isArray(data)) {
                console.error("Expected an array of rules");
                return;
            }

            // Populate the ruleSelect dropdown
            const ruleSelect = document.getElementById('ruleSelect');
            populateDropdown(ruleSelect, data);

            // Populate other dropdowns with the class ruleSelect
            const ruleSelects = document.querySelectorAll('.ruleSelect');
            ruleSelects.forEach(select => {
                populateDropdown(select, data);
        
            });
        })
        .catch(error => {
            console.error("Error fetching rules:", error);
            alert("Failed to load rules. Please try again later.");
        });
}
// Populate a specific dropdown with rules
function populateDropdown(selectElement, data) {
    // Clear existing options
    selectElement.innerHTML = '';

    // Create and append a placeholder option
    const placeholderOption = document.createElement("option");
    placeholderOption.value = ""; // No value for the placeholder
    placeholderOption.textContent = "Select a rule"; // Placeholder text
    placeholderOption.disabled = true; // Disable the placeholder option
    placeholderOption.selected = true; // Make it the default selected option
    selectElement.appendChild(placeholderOption);

    // Append fetched rule options
    data.forEach(rule => {
        const option = document.createElement("option");
        option.value = rule.rule_string; // Using rule string as the value for evaluation
        option.textContent = rule.name; // Display rule name
        selectElement.appendChild(option);
    });
}

// Function to add default rule selects and operator
function addDefaultRuleSelectors() {
    const combinedRulesContainer = document.getElementById("combinedRulesContainer");
    const newCombinedRuleDiv = document.createElement("div");
    newCombinedRuleDiv.className = "combined-rule";

    // Create the first rule dropdown and operator dropdown
    newCombinedRuleDiv.appendChild(createDropdown("Select Rule:", "ruleSelect")); // First rule dropdown
    newCombinedRuleDiv.appendChild(createOperatorDropdown()); // Operator dropdown
    newCombinedRuleDiv.appendChild(createDropdown("Select Rule:", "ruleSelect")); // Second rule dropdown

    combinedRulesContainer.appendChild(newCombinedRuleDiv);
}

// Function to create a dropdown
function createDropdown(labelText, className) {
    const label = document.createElement("label");
    label.textContent = labelText;

    const select = document.createElement("select");
    select.className = className + " ruleSelect"; // Use the same class for easy selection
    select.style.width = "100%";
    select.style.marginBottom = "10px";

    const container = document.createElement("div");
    container.appendChild(label);
    container.appendChild(select);
    
    return container;
}

// Function to create an operator dropdown
function createOperatorDropdown() {
    const label = document.createElement("label");
    label.textContent = "Select Operator:";

    const select = document.createElement("select");
    select.className = "operatorSelect";
    select.style.width = "100%";
    select.style.marginBottom = "10px";

    const operators = ["AND", "OR"];
    operators.forEach(operator => {
        const option = document.createElement("option");
        option.value = operator;
        option.textContent = operator;
        select.appendChild(option);
    });

    const container = document.createElement("div");
    container.appendChild(label);
    container.appendChild(select);
    
    return container;
}

// Handle the form submission to create a new rule
document.getElementById("ruleForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const ruleName = document.getElementById("rule_name").value;
    const ruleString = document.getElementById("rule_string").value;

    const payload = {
        rule_name: ruleName,
        rule_string: ruleString
    };

    fetch("http://127.0.0.1:5000/create_rule", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())  // Parse the JSON response
    .then(data => {
        // If there's an ast_tree in the response, format and display it
        if (data.ast_tree) {
            const formattedAstTree = data.ast_tree.replace(/\n/g, '<br>');  // Format AST tree with line breaks
            document.getElementById("astResult").innerHTML = formattedAstTree;  // Display the formatted AST tree
        }

        // Display the success message from the response
        document.getElementById("message").textContent = data.message;

        // Optionally fetch and update the dropdown with new rules after rule creation
        fetchAndPopulateRules();
    })
    .catch(error => {
        document.getElementById("message").textContent = "Error: " + error.message;
    });
});

// Handle evaluation of the selected rule
document.getElementById("evaluateButton").addEventListener("click", function() {
    const selectedRuleString = document.getElementById("ruleSelect").value; 
    const dataInput = document.getElementById("dataInput").value;

    if (!selectedRuleString) {
        alert("Please select a rule to evaluate.");
        return;
    }

    let data;
    try {
        data = JSON.parse(dataInput); // Parse JSON data from input
    } catch (error) {
        alert("Invalid JSON format. Please enter valid JSON data.");
        return;
    }

    const payload = {
        rule: selectedRuleString,
        data: data
    };

    fetch("http://127.0.0.1:5000/evaluate_rule", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        const resultBox = document.getElementById("messageevaluate");
        resultBox.style.display = 'block'; // Show the result box

        if (data.result === true) {
            resultBox.textContent = "Evaluation result: True";
            resultBox.classList.remove('result-false');
            resultBox.classList.add('result-true'); // Apply green box
        } else if (data.result === false) {
            resultBox.textContent = "Evaluation result: False";
            resultBox.classList.remove('result-true');
            resultBox.classList.add('result-false'); // Apply red box
        } else {
            resultBox.textContent = "Error: Unexpected result";
            resultBox.classList.remove('result-true', 'result-false');
        }
    })
    .catch(error => {
        const resultBox = document.getElementById("messageevaluate");
        resultBox.style.display = 'block';
        resultBox.textContent = "Error: " + error.message;
        resultBox.classList.remove('result-true', 'result-false');
    });
});


// Add new rule selection dropdowns
// Add new rule selection dropdowns when "Add Rule" button is clicked
document.getElementById("addRuleButton").addEventListener("click", function() {
    const combinedRulesContainer = document.getElementById("combinedRulesContainer");
    const newCombinedRuleDiv = document.createElement("div");
    newCombinedRuleDiv.className = "combined-rule";

    // Add operator dropdown and new rule dropdown
    newCombinedRuleDiv.appendChild(createOperatorDropdown()); // Operator dropdown
    const newRuleDropdown = createDropdown("Select Rule:", "ruleSelect"); // Rule dropdown
    newCombinedRuleDiv.appendChild(newRuleDropdown);

    combinedRulesContainer.appendChild(newCombinedRuleDiv);

    console.log("Fetching rules for newly added dropdown...");

    // Fetch rules only for the newly added dropdown
    fetch("http://127.0.0.1:5000/get_rules")
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok " + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log("Fetched rules:", data);  // Log the fetched data to see if it’s correct

            if (!Array.isArray(data)) {
                console.error("Expected an array of rules but got:", data);
                return;
            }

            // Populate only the newly added rule dropdown
            populateDropdown(newRuleDropdown.querySelector('select'), data);
        })
        .catch(error => {
            console.error("Error fetching rules:", error);  // Log the error for detailed output
            alert("Failed to load rules. Please try again later.");
        });
});

document.getElementById("combineButton").addEventListener("click", function() {
    const ruleNameInput = document.getElementById("rule_name_combine");
    const ruleName = ruleNameInput.value.trim();

    // Check if the rule name is provided
    if (!ruleName) {
        alert("Please enter a rule name before combining.");
        return;  // Stop execution if the rule name is blank
    }

    const combinedRules = [];
    const combinedOperators = [];

    const ruleSelects = document.querySelectorAll('.ruleSelect');
    const operatorSelects = document.querySelectorAll('.operatorSelect');

    // Validate that all rule dropdowns have selected values
    let hasUnselectedRule = false;
    ruleSelects.forEach(select => {
        if (select.value) {
            combinedRules.push({ "rule": select.value });
        } else {
            hasUnselectedRule = true;  // Mark if any rule dropdown is unselected
        }
    });

    // Validate that all operator dropdowns have selected values
    let hasUnselectedOperator = false;
    operatorSelects.forEach(select => {
        if (select.value) {
            combinedOperators.push({ "operator": select.value });
        } else {
            hasUnselectedOperator = true;  // Mark if any operator dropdown is unselected
        }
    });

    // Alert the user if any dropdowns are left unselected
    if (hasUnselectedRule) {
        alert("Please select a rule from all dropdowns.");
        return;  // Stop the function if a rule is not selected
    }

    if (hasUnselectedOperator) {
        alert("Please select an operator from all dropdowns.");
        return;  // Stop the function if an operator is not selected
    }

    const payload = {
        rule_names: ruleName,
        rules: combinedRules,
        operators: combinedOperators
    };

    // Proceed with the fetch request if validation passes
    fetch("http://127.0.0.1:5000/combine_rules", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        // If combined_ast exists, format and display it
        if (data.combined_ast) {
            const formattedAstTree = data.combined_ast.replace(/\n/g, '<br>');
            document.getElementById("message3").innerHTML = formattedAstTree;
        }

        // Display the response message
        if (data.message) {
            document.getElementById("message4").textContent = data.message;
        }

        // Optionally re-fetch and update the rule dropdowns
        fetchAndPopulateRules();
    })
    .catch(error => {
        document.getElementById("message3").textContent = "Error: " + error.message;
    });
});
