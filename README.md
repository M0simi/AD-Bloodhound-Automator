# AD-Bloodhound-Automator 🩸

**AD-Bloodhound-Automator** is an offensive security utility designed to streamline Active Directory reconnaissance. It wraps and automates execution workflows for `bloodhound-python`, managing secure credential parsing, target Domain Controller mapping, and structured output organization for quick analysis in Bloodhound GUI.

## Features
- **Streamlined Execution:** Eliminates repetitive CLI flags for standard Bloodhound collection phases.
- **Customizable Collection Methods:** Pass specific collection flags (`Group`, `LocalAdmin`, `Session`, `All`) seamlessly.
- **Structured Storage:** Automatically generates and isolates output archives into designated directories for ingest.

## Installation & Usage

1. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the automation script against your lab or target AD environment:
   ```bash
   python bloodhound_automator.py -d example.comm -u administrator -p "SecurePassword123" --dc-ip 000.000.000.000 -c All -o ./results
   ```
   
