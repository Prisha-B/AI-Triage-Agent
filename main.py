import csv
import os

# CLEAN FUNCTION 

def clean(text):
    return text.replace("\n", " ").replace("\r", " ")


# Understanding + Classification
def classify_request(issue):
    ...

# Understanding + Classification
 
def classify_request(issue):
    issue_lower = issue.lower()

    if any(word in issue_lower for word in ["error", "bug", "not working", "crash"]):
        return "bug", "technical"

    elif any(word in issue_lower for word in ["refund", "charged", "payment", "billing"]):
        return "product_issue", "billing"

    elif any(word in issue_lower for word in ["feature", "add", "request"]):
        return "feature_request", "product"

    elif any(word in issue_lower for word in ["increase my score", "force", "make them"]):
        return "invalid", "policy"

    else:
        return "product_issue", "general"


 
# Risk Assessment
 
def assess_risk(issue, company):
    issue_lower = issue.lower()

    if any(word in issue_lower for word in ["fraud", "unauthorized", "stolen", "hacked"]):
        return "high"

    if company == "Visa":
        return "high"

    if "access" in issue_lower and company == "Claude":
        return "medium"

    return "low"


 
# Decision Making
 
def decide_action(risk, request_type):
    if risk == "high" or request_type == "invalid":
        return "escalated"
    return "replied"


 
# Retrieval from data/ (simple RAG)
 

def retrieve_from_data(issue, company):
    try:
        path = f"data/{company.lower()}"

        if not os.path.exists(path):
            return None

        for file in os.listdir(path):
            full_path = os.path.join(path, file)

            if not os.path.isfile(full_path):
                continue

            with open(full_path, "r", errors="ignore") as f:
                content = f.read()

                lines = content.split("\n")

                # return first meaningful sentence (skip headings)
                for line in lines:
                    line = line.strip()
                    if len(line) > 50 and not line.startswith("#"):
                        return line[:200]

    except:
        return None

    return None


 
# Response Generation
 
def generate_response(issue, status, product_area, company):
    if status == "escalated":
        return "I understand your concern. This issue has been escalated to a human support specialist for further assistance."

    retrieved = retrieve_from_data(issue, company)

    if retrieved:
        return f"Based on our support documentation: {retrieved}"

    # fallback responses
    if company == "Visa":
        return "I understand how concerning payment issues can be. Please contact your bank or card provider for further assistance."

    elif company == "HackerRank":
        return "Thanks for reaching out. Test evaluations are automated and cannot be manually changed."

    elif company == "Claude":
        return "It seems like you're facing an access issue. Please contact your workspace administrator for assistance."

    return "Thanks for reaching out. Please refer to the help center for more details."


 
# Justification
 
def generate_justification(issue, risk, status, product_area, company):
    return f"Issue categorized under {company}/{product_area}, assessed as {risk} risk, action: {status}."


 
# Main Pipeline
 
def main():
    input_file = "support_tickets/support_tickets.csv"
    output_file = "support_tickets/output.csv"

    with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
        reader = csv.DictReader(infile)

        fieldnames = ["status", "product_area", "response", "justification", "request_type"]
        writer = csv.DictWriter(
    outfile,
    fieldnames=fieldnames,
    quoting=csv.QUOTE_ALL
)

        writer.writeheader()

        for row in reader:
            issue = row["Issue"]
            company = row["Company"]

            request_type, product_area = classify_request(issue)
            risk = assess_risk(issue, company)
            status = decide_action(risk, request_type)
            response = generate_response(issue, status, product_area, company)
            justification = generate_justification(issue, risk, status, product_area, company)

            writer.writerow({
                "status": status,
                "product_area": product_area,
                "response": clean(response),
                "justification": justification,
                "request_type": request_type
            })

    print("Done! Final agent executed successfully.")


if __name__ == "__main__":
    main()