import os
import re

# Define paths for the folder containing extracted vehicle meta files and the output folder where sorted files will be stored.
extracted_folder = "D:/GtaFiles/raw"  
output_folder = "D:/GtaFiles/sorted"  

# This dictionary maps certain vehicle names to their special handling names. 
# Some vehicles have alternative names used in specific metadata files.
special_handling_names = {
    "annihilator": "ANNIHL",
    "annihilator2": "ANNIHLATOR2",
    "armytrailer2": "ARMYTRAILER",
    "armytanker": "TANKER",
    "asea2": "ASEA",
    "avenger2": "AVENGER",
    "avenger4": "AVENGER3",
    "bati2": "BATI",
    "benson2": "BENSON",
    "bfinjection": "BFINJECT",
    "blazer3": "BLAZER",
    "blista3": "BLISTA2",
    "boattrailer2": "BOATTRAILER",
    "boattrailer3": "BOATTRAILER",
    "boxville2": "BOXVILLE",
    "boxville3": "BOXVILLE",
    "boxville4": "BOXVILLE",
    "boxville6": "BOXVILLE",
    "brickade2": "BRICKADE",
    "bruiser3": "BRUISER",
    "btype3": "ROOSEVELT2",
    "buccaneer": "BUCCANEE",
    "buccaneer2": "BUCCANEE2",
    "bulldozer": "BULLDOZE",
    "burrito3": "BURRITO",
    "burrito4": "BURRITO",
    "burrito5": "BURRITO",
    "cablecar": "FREIGHT",
    "carbonizzare": "CARBONIZ",
    "carbonrs": "CARBON",
    "cargobob2": "CARGOBOB",
    "cargobob3": "CARGOBOB",
    "cargobob4": "CARGOBOB",
    "cargoplane2": "CARGOPLANE",
    "cavalcade2": "CAVCADE",
    "cerberus3": "CERBERUS",
    "cliffhanger": "CLIFFHANG",
    "cognoscenti": "COGNOSC",
    "cognoscenti2": "COGNOSC2",
    "comet2": "COMET",
    "deathbike3": "DEATHBIKE",
    "dinghy3": "DINGHY",
    "dinghy4": "DINGHY",
    "dilettante2": "DILETTANTE",
    "dodo": "SEAPLANE",
    "dominator6": "DOMINATOR4",
    "dubsta2": "DUBSTA",
    "emperor2": "EMPEROR",
    "emperor3": "EMPEROR",
    "faction2": "FACTION",
    "faggio2": "FAGGIO",
    "feltzer2": "FELTZER",
    "freight2": "FREIGHT",
    "freightcar2": "FREIGHTCAR",
    "freightcont1": "FREIGHT",
    "freightcont2": "FREIGHT",
    "freightgrain": "FREIGHT",
    "freighttrailer": "FREIGHT",
    "frogger2": "FROGGER",
    "graintrailer": "GRAINTRAIL",
    "impaler4": "IMPALER2",
    "inductor2": "INDUCTOR",
    "innovation": "INNOVAT",
    "iwagen": "I-WAGEN",
    "journey2": "JOURNEY",
    "khamelion": "KHAMEL",
    "landstalker2": "LANDSTLKR2",
    "mesa2": "MESA",
    "mesa3": "MESA",
    "moonbeam2": "MOONBEAM",
    "monster4": "MONSTER3",
    "monster5": "MONSTER3",
    "mule2": "MULE",
    "mule5": "MULE3",
    "ninef2": "NINEF",
    "nightshade": "NITESHAD",
    "phantom4": "PHANTOM",
    "police4": "POLICE",
    "police5": "police5",
    "policeold1": "POLICEOLD",
    "policeold2": "POLICEOL2",
    "pony2": "PONY",
    "rancherxl2": "RANCHERXL",
    "rapidgt2": "RAPIDGT",
    "ratloader": "RLOADER",
    "ratloader2": "RLOADER2",
    "rebel2": "REBEL",
    "rentalbus": "TOURBUS",
    "ruiner3": "RUINER",
    "rumpo2": "RUMPO",
    "sadler2": "SADLER",
    "sandking2": "SANDKING",
    "sanchez2": "SANCHEZ",
    "scarab3": "SCARAB",
    "schwarzer": "SCHWARZE",
    "seasparrow3": "SEASPARROW2",
    "seashark2": "SEASHARK",
    "seashark3": "SEASHARK",
    "sentinel2": "SENTINEL",
    "sheriff2": "FBI2",
    "slamvan6": "SLAMVAN4",
    "sovereign": "POLICEB",
    "speeder2": "SPEEDER",
    "speedo2": "SPEEDO",
    "speedo5": "SPEEDO4",
    "stockade3": "STOCKADE",
    "stromberg": "STROMBER",
    "supervolito": "SVOLITO",
    "supervolito2": "SVOLITO",
    "surfer2": "SURFER",
    "surfer3": "SURFER",
    "tankercar": "FREIGHT",
    "tanker2": "TANKER",
    "terbyte": "TERRORBYTE",
    "tornado2": "TORNADO",
    "tornado3": "TORNADO",
    "tornado4": "TORNADO",
    "towtruck4": "TOWTRUCK3",
    "tr4": "TR2",
    "trailers2": "TRAILER",
    "trailers3": "TRAILER",
    "trailers4": "TRAILER",
    "trailers5": "TRAILER",
    "trailerlogs": "TRAILERL",
    "tractor3": "TRACTOR2",
    "tribike2": "TRIBIKE",
    "tribike3": "TRIBIKE",
    "trophytruck": "TROPHY",
    "trophytruck2": "TROPHY2",
    "tvtrailer": "TRAILER",
    "tvtrailer2": "TRAILER",
    "utillitruck": "UTILTRUC",
    "utillitruck2": "UTILTRUC2",
    "utillitruck3": "UTILTRUC3",
    "valkyrie": "VALKYR",
    "valkyrie2": "VALKYR2",
    "velum2": "VELUM",
    "verlierer2": "VERLIER",
    "zion2": "ZION",
    "zr3803": "ZR380",
    "ambulance":"AMBULAN",
    "brutus3":"BRUTUS",
    "tropic2":"TROPIC",
    "issi6":"ISSI4",
    "issi2":"ISSI",
    "police5":"POLICE",
    "bison3":"BISON",
    "toro2":"TORO",
    "barracks3":"BARRACKS",
    "bison2":"BISON",
    "imperator3":"IMPERATOR",
}

