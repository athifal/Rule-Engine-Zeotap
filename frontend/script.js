// Fetch and populate the dropdown with rule names when the page loads
window.onload = function() {
    fetch("http://127.0.0.1:5000/get_rules")
        .then(response => response.json())
        .then(data => {
            const ruleSelect = document.getElementById("ruleSelect");
            const ruleSelect1 = document.getElementById("ruleSelect1");
            const ruleSelect2 = document.getElementById("ruleSelect2");
            
            data.forEach(rule => {
                const option1 = document.createElement("option");
                option1.value = rule.rule_string;
                option1.textContent = rule.name;

                const option2 = document.createElement("option");
                option2.value = rule.rule_string;
                option2.textContent = rule.name;

                ruleSelect.appendChild(option1.cloneNode(true)); // For evaluating a rule
                ruleSelect1.appendChild(option1); // For combining rule 1
                ruleSelect2.appendChild(option2); // For combining rule 2
            });
        })
        .catch(error => {
            console.error("Error fetching rules:", error);
        });
};

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
    .then(response => response.json())
    .then(data => {
        const formattedAstTree = data.ast_tree.replace(/\n/g, '<br>');
        document.getElementById("astResult").innerHTML = formattedAstTree;
        document.getElementById("message").textContent = data.message;
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
        data = JSON.parse(dataInput);
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
        document.getElementById("message").textContent = "Evaluation result: " + data.result;
    })
    .catch(error => {
        document.getElementById("message").textContent = "Error: " + error.message;
    });
});

// Handle combining of two rules
document.getElementById("combineButton").addEventListener("click", function() {
    const selectedRule1 = document.getElementById("ruleSelect1").value;
    const selectedRule2 = document.getElementById("ruleSelect2").value;
    const selectedOperator = document.getElementById("operatorSelect").value;

    if (!selectedRule1 || !selectedRule2) {
        alert("Please select both Rule 1 and Rule 2.");
        return;
    }

    const payload = {
        rules: [
            { rule: selectedRule1 },
            { rule: selectedRule2 }
        ],
        operators: [{ operator: selectedOperator }]
    };

    fetch("http://127.0.0.1:5000/combine_rules", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        const formattedCombinedAstTree = data.combined_ast.replace(/\n/g, '<br>');
        document.getElementById("combinedAstResult").innerHTML = formattedCombinedAstTree;
        document.getElementById("combineMessage").textContent = "Combined successfully.";
    })
    .catch(error => {
        document.getElementById("combineMessage").textContent = "Error: " + error.message;
    });
});
