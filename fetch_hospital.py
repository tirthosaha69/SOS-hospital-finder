import json
import re
from langchain.prompts import PromptTemplate
from model.llm import model  # your custom LLM wrapper

# Step 1: Load hospitals data
def load_hospitals():
    with open("hospitals/hospitals.json", "r", encoding="utf-8") as f1:
        hospitals1 = json.load(f1)
    with open("hospitals/hospitals2.json", "r", encoding="utf-8") as f2:
        hospitals2 = json.load(f2)
    return hospitals1 + hospitals2


# Step 2: Extract pin code
def extract_pincode(address: str):
    match = re.search(r"\b\d{6}\b", address)
    return match.group(0) if match else None


# Step 3: Improved prompt
prompt_template = PromptTemplate(
    input_variables=["user_address", "hospital_data"],
    template="""
You are an assistant that finds the nearest hospitals.

User address: {user_address}

Hospital list:
{hospital_data}

Return ONLY the top 3 to 5 nearest hospitals in valid JSON format.
Do not add explanations, notes, or extra text.
Format strictly as:
[
  {{
    "hospital_name": "Hospital Name",
    "address": "Full Address",
    "phone_number": "Phone Number"
  }}
]
"""
)

# Step 4: Build new chain
chain = prompt_template | model()


# Step 5: Function to get nearest hospital
def get_nearest_hospital(user_address: str):
    hospitals = load_hospitals()
    user_pincode = extract_pincode(user_address)

    # Try exact pincode match first
    if user_pincode:
        matched = [h for h in hospitals if user_pincode in h["address"]]
        if matched:
            return matched[:5]  # return top 3–5 matches

    # Fall back to LLM
    hospital_str = "\n".join(
        [f"{h['hospital_name']} - {h['address']} - {h['phone_number']}" for h in hospitals]
    )
    response = chain.invoke({
        "user_address": user_address,
        "hospital_data": hospital_str
    }).content

    try:
        return json.loads(response)  # ✅ always return list of dicts
    except json.JSONDecodeError:
        return []


# Example usage
if __name__ == "__main__":
    address = "Salt Lake Sector V, Kolkata 700091"
    result = get_nearest_hospital(address)
    print("Nearest Hospital(s):")
    print(result)