# This function searches the specified folder and its subdirectories to find all `vehicles.meta` files.
def find_vehicle_meta_files(folder):
    vehicle_meta_files = []
    for root, dirs, files in os.walk(folder, topdown=True, followlinks=True):
        for file in files:
            if file.lower() == "vehicles.meta":  # Case-insensitive match for 'vehicles.meta'
                vehicle_meta_files.append(os.path.join(root, file))  # Add the full path of the file
    return vehicle_meta_files

# This function recursively searches for any metadata files (e.g., handling.meta, vehicles.meta) 
# that match the names provided in `meta_file_names`.
def find_meta_files(folder, meta_file_names):
    meta_files = {}
    for root, dirs, files in os.walk(folder, topdown=True, followlinks=True):
        for file in files:
            if file.lower() in (name.lower() for name in meta_file_names):  # Case-insensitive matching
                if file.lower() not in meta_files:
                    meta_files[file.lower()] = []
                meta_files[file.lower()].append(os.path.join(root, file))  # Store the full file path
    return meta_files

# This function reads the `vehicles.meta` file and extracts car names (model names) found in the XML structure.
# The car names are found within `<modelName>` tags.
def extract_car_names(vehicle_meta_path):
    car_names = []
    with open(vehicle_meta_path, 'r', encoding='utf-8') as file:
        data = file.read()
        # Use regex to find all occurrences of car names within `<modelName>` tags.
        matches = re.findall(r'<modelName>(.*?)</modelName>', data)
        car_names.extend(list(set(matches)))  # Ensure unique car names (removes duplicates)
    return car_names

# This function ensures that all opened XML tags have corresponding closing tags.
# It's especially useful when the file may have missing closing tags due to incomplete entries.
def ensure_closing_tags(lines, section_tags):
    open_tags = []
    for line in lines:
        stripped_line = line.strip()
        for tag in section_tags:
            # If an open tag is found, add it to the list.
            if re.match(f'<{tag}[^/>]*>', stripped_line) and not stripped_line.endswith('/>'):
                open_tags.append(tag)
            # If a matching close tag is found, remove the corresponding open tag.
            elif stripped_line == f'</{tag}>' and tag in open_tags:
                open_tags.remove(tag)
    # Add missing closing tags for any remaining unclosed sections.
    for tag in reversed(open_tags):
        lines.append(f'</{tag}>\n')
    return lines

# This function extracts a specific vehicle's handling section from `handling.meta`. 
# It looks for the `<handlingName>` tag that corresponds to the car's name or its special name from `special_handling_names`.
def extract_vehicle_section(file_path, car_name, section_type=None):
    section_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        inside_section = False
        current_section = []
        for line in file:
            stripped_line = line.strip()
            if '<Item ' in stripped_line and not inside_section:
                current_section = [line]
                inside_section = False
            elif '<handlingName>' in stripped_line:
                # Use the special handling name if it exists, otherwise use the default car name.
                handling_name = special_handling_names.get(car_name, car_name)
                if handling_name.upper() in stripped_line.upper():
                    inside_section = True
                    current_section.append(line)
                else:
                    current_section = []
            elif inside_section:
                current_section.append(line)
                if '</Item>' in stripped_line:
                    inside_section = False
                    section_lines.extend(current_section)
                    break  # Only extract the first matching item
    if section_lines:
        section_lines = ensure_closing_tags(section_lines, ['SubHandlingData', 'Item'])
        return section_lines
    else:
        return []

# This function extracts a car's section from `vehicles.meta` by finding the `<modelName>` tag that matches the car name.
# It also ensures the entire block is extracted, including any nested items.
def extract_vehicles_meta_section(file_path, car_name):
    section_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        inside_section = False
        current_section = []
        depth = 0
        for line in file:
            stripped_line = line.strip()
            if '<Item' in stripped_line and not inside_section:
                current_section = [line]
                inside_section = True
                depth = 1
            elif inside_section:
                current_section.append(line)
                if '<modelName>' in stripped_line and car_name.upper() in stripped_line.upper():
                    inside_section = True
                if '<Item' in stripped_line:
                    depth += 1
                if '</Item>' in stripped_line:
                    depth -= 1
                    if depth == 0:  # End of the section
                        section_lines.extend(current_section)
                        break
    if section_lines:
        section_lines = ensure_closing_tags(section_lines, ['Item', 'firstPersonDrivebyData', 'InitDatas', 'CVehicleModelInfo__InitDataList'])
        return section_lines
    else:
        return []

# This function wraps handling data in the required XML structure with proper indentation.
def wrap_with_handling_tags(section_lines):
    wrapped_lines = [
        '<?xml version="1.0" encoding="utf-8"?>\n',
        '<CHandlingDataMgr>\n',
        '  <HandlingData>\n',
    ]
    indented_section = fix_indentation(section_lines, initial_indent=2)
    wrapped_lines.extend(indented_section)
    wrapped_lines.append('  </HandlingData>\n')
    wrapped_lines.append('</CHandlingDataMgr>\n')
    return wrapped_lines

# This function wraps vehicle data in the required XML structure with proper indentation.
def wrap_with_vehicles_meta_tags(section_lines):
    wrapped_lines = [
        '<?xml version="1.0" encoding="utf-8"?>\n',
        '<CVehicleModelInfo__InitDataList>\n',
        '  <InitDatas>\n',
    ]
    indented_section = fix_indentation(section_lines, initial_indent=2)
    wrapped_lines.extend(indented_section)
    wrapped_lines.append('  </InitDatas>\n')
    wrapped_lines.append('</CVehicleModelInfo__InitDataList>\n')
    return wrapped_lines

# This function ensures proper indentation of XML sections. 
# Each opening tag increases the indent level, and each closing tag decreases it.
def fix_indentation(lines, initial_indent=2):
    indented_lines = []
    indent_level = initial_indent
    indent_str = '  '  # Two spaces per indentation level
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('</'):
            indent_level -= 1
        indented_lines.append(indent_str * indent_level + stripped_line + '\n')
        if stripped_line.startswith('<') and not stripped_line.startswith('</') and not stripped_line.endswith('/>'):
            indent_level += 1
    return indented_lines

# This function organizes the `handling.meta` and `vehicles.meta` data for each car by extracting and writing relevant data to the output folder.
def organize_meta_files(car_names):
    meta_file_names = ['handling.meta', 'vehicles.meta']
    meta_files = find_meta_files(extracted_folder, meta_file_names)

    cars_populated = 0
    vehicles_with_no_data = []  
    empty_folders = []  
    large_entries = []  

    for car_name in car_names:
        car_folder = os.path.join(output_folder, car_name)
        os.makedirs(car_folder, exist_ok=True)  # Create a folder for the car if it doesn't exist

        populated = False  
        handled_sections = set()  # Keep track of processed sections to avoid duplicates

        # Extract handling.meta data
        for file_path in meta_files.get('handling.meta', []):
            new_section = extract_vehicle_section(file_path, car_name, section_type="handling")
            section_signature = ''.join(new_section)
            if section_signature not in handled_sections and new_section:
                handled_sections.add(section_signature)
                wrapped_section = wrap_with_handling_tags(new_section)
                output_file_path = os.path.join(car_folder, 'handling.meta')
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.writelines(wrapped_section)
                populated = True
                break  # No need to process further once data is found

        # Extract vehicles.meta data
        for file_path in meta_files.get('vehicles.meta', []):
            new_section = extract_vehicles_meta_section(file_path, car_name)
            if len(new_section) > 250:
                large_entries.append(car_name)
            section_signature = ''.join(new_section)
            if section_signature not in handled_sections and new_section:
                handled_sections.add(section_signature)
                wrapped_section = wrap_with_vehicles_meta_tags(new_section)
                output_file_path = os.path.join(car_folder, 'vehicles.meta')
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.writelines(wrapped_section)
                populated = True
                break

        if populated:
            cars_populated += 1
        else:
            vehicles_with_no_data.append(car_name)  # Track vehicles with no data

        if not os.listdir(car_folder):  # Check if folder is empty after processing
            empty_folders.append(car_name)

    print(f'Total cars with data populated: {cars_populated}')
    
    if empty_folders:
        print("Empty folders:")
        for folder in empty_folders:
            print(folder)

    if large_entries:
        print("Entries that exceed 250 lines:")
        for entry in large_entries:
            print(entry)

# Main function that kicks off the process by finding all car names and organizing the relevant meta files.
def main():
    vehicle_meta_files = find_vehicle_meta_files(extracted_folder)
    
    if not vehicle_meta_files:
        print("No vehicle.meta files found.")
        return

    car_names = []
    for vehicle_meta_path in vehicle_meta_files:
        car_names.extend(extract_car_names(vehicle_meta_path))

    car_names = list(set(car_names))  # Remove duplicate car names
    print(f"Found {len(car_names)} unique car names.")

    organize_meta_files(car_names)

# Run the script if executed as the main program.
if __name__ == "__main__":
    main()
